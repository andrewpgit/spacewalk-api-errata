#!/usr/bin/env python

import xmlrpclib, time, getpass,sys,smtplib
from datetime import datetime, timedelta
from optparse import OptionParser

URL = 'http://serverip or name/rpc/api'
USERNAME = 'spaceadmin'
PASSWORD = 'some password'
client = xmlrpclib.Server(URL, verbose=0)
session = client.auth.login(USERNAME, PASSWORD)



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
		if channel_disable not in channelLabel:
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


def main(hours,minutes,channel_disable,flag_packages):
	
	
	hours, minutes = (options.hours,options.minutes)
	DateTime = datetime.now() - timedelta(hours=hours,minutes=minutes)	
	print DateTime
	lineformat = '{0:<50s} {1:<10s} {2:<30s} {3:<10s}'
	
	

#Chacked last errata
	print channel_disable
	geterrata  = getErrata(DateTime,channel_disable)
	

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
	if not flag_packages:
		getlist = getLastDownloadPackages(DateTime)
		print lineformat.format('Package Name','Version','Release', 'Last_modified')
		print lineformat.format('------------','-------','-------', '--------------')

		for key in getlist:
			print lineformat.format(key['name'],key['version'],key['release'],key['last_modified'])		


if __name__ == "__main__":

	usage = "usage %prog[option]"
	parser = OptionParser(usage=usage)
	parser.add_option("--disable", dest="channel_disable",default='None',
		help="Do not see errara for channel label.[ centos7|epel7 ]")
	parser.add_option('--no-packages', action='store_true',dest='flag_packages',default=False,
		help='Disable list of packeges')
	parser.add_option('--hours',type='int',dest='hours',
		help="Set period of time in hours",default='24')
	parser.add_option('--minutes',type='int',dest='minutes',
		help="Set period of time in minutes", default='00')
	options, args = parser.parse_args()
	
	main(options.hours,options.minutes,options.channel_disable,options.flag_packages)
