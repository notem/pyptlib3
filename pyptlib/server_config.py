#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-level parts of pyptlib that are only useful to servers.
"""

import pyptlib.config as config

class ServerConfig(config.Config):
    """
    A client-side pyptlib configuration.

    :var tuple ORPort: (ip,port) pointing to Tor's ORPort.
    :var tuple extendedORPort: (ip,port) pointing to Tor's Extended ORPort. None if Extended ORPort is not supported.
    :var dict serverBindAddr: A dictionary {<transport> : [<addr>, <port>]}, where <transport> is the name of the transport that must be spawned, and [<addr>, <port>] is a list containing the location where that transport should bind. The dictionary can be empty.
    :var string authCookieFile: String representing the filesystem path where the Extended ORPort Authentication cookie is stored. None if Extended ORPort authentication is not supported.

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """
    def __init__(self):
        config.Config.__init__(self)

        """
        TOR_PT_EXTENDED_SERVER_PORT is optional; tor uses the empty
        string as its value if it does not support the Extended
        ORPort.
        """
        ext_orport_tmp = self.get('TOR_PT_EXTENDED_SERVER_PORT')
        if ext_orport_tmp == '':
            self.extendedORPort = None
        else:
            self.extendedORPort = self.get_addrport('TOR_PT_EXTENDED_SERVER_PORT')

        if self.check('TOR_PT_AUTH_COOKIE_FILE'):
            self.authCookieFile = self.get('TOR_PT_AUTH_COOKIE_FILE')
        else:
            self.authCookieFile = None

        # Check that either both Extended ORPort and the Extended
        # ORPort Authentication Cookie are present, or neither.
        if self.extendedORPort and not self.authCookieFile:
            err = "Extended ORPort address provided, but no cookie file."
            self.writeEnvError(err)
            raise config.EnvError(err)
        elif self.authCookieFile and not self.extendedORPort:
            err = "Extended ORPort Authentication cookie file provided, but no Extended ORPort address."
            self.writeEnvError(err)
            raise config.EnvError(err)

        # Get ORPort.
        self.ORPort = self.get_addrport('TOR_PT_ORPORT')

        # Get bind addresses.
        self.serverBindAddr = {}
        bindaddrs = self.get('TOR_PT_SERVER_BINDADDR').split(',')
        for bindaddr in bindaddrs:
            (transport_name, addrport) = bindaddr.split('-')
            (addr, port) = self.get_addrport_from_string(addrport)
            self.serverBindAddr[transport_name] = (addr, port)

        # Get transports.
        self.transports = self.get('TOR_PT_SERVER_TRANSPORTS').split(',')
        if '*' in self.transports:
            self.allTransportsEnabled = True
            self.transports.remove('*')

        if sorted(self.transports) != sorted(self.serverBindAddr.keys()):
            err = "Can't match transports with bind addresses (%s, %s)" % (self.transports, self.serverBindAddr.keys())
            self.writeEnvError(err)
            raise config.EnvError(err)

    def getExtendedORPort(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.extendedORPort`
        """
        return self.extendedORPort

    def getORPort(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.ORPort`
        """
        return self.ORPort

    def getServerBindAddresses(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.serverBindAddr`
        """
        return self.serverBindAddr

    def getServerTransports(self):
        """
        :returns: :attr:`pyptlib.config.Config.transports`
        """
        return self.transports

    def getAuthCookieFile(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.authCookieFile`
        """
        return self.authCookieFile

    def writeMethod(self, name, addrport, options):
        """
        Write a message to stdout announcing that a server transport was
        successfully launched.

        :param str name: Name of transport.
        :param tuple addrport: (addr,port) where this transport is listening for connections.
        :param str options: Transport options.
        """

        if options:
            self.emit('SMETHOD %s %s:%s %s' % (name, addrport[0],
                      addrport[1], options))
        else:
            self.emit('SMETHOD %s %s:%s' % (name, addrport[0],
                      addrport[1]))

    def writeMethodError(self, name, message):  # SMETHOD-ERROR
        """
        Write a message to stdout announcing that we failed to launch
        a transport.

        :param str name: Name of transport.
        :param str message: Error message.
        """

        self.emit('SMETHOD-ERROR %s %s' % (name, message))

    def writeMethodEnd(self):  # SMETHODS DONE
        """
        Write a message to stdout announcing that we finished
        launching transports..
        """

        self.emit('SMETHODS DONE')

    def get_addrport(self, key):
        """
        Parse an environment variable holding an address:port value.

        :param str key: Environment variable key.

        :returns: tuple -- (address,port)

        :raises: :class:`pyptlib.config.EnvError` if string was not in address:port format.
        """

        string = self.get(key)
        return self.get_addrport_from_string(string)

    def get_addrport_from_string(self, string):
        """
        Parse a string holding an address:port value.

        :param str string: A string.

        :returns: tuple -- (address,port)

        :raises: :class:`pyptlib.config.EnvError` if string was not in address:port format.
        """

        addrport = string.split(':')

        if (len(addrport) != 2) or (not addrport[1].isdigit()):
            message = 'Parsing error (%s).' % (string)
            self.writeEnvError(message)
            raise config.EnvError(message) # XXX maybe return ValueError

        if (not 0 <= int(addrport[1]) < 65536):
            message = 'Port out of range (%s).' % (string)
            self.writeEnvError(message)
            raise config.EnvError(message)

        return addrport

