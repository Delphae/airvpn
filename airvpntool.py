#!/usr/bin/env python
# coding: utf-8

#    ____       _       _
#   |  _ \  ___| |_ __ | |__   __ _  ___
#   | | | |/ _ \ | '_ \| '_ \ / _` |/ _ \
#   | |_| |  __/ | |_) | | | | (_| |  __/
#   |____/ \___|_| .__/|_| |_|\__,_|\___|
#                |_|


MAXROWS = 40

__version__ = '3.6'
__date__ = '2018-11-18'

import sys, random

from AirPy import Airvpn
from hostanalyse import read_speedtestlog

def listservers(servers):
    serversort = sorted(servers, key=lambda x:int(x.currentload), reverse=False)
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


def usersummary():
    print ('%-19s %s' % ('Login', air.user.login))
    print ('%-19s %s' % ('Connected', air.user.connected))
    if air.user.connected:
        for k, session in enumerate(air.sessions):
            print
            print ('%-19s %1d' % ('Session', k+1))
            print ('%-19s %s' % ('Server', session.server_name))
            print ('%-19s %s' % ('Entry ip', session.entry_ip))
            print ('%-19s %s' % ('Exit ip', session.exit_ip))
            print ('%-19s %9.3f MB' % ('Read', int(session.bytes_read)/1024.0/1024.0))
            print ('%-19s %9.3f MB' % ('Write', int(session.bytes_write)/1024.0/1024.0))
            print ('%-19s %s UTC' % ('Connected since', session.connected_since_date))
            print ('%-19s %s' % ('Last activity', air.user.last))
            print ('%-19s %s, %s' % ('Location', session.server_location,
                                                 session.server_country_code.upper()))

def lowest(servers):
    speedlog = read_speedtestlog()
    speednodes = [speedtest.node for speedtest in speedlog]
    
    counts = [(server, speednodes.count(server.public_name)) for server in servers]
    countmin = min([count[1] for count in counts])
    candidates = [count[0] for count in counts if count[1]==countmin]
    return random.choice(candidates)


if __name__ == '__main__':
    verbose = '-v' in sys.argv
    rand    = '-r' in sys.argv
    count   = '-c' in sys.argv
    report  = '-r' in sys.argv
    user    = '-u' in sys.argv
    node    = '-n' in sys.argv
    low     = '-l' in sys.argv

    apikey = open('airapikey.txt').read()
    air = Airvpn(apikey, 'NL')

    if rand:
        txt = 'random' if verbose else ''
        server = air.rand()
    elif low:
        txt = 'lowest' if verbose else ''
        server = lowest(air.servers())
    else:
        txt = 'best' if verbose else ''
        server = air.best()

    if verbose:
        print ('%-10s %s' % ('Select',txt))
        print ('%-10s %s' % ('Server',server.public_name))
        print ('%-10s %s' % ('Load',server.currentload))
        print ('%-10s %s' % ('Users',server.users))
        print ('%-10s %s' % ('IP',server.ip_entry))
        print ('%-10s %s' % ('IP_alt',server.ip_entry_alt))
        print ('%-10s %s' % ('Country',server.country_code))
    elif count:
        print (len(air.servers()))
    elif report:
        listservers(air.servers())
    elif user:
        usersummary()
    elif node:
        if air.user.connected:
            print (air.connection.server_name)
        else:
            print('not connected')
    else:
        print (server.public_name)
