#!/usr/bin/env python
# coding: utf-8

#    ____       _       _
#   |  _ \  ___| |_ __ | |__   __ _  ___
#   | | | |/ _ \ | '_ \| '_ \ / _` |/ _ \
#   | |_| |  __/ | |_) | | | | (_| |  __/
#   |____/ \___|_| .__/|_| |_|\__,_|\___|
#                |_|

import urllib2
import json
import random
from datetime import datetime as dt

__version__ = '1.4'
__date__ = '2018-11-13'

class Airvpn():
    '''
    A Python wrapper around the AirVPN API.
    API documentation: https://airvpn.org/faq/api/
    You can generate your API key at the client area
    
    API calls:
    https://airvpn.org/api/?format=json&key=<your_api_key>&service=userinfo
    https://airvpn.org/api/?format=json&key=<your_api_key>&service=status

    Example:
        from AirPy import Airvpn
        APIKEY = "7de2aa122b7a42b9882d2f5b1e8ff30168ca6468"
        air = Airvpn(APIKEY,'nl')  # when you are located in the Netherlands
        air = Airvpn(APIKEY,'gb')  # when you are located in the UK, and so on

    Example (Basic request):
        print (air.user)
        print (air.user.connected)
        print (air.user.login)

        print (air.connection)
        print (air.connection.server_name)

        print (air.sessions[0])

        print (servers = air.servers())
        for server in servers:
            print (server)

        print (air.best())
        print (air.rand())
    '''

    def __init__ (self, apikey, country):
        self.apikey  = apikey
        self.country = country.upper()

        userinfo        = readapi('userinfo', self.apikey)
        self.user       = User(userinfo['user'])
        if self.user.connected:
            self.connection = Connection(userinfo['connection'])
            self.sessions   = [Session(session) for session in userinfo['sessions']]
        return

    def servers(self):
        jsdata = readapi('status', self.apikey)
        serverlist = [Server(item) for item in jsdata['servers']]
        return [server for server in serverlist if server.country_code==self.country.lower()]

    def best(self):
        serverssort = sorted(self.servers(), key=lambda k: k.currentload)
        return serverssort[0]

    def rand(self):
        return random.choice(self.servers())

def readapi(service, apikey):
    url = "https://airvpn.org/api/?service=%s&format=json&key=%s" % (service, apikey)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request, timeout=5)
    jsdata = json.load(response)
    return jsdata


class Server():
    def __init__(self, serverdict):
        self.__dict__ = serverdict
        return

    def __repr__(self):
        return self.public_name

    def __str__(self):
        return '%s ,%s, %s, %s, %s, %s' %\
               (self.public_name, self.location,
                self.country_code, self.ip_entry,
                self.currentload, self.users)

    def __eq__ (self, other):
        return self.public_name==other.public_name


class Connection():
    def __init__ (self, connection):
        self.__dict__ = connection
    def __repr__ (self):
        return self.server_name
    def __str__ (self):
        return ('%s, %s UTC' % (self.server_name, self.connected_since_date))


class User():
    def __init__ (self, user):
        self.__dict__ = user
        self.last = dt.fromtimestamp(float(self.last_activity_unix))
    def __repr__ (self):
        return str(self.login)
    def __str__ (self):
        return ('%s, %s' % (self.login, self.last))


class Session():
    def __init__ (self, session):
        self.__dict__ = session
    def __repr__ (self):
        return self.server_name
    def __str__ (self):
        return ('%s, %s, %s') % (self.server_name, self.exit_ip, self.connected_since_date)

