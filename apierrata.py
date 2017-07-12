#!/usr/bin/env python

import xmlrpclib, time, getpass,sys,smtplib
from datetime import datetime, timedelta
from optparse import OptionParser


def getChannelLabel():
 	getchannel = client.channel.listAllChannels(session)
 	ChannelLabel =  [] 
	for key in getchannel:
		if not key['label'].startswith(('dev','prod','temp')):
			ChannelLabel.append(key['label'])
	return ChannelLabel
	
	

def getErrata(DateTime,channel_disable):
	datachannel = getChannelLabel()
	for channelLabel in datachannel:
		if not channelLabel.startwith(channel_disable):
			listErrata = client.channel.software.listErrata(session, channelLabel,DateTime.isoformat())
			for key in listErrata:
				yield key

def getLastDownloadPackages(DateTime):
	datachannel = getChannelLabel()
	if datachannel is not None:
		for value in datachannel:
			channelLabel = value 
			PackagesByDate = client.channel.software.listAllPackagesByDate(session, channelLabel, DateTime.isoformat())
			for lists in PackagesByDate:
			 	yield lists


def main(options):
	
	hours, minutes = (options.hours,options.minutes)
	DateTime = datetime.now() - timedelta(hours=hours,minutes=minutes)	
	print DateTime
	lineformat = '{0:<50s} {1:<10s} {2:<30s} {3:<10s}'
	
	#Chacked last errata
	geterrata  = getErrata(DateTime,options.channel_disable)
	
	for keys in geterrata:
		#print keys['advisory'],keys['synopsis'],keys['advisory_type'],keys['issue_date']
		name = keys['advisory']
		errat = client.errata.getDetails(session, name)

		if keys['advisory'].startswith(('C')):
			print lineformat.format(keys['advisory'], errat['issue_date'], errat['synopsis'], errat['references'])
			print '\n Description: {0:10s}\n'.format(errat['description'])
			print  '-' * 120
		
		else:
			print lineformat.format(keys['advisory'], errat['issue_date'], errat['synopsis'],errat['topic']) 
			print '\n Description: {0:10s}\n'.format(errat['description'].encode('utf-8'))
			print '-' * 120
	
    #Get last packages were downloaded.
	if not options.flag_packages:
		getlist = getLastDownloadPackages(DateTime)
		print lineformat.format('Package Name','Version','Release', 'Last_modified')
		print lineformat.format('------------','-------','-------', '--------------')

		for key in getlist:
			print lineformat.format(key['name'],key['version'],key['release'],key['last_modified'])		


if __name__ == "__main__":

	usage = "usage %prog [option]"
	parser = OptionParser(usage=usage)
	parser.add_option("--disable", dest="channel_disable",default='None',
		help="Do not see errara for channel label.[ centos7|epel7 ]")
	parser.add_option('--no-packages', action='store_true',dest='flag_packages',default=False,
		help='Disable list of packeges')
	parser.add_option('--hours',type='int',dest='hours',
		help="Set period of time in hours",default='24')
	parser.add_option('--minutes',type='int',dest='minutes',
		help="Set period of time in minutes", default='00')
	parser.add_option('-p','--password',dest='password',default='None',
		help='Set user password')
	parser.add_option('-u', '--user', dest='username',default='None',
		help='Set user name')

	options, args = parser.parse_args()

	if not (options.username and options.password):
		parser.print_help()
		parser.error("Must provide a username and password to content to spacewalk api")
	else:
	
		URL = 'http://localhost/rpc/api'
		client = xmlrpclib.Server(URL, verbose=0)
		session = client.auth.login(options.username,options.password)

		main(options)
