#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-level parts of pyptlib that are only useful to servers.
"""

import pyptlib.config as config
import pyptlib.util as util
import sys

from pyptlib.config import env_has_k, env_id

class ServerConfig(config.Config):
    """
    A client-side pyptlib configuration.

    :var tuple ORPort: (ip,port) pointing to Tor's ORPort.
    :var tuple extendedORPort: (ip,port) pointing to Tor's Extended ORPort. None if Extended ORPort is not supported.
    :var dict serverBindAddr: A dictionary {<transport> : [<addr>, <port>]}, where <transport> is the name of the transport that must be spawned, and [<addr>, <port>] is a list containing the location where that transport should bind. The dictionary can be empty.
    :var string authCookieFile: String representing the filesystem path where the Extended ORPort Authentication cookie is stored. None if Extended ORPort authentication is not supported.

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """
    def __init__(self, stdout=sys.stdout):
        """
        TOR_PT_EXTENDED_SERVER_PORT is optional; tor uses the empty
        string as its value if it does not support the Extended
        ORPort.
        """
        def empty_or_valid_addr(k, v):
            v = env_has_k(k, v)
            if v == '': return None
            return util.parse_addr_spec(v)

        self.extendedORPort = self.getEnv('TOR_PT_EXTENDED_SERVER_PORT', empty_or_valid_addr)

        # Check that either both Extended ORPort and the Extended
        # ORPort Authentication Cookie are present, or neither.
        if self.extendedORPort:
            def validate_authcookie(k, v):
                if v is None: raise ValueError("Extended ORPort address provided, but no cookie file.")
                return v
        else:
            def validate_authcookie(k, v):
                if v is not None: raise ValueError("Extended ORPort Authentication cookie file provided, but no Extended ORPort address.")
                return v
        self.authCookieFile = self.getEnv('TOR_PT_AUTH_COOKIE_FILE', validate_authcookie)

        # Get ORPort.
        self.ORPort = self.getEnv('TOR_PT_ORPORT', empty_or_valid_addr)

        # Get bind addresses.
        def validate_sever_bindaddr(k, bindaddrs):
            serverBindAddr = {}
            bindaddrs = env_has_k(k, bindaddrs).split(',')
            for bindaddr in bindaddrs:
                (transport_name, addrport) = bindaddr.split('-')
                (addr, port) = util.parse_addr_spec(addrport)
                serverBindAddr[transport_name] = (addr, port)
            return serverBindAddr
        self.serverBindAddr = self.getEnv('TOR_PT_SERVER_BINDADDR', validate_sever_bindaddr)

        # Get transports.
        def validate_transports(k, transports):
            transports = env_has_k(k, transports).split(',')
            t = sorted(transports)
            b = sorted(self.serverBindAddr.keys())
            if t != b:
                raise ValueError("Can't match transports with bind addresses (%s, %s)" % (t, b))
            return transports
        transports = self.getEnv('TOR_PT_SERVER_TRANSPORTS', validate_transports)

        config.Config.__init__(self, transports, stdout)

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
        try:
            return util.parse_addr_spec(string)
        except ValueError, err:
            self.writeEnvError(err)
            raise config.EnvError(err)

