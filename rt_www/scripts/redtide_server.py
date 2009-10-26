#!/usr/bin/env python

"""
	This is a little mail server.  It manages forwards and mail to the mailing lists.  This
rids us of our dependancy on our providers mail system.  Which is a plus in my book.

	start like twistd -l - -ny scripts/redtide_server.py
"""

from zope.interface import implements
from twisted.internet import defer, error, reactor, threads
from twisted.python import failure
from twisted.mail import smtp, relaymanager
from twisted.names import client

from twisted.application import internet, service
from rt_www.mailinglist.models import MailingList, RTMessage, Forward
from rt_www.swimmers.models import Swimmer, BoardMember
from rt_www.siteutils import Stripper
import dns.resolver, sys, time, email, re, rfc822, smtplib, socket, threading, datetime, Queue

def handleFailure(e):
	print >>sys.stderr, 'exception %s trapped' % e.getTraceback()
	e.trap(Exception)

def get_local_ips():
	return socket.gethostbyname_ex(socket.gethostname())[2] + [ '127.0.0.1' ]

def msg_parse(env_from, msg):
	msg_parsed = email.message_from_string(msg)
	(env_to_name, env_to_addr) = rfc822.parseaddr(msg_parsed['To'])
	return env_from, env_to_addr, msg

class Sender:
	RETRANS_TIMES = ([60] * 5 + [60 * 5] * 5 + [60 * 30] * 3 + [60 * 60 * 2] * 2 + [60 * 60 * 6] * 19)	
	def __init__(self, env_from, env_to, msg):
		self.from_addr = env_from
		self.to_addr = env_to
		self.msg = msg
		self.mx_list = []
	def getMailExchange(self, recipientDomain):
		resolver = client.Resolver(servers=[('127.0.0.1', 53)])
		mxc = relaymanager.MXCalculator(resolver)
		d = mxc.getMX(recipientDomain)
		def gotMX(mx):
			print 'Got mx'
			resolver.protocol.transport.stopListening()
			return mx
		d.addCallback(gotMX)
		return d
	def _mailSent(self, ignored):
		print >>sys.stderr, 'successful send to %s' % self.to_addr
		return 'Success'
	def _failureSending(self, err):
		t = err.trap(smtp.SMTPDeliveryError, error.DNSLookupError)
		if t is smtp.SMTPDeliveryError:
			code = err.value.code
			log = err.value.log
		        print >>sys.stderr, 'Failed on smtp error code = %s, log = %s for %s' % ( code, log, self.to_addr)
			if 500 <= code < 600:
				print >>sys.stderr, 'Failed on smtp error for %s' % self.to_addr
		elif t is error.DNSLookupError:
			pass
		return 'Failed'
	def _sendMail(self, mx):
		host = str(mx.name)
		#return True
		return smtp.sendmail(host, self.from_addr, [self.to_addr], self.msg)
	def sendmail(self):
		domain = ''
		try:
			domain = self.to_addr.split('@')[1]
		except:
			print >>sys.stderr, 'malformed email %s' % self.to_addr
			return
		
		return self.getMailExchange(domain).addCallback(self._sendMail
			).addCallback(self._mailSent
			).addErrback(self._failureSending)
	
def save_list_message(lines, mailinglist):
	msg = email.message_from_string('\n'.join(lines))
	(listname, list_addr) = rfc822.parseaddr(msg['To'])
	""" This is fairly simple in here. validate, save, and look up mx record and
	then use the smtp.send() method 
	"""
	print 'mailinglist: %s to: %s' % ( mailinglist, msg['To'])
	try:
		swimmer_set = [ s.user.email for s in mailinglist.swimmers.all() ]
	except:
		raise Exception('oops failed to send on null mailing list %s ' % msg['To'] ) 
		
	newmsg = msg
	try:
		newmsg.replace_header('Reply-To', msg['From'])
	except KeyError:
		newmsg.add_header('Reply-To', msg['From'])

		
	""" Two things. 1. Check that the sender is on the list they are sending to. 2. Save a copy of the message """
	""" FIXME: I have a feeling that broken email clients are going to pass through mangled from headers """
	(realname, from_email) = rfc822.parseaddr(msg['From'])
        
	swimmer = None
	""" The reason for this check is that we want certain automatic scripts to be able to mail lists.  dev@ uses this """
	
	if from_email != mailinglist.listaddress:
                """ Okay so we set the FROM header to the mailing list and make sure the env_from matches it"""
                newmsg.replace_header('From', mailinglist.listaddress)
                """ First thing we check is whether only board members can post.  If so throw the
                message out if the from isn't a board member"""
                if mailinglist.board_postable_only:
                    try:
                        bm = BoardMember.objects.get(swimmer__email__iexact=from_email)
                    except BoardMember.DoesNotExist:
                        raise Exception('Only board members can post to this list %s' % from_email)
		try:
			swimmer = Swimmer.objects.get(user__email__iexact=from_email)
		except Swimmer.DoesNotExist:
			raise Exception('didn\'t find swimmer with email address = %s' % from_email)
	
        env_from = list_addr
	
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
			m = RTMessage.objects.create(fromswimmer=swimmer, tolist=mailinglist, message=unicode(body, 'utf-8'), subject=msg['Subject'])
		except Exception, e:
			print >>sys.stderr, 'Message save failed like %s on body = %s and subject = %s' %( e, body, msg['Subject'])
	return ( env_from, swimmer_set, newmsg.as_string(), ) 

