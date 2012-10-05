#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains parts of the API that are only useful to servers.
"""

import pyptlib.config as config

class ServerConfig(config.Config):
    """
    Attributes:

    self.transports: List with strings of pluggable transport names
    that Tor wants us to handle.

    self.allTransportsEnabled: True if Tor wants us to spawn all the
    transports.

    self.extendedORPort: '(<ip>,<port>)' tuple pointing to Tor's
    Extended ORPort. 'None' if Extended ORPort is not supported.

    self.serverBindAddr: A dictionary {<transport> : [<addr>, <port>]},
    where <transport> is the name of the transport that must be
    spawned, and [<addr>, <port>] is a list containing the location
    where that transport should bind. The dictionary can be empty.
    """
    def __init__(self):
        """
        Initializer.
        Throws EnvError.
        """

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

        # Get ORPort.
        self.ORPort = self.get_addrport('TOR_PT_ORPORT')

        # Get bind addresses.
        self.serverBindAddr = {}
        bindaddrs = self.get('TOR_PT_SERVER_BINDADDR').split(',')
        for bindaddr in bindaddrs:
            (transport_name, addrport) = bindaddr.split('-')
            (addr, port) = get_addrport_from_string(addrport)
            self.serverBindAddr[key] = (addr, port)

        # Get transports.
        self.transports = self.get('TOR_PT_SERVER_TRANSPORTS').split(',')
        if '*' in self.transports:
            self.allTransportsEnabled = True
            self.transports.remove('*')

    def getExtendedORPort(self):
        return self.extendedORPort

    def getORPort(self):
        return self.ORPort

    def getServerBindAddresses(self):
        return self.serverBindAddr

    def getServerTransports(self):
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

        Throws EnvError.
        """
        string = self.get(key)
        return self.get_addrport_from_string(string)

    def get_addrport_from_string(self, string):
        """
        Given a string in 'string' with an '<addr>:<port>' value,
        return [<addr>,<port>].

        Throws EnvError.
        """

        addrport = string.split(':')

        if (len(addrport) != 2) or (not addrport[1].isdigit()):
            message = 'Parsing error (%s).' % (string)
            self.writeEnvError(message)
            raise config.EnvError(message)

        if (not 0 <= int(addrport[1]) < 65536):
            message = 'Port out of range (%s).' % (string)
            self.writeEnvError(message)
            raise config.EnvError(message)

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


