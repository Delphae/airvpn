#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function


#    ____       _       _
#   |  _ \  ___| |_ __ | |__   __ _  ___
#   | | | |/ _ \ | '_ \| '_ \ / _` |/ _ \
#   | |_| |  __/ | |_) | | | | (_| |  __/
#   |____/ \___|_| .__/|_| |_|\__,_|\___|
#                |_|


MAXROWS = 40
#DEVICE  = 'nuc'

__version__ = '3.12'
__date__ = '2019-01-19'


'''
TODO


'''

import sys, urllib2, json
import socket
from AirPy import Airvpn
from datetime import timedelta
from datetime import datetime as dt

def listservers(servers):
    #serversort = sorted(servers, key=lambda x:int(x.currentload), reverse=False)
    serversort = sorted(servers, key=lambda x:x.public_name, reverse=False)
    print ('%2s %-12s %s %3s %3s   %-18s %-18s' % ('#', 'server', 'flag', 'load', 'user', 'ip' ,'ip-alt'))
    for k, server in enumerate(serversort[:MAXROWS]):
        print ('%2d %-14s %2s  %3d %4d   %-18s %-18s' %
               (k+1,
                server.public_name,
                server.country_code,
                int(server.currentload),
                int(server.users),
                server.ip_entry,
                server.ip_entry_alt
                )
               )
    print ('%2d Count' % len(servers))

#%%
def myip():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open('http://ifconfig.co/ip')
    ipv4 = response.read()[:-1]
    return ipv4
#%%
def session2json(session):
    sessiondict = dict(timestamp=dt.now().strftime('%Y-%m-%d %H:%M:%S'),
                  device=session.device_name,
                  server=session.server_name,
                  ipv4=session.exit_ipv4,
                  ipv6=session.exit_ipv6)
    jsdata = json.dumps(sessiondict)
    f = open('ipaddresslog.json', 'a')
    f.write('%s\n' % jsdata)
    f.close()
    return


#%%
def usersummary(air, ipaddress):
    if air.user.connected:
        for k, session in enumerate(sorted(air.sessions, key=lambda ses:ses.device_name, reverse=False)):
            session2json(session)
            if session.device_name==socket.gethostname():
                marker='*'
            else:
                marker=''

#            print ('%-19s %1d%s' % ('Session', k+1, marker))
            print ('%-19s %s%s' % ('Device', session.device_name, marker))
            print ('%-19s %s' % ('Server', session.server_name))

            print ('%-19s %s' % ('IPv4', session.exit_ipv4))
            print ('%-19s %s' % ('IPv6', session.exit_ipv6))
            print ('%-19s %9.3f MB' % ('Read', int(session.bytes_read)/1024.0/1024.0))
            print ('%-19s %9.3f MB' % ('Write', int(session.bytes_write)/1024.0/1024.0))
            cettime = session.connected + timedelta(hours=1)
            print ('%-19s %s CET' % ('Connected since', cettime))
            uptime = dt.now()-cettime
            hours = uptime.seconds // 3600
            minutes = uptime.seconds % 3600 // 60
            print ('%-19s days=%s, hrs=%s, min=%s' % ('uptime',
                                                      uptime.days,
                                                      hours,
                                                      minutes))
            print ('%-19s %s, %s' % ('Location', session.server_location,
                                                 session.server_country_code.upper()))
            print ()
    return

def nodesummary(air, ipv4):
    if air.user.connected:
        for session in air.sessions:
            if session.device_name==socket.gethostname():
                print (session.server_name)
    else:
        print('not connected')
    return


if __name__ == '__main__':
    count   = '-c' in sys.argv
    report  = '-r' in sys.argv
    user    = '-u' in sys.argv
    node    = '-n' in sys.argv

    apikey = open('airapikey.txt').read()
    air = Airvpn(apikey, 'NL')
    ipv4 = myip()

    if count:
        print (len(air.servers()))
    elif report:
        listservers(air.servers())
    elif user:
        usersummary(air, ipv4)
    elif node:
        nodesummary(air, ipv4)
