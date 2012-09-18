#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module inherits from pyptlib.config and contains just the parts
of the API which are specific to the server implementations of the
protocol.
"""

import os

import pyptlib.config as config

__docformat__ = 'restructuredtext'

class ServerConfig(config.Config):
    """
    This class inherits from pyptlib.config.Config and contains just
    the parts of the API which are specific to the client
    implementations of the protocol.
    """
  # Public methods

    def __init__(self):
        """
        Initialize the ClientConfig object.
        This causes the state location, managed transport, and transports version to be set.

        Throws EnvException.
        """

        config.Config.__init__(self)

        # TOR_PT_EXTENDED_SERVER_PORT is optional; tor uses the empty
        # string as its value if it does not support the Extended
        # ORPort.
        ext_orport_tmp = self.get('TOR_PT_EXTENDED_SERVER_PORT')
        if ext_orport_tmp == '':
            self.extendedORPort = None
        else:
            self.extendedORPort = self.get_addrport('TOR_PT_EXTENDED_SERVER_PORT')

        self.ORPort = self.get_addrport('TOR_PT_ORPORT')

        self.serverBindAddr = {}
        bindaddrs = self.get('TOR_PT_SERVER_BINDADDR').split(',')
        for bind in bindaddrs:
            (key, value) = bind.split('-')
            self.serverBindAddr[key] = value.split(":") # XXX ugly code
            self.serverBindAddr[key][1] = int(self.serverBindAddr[key][1]) # XXX ugly code

        self.transports = self.get('TOR_PT_SERVER_TRANSPORTS').split(',')
        if '*' in self.transports:
            self.allTransportsEnabled = True
            self.transports.remove('*')

    def getExtendedORPort(self):
        """ Returns a tuple (str,int) representing the address of the Tor server port as reported by Tor """

        return self.extendedORPort

    def getORPort(self):
        """ Returns a tuple (str,int) representing the address of the Tor OR port as reported by Tor """

        return self.ORPort

    def getServerBindAddresses(self):
        """ Returns a dict {str: (str,int)} representing the addresses for each transport as reported by Tor """

        return self.serverBindAddr

    def getServerTransports(self):
        """
        Returns a list of strings representing the server
        transports reported by Tor. If present, '*' is stripped from
        this list and used to set allTransportsEnabled to True.
        """

        return self.transports

    def writeMethod(self, name, address, options):
        """
        Write a message to stdout specifying a supported transport
        Takes: str, (str, int), MethodOptions
        """

        if options:
            self.emit('SMETHOD %s %s:%s %s' % (name, address[0],
                      address[1], options))
        else:
            self.emit('SMETHOD %s %s:%s' % (name, address[0],
                      address[1]))

    def writeMethodError(self, name, message):  # SMETHOD-ERROR
        """
            Write a message to stdout specifying that an error occurred setting up the specified method
            Takes: str, str
        """

        self.emit('SMETHOD-ERROR %s %s' % (name, message))

    def writeMethodEnd(self):  # SMETHODS DONE
        """ Write a message to stdout specifying that the list of supported transports has ended """

        self.emit('SMETHODS DONE')

    def get_addrport(self, key):
        """
        Given an environment variable name in 'key' with an
        '<addr>:<port>' value, return [<addr>,<port>].

        Throws EnvException.
        """
        string = self.get(key)

        addrport = string.split(':')

        if (len(addrport) != 2) or (not addrport[1].isdigit()):
            message = '%s: Parsing error (%s).' % (key, string)
            self.writeEnvError(message)
            raise config.EnvException(message)

        if (not 0 <= int(addrport[1]) < 65536):
            message = '%s: Port out of range (%s).' % (key, string)
            self.writeEnvError(message)
            raise config.EnvException(message)

        return addrport

class MethodOptions:

    """ The MethodOptions class represents the method options: FORWARD, ARGS, DECLARE, and USE-EXTENDED-PORT. """

    forward = False  # FORWARD
    args = {}  # ARGS
    declare = {}  # DECLARE
    useExtendedPort = False  # USE-EXTENDED-PORT

  # Public methods

    def setForward(self):
        """ Sets forward to True """

        self.forward = True

    def addArg(self, key, value):
        """ Adds a key-value pair to args """

        self.args[key] = value

    def addDeclare(self, key, value):
        """ Adds a key-value pair to declare """

        self.declare[key] = value

    def setUserExtendedPort(self):
        """ Sets useExtendedPort to True """

        self.useExtendedPort = True

    def __str__(self):
        """ Returns a string representation of the method options. """

        options = []
        if self.forward:
            options.append('FORWARD:1')
        if len(self.args) > 0:
            argstr = 'ARGS:'
            for key in self.args:
                value = self.args[key]
                argstr = argstr + key + '=' + value + ','
            argstr = argstr[:-1]  # Remove trailing comma
            options.append(argstr)
        if len(self.declare) > 0:
            decs = 'DECLARE:'
            for key in self.declare:
                value = self.declare[key]
                decs = decs + key + '=' + value + ','
            decs = decs[:-1]  # Remove trailing comma
            options.append(decs)
        if self.useExtendedPort:
            options.append('USE-EXTENDED-PORT:1')

        return ' '.join(options)


