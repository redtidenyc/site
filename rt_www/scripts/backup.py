from django.conf import settings
from rt_www.backups.models import Backup, DB, SVN
from optparse import OptionParser
import MySQLdb, datetime, subprocess, bz2, sys, bitbucket, os

def sync_dir(bucket_name, path):
	bucket = bitbucket.BitBucket(bucket_name, access_key='0Z9ZYHJQKNASPMD5W6R2', secret_key='japrNLqnUHlwa43efYmO5TIWsDc52sLEtM8zghmd')
	for root, dirs, files in os.walk(path):
		for file in files:
			fullpath = os.path.join(root, file)
			try:
				if bucket.has_key(fullpath):
					bits = bucket[fullpath]
					bits.filename = fullpath
				else:
					bits = bitbucket.Bits(filename=fullpath)
					bucket[fullpath] = bits
			except bitbucket.BitBucketEmptyError:
				print 'sync_dir: Empty File - Ignored %s' % fullpath
		full_paths = [ os.path.join(root, f) for f in files ]
		for file in bucket.keys():
			if file not in full_paths:
				del bucket[file]
				
	return bucket

def make_backup(cmd, outfile, compress, btype):
	file = None
	if compress:
		outfile += '.bz2'
		file = bz2.BZ2File(outfile, 'w')
	else:
		file = open(outfile, 'wb')
	pipe_stdout = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()[0]
	file.write(pipe_stdout)
	file.close()
	save_backup(outfile, btype)

def save_backup(outfile, btype):
	try:
		backup = Backup.objects.get(file__exact=outfile)
		backup.date_taken = datetime.datetime.now()
		backup.save()
	except Backup.DoesNotExist:
		backup = Backup(file=outfile, type=btype)
		backup.save()

def backup_file(infile, outfile, compress, btype):
	file = None
	if compress:
		outfile += '.bz2'
		file = bz2.BZ2File(outfile, 'w')
	else:
		file = open(outfile, 'wb')
	fp = open(infile, 'rb')
	file.write(fp.read())
	file.close()	
	save_backup(outfile, btype)

def main():
	usage = 'usage: %prog [options] arg'
	parser = OptionParser()
	parser.add_option('-o', '--output', dest='outfile', help='The output file for the backup')
	parser.add_option('-d', '--db', action='store_true', dest='backupdb', help='backup the production database')
	parser.add_option('-c', '--compress', action='store_true', dest='compress', help='compress the backup')
	parser.add_option('-s', '--svn', action='store_true', dest='backupsvn', help='backup the subversion repository')
	parser.add_option('-l', '--limit', dest='retainlimit', help='The number of previous backups to keep, defaults to 5')
	limit, outputdir, compress, backupsvn, backupdb = 5, settings.BACKUPDIR, False, False, True
	btype = DB
	
	(options, args) = parser.parse_args()
	if options.backupsvn:
		backupsvn, backupdb = True, False
		btype = SVN
	if options.compress:
		compress = True
	if options.outfile:
		outfile = outputdir + '/' + options.outfile
	else:
		if backupsvn:
			outfile = outputdir + '/svn_%s.dump' % datetime.datetime.now().strftime('%Y-%m-%d')
		else:
			outfile = outputdir + '/db_%s.dump' % datetime.datetime.now().strftime('%Y-%m-%d')
	if options.retainlimit:
		limit = int(options.retainlimit)

	if backupdb:
		backup_file(settings.DATABASE_NAME, outfile, compress, btype)
	else:
		svnadmin = '/usr/bin/svnadmin dump %s ' % settings.SVNREPOS
		make_backup(svnadmin, outfile, compress, btype)
	
	todel = Backup.objects.filter(type__exact=btype).order_by('-date_taken')
	for i, d in enumerate(todel):
		if i > limit:
			d.delete()
	sync_dir('rt_backup', outputdir)

if __name__ == '__main__':
	main()
