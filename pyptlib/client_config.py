#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-level parts of pyptlib that are only useful to clients.
"""

from pyptlib.config import Config

class ClientConfig(Config):
    """
    A client-side pyptlib configuration.

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """
    def __init__(self):
        Config.__init__(self)

        self.transports = self.get('TOR_PT_CLIENT_TRANSPORTS').split(',')
        if '*' in self.transports:
            self.allTransportsEnabled = True
            self.transports.remove('*')

    def getClientTransports(self): # XXX why is this client-specific ???
        """
        Return a list of strings representing the client transports reported by Tor.

        If present, the wildcard transport, '*', is stripped from this list and used to set allTransportsEnabled to True.

        :returns: list of transports
        """

        return self.transports

    def writeMethod(self, name, socksVersion, addrport, args=None, optArgs=None):
        """
        Write a message to stdout announcing that a transport was
        successfully launched.

        :param str name: Name of transport.
        :param int socksVersion: The SOCKS protocol version.
        :param tuple addrport: (addr,port) where this transport is listening for connections.
        :param str args: ARGS field for this transport.
        :param str optArgs: OPT-ARGS field for this transport.
        """

        methodLine = 'CMETHOD %s socks%s %s:%s' % (name, socksVersion,
                addrport[0], addrport[1])
        if args and len(args) > 0:
            methodLine = methodLine + ' ARGS=' + args.join(',')
        if optArgs and len(optArgs) > 0:
            methodLine = methodLine + ' OPT-ARGS=' + args.join(',')
        self.emit(methodLine)

    def writeMethodError(self, name, message):
        """
        Write a message to stdout announcing that we failed to launch a transport.

        :param str name: Name of transport.
        :param str message: Error message.
        """

        self.emit('CMETHOD-ERROR %s %s' % (name, message))

    def writeMethodEnd(self):
        """
        Write a message to stdout announcing that we finished launching transports..
        """

        self.emit('CMETHODS DONE')


