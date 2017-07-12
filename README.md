# spacewalk-api-errata
To get errata information and last packages were uploaded to the spacewalk server

 Usage: usage apierrata.py [option]
========================================

What is this script for?

This script get errata and package by date from api. 
Only get information from main channel.



    Usage 
   -------


<pre>

Options:
     -h, --help            show this help message and exit
     --disable=CHANNEL_DISABLE
                        Do not see errara for channel label.[ centos7|epel7 ]
     --no-packages         
                        Disable list of packeges
     --hours=HOURS         
                        Set period of time in hours
     --minutes=MINUTES     
                        Set period of time in minutes
     -p PASSWORD, --password=PASSWORD
                        Set user password
     -u USERNAME, --user=USERNAME
                        Set user name
<pre>

