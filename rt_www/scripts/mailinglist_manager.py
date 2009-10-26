import sys, os

from rt_www.registration.models import Registration
from rt_www.mailinglist.models import MailingList, Message
from rt_www.swimmers.models import Swimmer
from django.conf import settings
import poplib, sgmllib, time, email, smtplib, re, rfc822

"""
	How this is going to work:
	Set up the addresses on the remote mailserver that correspond with the mailing lists we support.  Also setup one central 
	mail account named something like listuser@redtidenyc.org.  All the mailing list addresses should forward to this address.
"""

"""
	This takes a list of headers/message body and transforms it into a mime message to send out

"""

class Stripper(sgmllib.SGMLParser):
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		
	def strip(self, some_html):
		self.theString = ""
		self.feed(some_html)
		self.close()
		return self.theString
	def handle_data(self, data):
		self.theString += data



def process_msg(msg):
	msg = email.message_from_string('\n'.join(msg))
	(listname, list_addr) = rfc822.parseaddr(msg['To'])
	try:
		mlist = MailingList.objects.get(listaddress__iexact=list_addr)
	except MailingList.DoesNotExist:
		print >>sys.stderr, 'Mailing list %s does not exist' % msg['To']
		return False

	swimmer_set = [ s.user.email for s in mlist.swimmers.all() ]
	newmsg = msg
	try:
		newmsg.replace_header('Reply-To', msg['From'])
	except KeyError:
		newmsg.add_header('Reply-To', msg['From'])
		
	""" Two things. 1. Check that the sender is on the list they are sending to. 2. Save a copy of the message """
	""" FIXME: I have a feeling that broken email clients are going to pass through mangled from headers """
	(realname, from_email) = rfc822.parseaddr(msg['From'])
	
	rfc_from = ''
	swimmer = None
	""" The reason for this check is that we want certain automatic scripts to be able to mail lists.  dev@ uses this """
	
	if from_email != list_addr:
		try:
			swimmer = Swimmer.objects.get(user__email__iexact=from_email)
		except Swimmer.DoesNotExist:
			print >>sys.stderr, 'didn\'t find swimmer with email address = %s' % from_email
			return False
		rfc_from = rfc822.dump_address_pair(('%s %s' %( swimmer.user.first_name, 
			swimmer.user.last_name), swimmer.user.email))
	else:
		rfc_from = rfc822.dump_address_pair(('', list_addr))
	
	body = ''
	if msg.is_multipart():
		for b in msg.get_payload():
			if b.get_content_type() == 'text/plain':
				body = b.get_payload()
				break
			elif b.get_content_type() == 'text/html':
				body = b.get_payload()
				stripper = Stripper()
				try:
					body = stripper.strip(body)
				except: #Sometimes the html is just a mess
					body = re.sub('<.*?>', '', body)
				break
	else:
		body = msg.get_payload()
	if swimmer != None:
		try:
			m = Message(fromswimmer=swimmer, tolist=mlist, message=body, subject=msg['Subject'])
			m.save()
		except:
			print >>sys.stderr, 'Message save failed on body = %s and subject = %s' %( body, msg['Subject'])
	
	s = smtplib.SMTP()
	s.connect(settings.OUTGOING_MAIL_HOST)

	failed_hash = {}

	try: 
		failed_hash = s.sendmail(rfc_from, swimmer_set, newmsg.as_string())
	except smtplib.SMTPRecipientsRefused, e:
		print >>sys.stderr, 'recipients refused %s' %e

	s.close()

	for k,v in failed_hash.items():
		print >>sys.stderr, '%s failed like %s' %( k, v )
	
	return True
def main():
	
	sleep_interval = 1*60 #poll the mail server every five minutes

	while True:
		mail_account = poplib.POP3(settings.REMOTE_MAIL_HOST)
		mail_account.user(settings.REMOTE_MAIL_USER)
		mail_account.pass_(settings.REMOTE_MAIL_PASS)
		mail_account.list()
		(msg_count, total_size) = mail_account.stat()
		print msg_count
		for i in range(1, msg_count + 1):
			(header, msg, octets) = mail_account.retr(i)
			print msg
			try:
				process_msg(msg)
			except Exception, e:
				print >>sys.stderr, 'Failed because %s on msg = %s' %(e, msg)
			mail_account.dele(i)
		
		mail_account.quit()
		time.sleep(sleep_interval)

if __name__ == '__main__':
	main()
