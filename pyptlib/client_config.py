#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains parts of the API that are only useful to clients.
"""

from pyptlib.config import Config

class ClientConfig(Config):
    """
    Attributes:

    self.transports: List with strings of pluggable transport names
    that Tor wants us to handle.

    self.allTransportsEnabled: True if Tor wants us to spawn all the
    transports.
    """
    def __init__(self):
        """
        Initializer.
        Throws EnvError.
        """

        Config.__init__(self)

        self.transports = self.get('TOR_PT_CLIENT_TRANSPORTS').split(',')
        if '*' in self.transports:
            self.allTransportsEnabled = True
            self.transports.remove('*')

    def getClientTransports(self): # XXX why is this client-specific ???
        """
        Returns a list of strings representing the client transports
        reported by Tor. If present, '*' is stripped from this list
        and used to set allTransportsEnabled to True.
        """

        return self.transports

    def writeMethod(self, name, socksVersion, address, args, optArgs):
        """
        Write a message to stdout specifying a supported transport
        Takes: str, int, (str, int), [str], [str]
        """

        methodLine = 'CMETHOD %s socks%s %s:%s' % (name, socksVersion,
                address[0], address[1])
        if args and len(args) > 0:
            methodLine = methodLine + ' ARGS=' + args.join(',')
        if optArgs and len(optArgs) > 0:
            methodLine = methodLine + ' OPT-ARGS=' + args.join(',')
        self.emit(methodLine)

    def writeMethodError(self, name, message):  # CMETHOD-ERROR
        """
        Write a message to stdout specifying that an error occurred setting up the specified method
        Takes: str, str
        """

        self.emit('CMETHOD-ERROR %s %s' % (name, message))

    def writeMethodEnd(self):  # CMETHODS DONE
        """
        Write a message to stdout specifying that the list of
        supported transports has ended.
        """

        self.emit('CMETHODS DONE')