class RedtideMessageDelivery:
	implements(smtp.IMessageDelivery)
   	
	local_ips = get_local_ips()
	 
	def receivedHeader(self, helo, origin, recipients):
		return ""

	def validateFrom(self, helo, origin):
		# All addresses are accepted
		return defer.succeed(origin)
    
	def validateTo(self, user):
		# Only messages directed to either a valid forward or a mailinglist are
		# accepted
		ip = user.protocol.transport.getPeer()[1]
		addr = None
		try:
			addr = MailingList.objects.get(listaddress__iexact='%s' % user.dest)
			print >>sys.stderr, 'list addr: %s' % (addr)
			return lambda: ListMessage(user, addr)
		except MailingList.DoesNotExist:
			pass
		try:
			addr = Forward.objects.get(forward__iexact='%s' % user.dest )
			print >>sys.stderr, 'forward addr: %s' % (addr)
			return lambda: ForwardMessage(user, addr)
		except Forward.DoesNotExist:
			pass
		if ip in self.local_ips:
			return lambda: LocalMessage(user)
		 
		raise smtp.SMTPBadRcpt(user)
			
class ListMessage:
	implements(smtp.IMessage)
    
	def __init__(self, sender, listobj):
		self.sender = sender
		self.mailinglist = listobj
		self.lines = []

	def lineReceived(self, line):
		self.lines.append(line)

	def eomReceived(self): #At this point the logic goes in
		""" send out here """
		env_from = self.sender.dest.local + '@' + self.sender.dest.domain
		self.sender.protocol.factory.queue_append(Message(env_from, self.lines, self.mailinglist))
		return defer.succeed(None)

	def connectionLost(self):
		# There was an error, throw away the stored lines
		self.lines = None

class ForwardMessage:
	implements(smtp.IMessage)
    
	def __init__(self, sender, forwardobj):
		self.sender = sender
		self.forward = forwardobj
		self.lines = []

	def lineReceived(self, line):
		self.lines.append(line)

	def eomReceived(self): #At this point the logic goes in
		msg = '\n'.join(self.lines)
		env_from = self.sender.dest.local + '@' + self.sender.dest.domain
		""" send out here 
		(self, fromaddr, to, msg)	
		"""
		self.sender.protocol.factory.queue_append(Message( env_from, msg, self.forward.swimmer.user.email ))
		return defer.succeed(None)

	def connectionLost(self):
		# There was an error, throw away the stored lines
		self.lines = None

class LocalMessage:
	implements(smtp.IMessage)
	
	def __init__(self, sender):
		self.sender = sender
		self.lines = []
	def lineReceived(self, line):
		self.lines.append(line)
	def eomReceived(self):
		msg = '\n'.join(self.lines)
		env_from = self.sender.dest.local + '@' + self.sender.dest.domain
		env_from, to_addr, msg = msg_parse(env_from, msg)
		self.sender.protocol.factory.queue_append(Message(env_from, msg, to_addr))
		return defer.succeed(None)


class RSMTP(smtp.SMTP):
	host = 'mail.redtidenyc.org'
	def greeting(self):
		return '%s says howdy by the request of her majesty El Presidente' % self.host

class Message:
	def __init__(self, env_from, msg, env_to):
		self.env_from, self.env_to, self.msg = env_from, env_to, msg
		self.ml = False
		if not isinstance(env_to, basestring):
			self.ml = True
	def get(self):
		if self.ml:
			return save_list_message(self.msg, self.env_to)
		else:
			return self.env_from, [ self.env_to ], self.msg
 		
	

class RedtideSMTPFactory(smtp.SMTPFactory):
	protocol = RSMTP
	domain = 'redtidenyc.org'
	def __init__(self, *a, **kw):
		smtp.SMTPFactory.__init__(self, *a, **kw)
		self.delivery = RedtideMessageDelivery()
		self.queue = []
		l = internet.task.LoopingCall(self.sendMessage)
		l.start(1.0)
	def queue_append(self, msg):
		self.queue.append(msg)
	def sendMessage(self):
		while len(self.queue) > 0:
			message = self.queue.pop()
			try:
				env_from, env_tos, msg = message.get()
			except Exception, e:
				print >>sys.stderr, 'caught exception %s' % e
				continue
			for env_to in env_tos:
				s = Sender(env_from, env_to, msg)
				d = s.sendmail()
			
	def buildProtocol(self, addr):
		p = smtp.SMTPFactory.buildProtocol(self, addr)
		p.delivery = self.delivery
		return p

def main():
	app = service.Application("Redtide SMTP Server")
	internet.TCPServer(25, RedtideSMTPFactory()).setServiceParent(app)
	return app

application = main()
