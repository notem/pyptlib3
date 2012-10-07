#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parts of pyptlib that are useful both to clients and servers.
"""

import os, sys

class Config(object):
    """
    pyptlib's configuration.

    :var string stateLocation: Location where application should store state.
    :var list managedTransportVer: List of managed-proxy protocol versions that Tor supports.
    :var list transports: Strings of pluggable transport names that Tor wants us to handle.
    :var bool allTransportsEnabled: True if Tor wants us to spawn all the transports.

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """

    stateLocation = None  # TOR_PT_STATE_LOCATION
    managedTransportVer = []  # TOR_PT_MANAGED_TRANSPORT_VER
    transports = []  # TOR_PT_SERVER_TRANSPORTS or TOR_PT_CLIENT_TRANSPORTS
    allTransportsEnabled = False

    def __init__(self):
        self.stateLocation = self.get('TOR_PT_STATE_LOCATION')
        self.managedTransportVer = self.get('TOR_PT_MANAGED_TRANSPORT_VER').split(',')

    def checkClientMode(self):
        """
        Check whether Tor wants us to run as a client or as a server.

        :returns: bool -- True if Tor wants us to run as a client.
        """

        return self.check('TOR_PT_CLIENT_TRANSPORTS')

    def getStateLocation(self):
        """
        :returns: string -- The state location.
        """

        return self.stateLocation

    def getManagedTransportVersions(self):
        """
        :returns: list -- The managed-proxy protocol versions that Tor supports.
        """

        return self.managedTransportVer

    def checkManagedTransportVersion(self, version):
        """
        Check if Tor supports a specific managed-proxy protocol version.

        :param string version: A managed-proxy protocol version.

        :returns: bool -- True if version is supported.
        """

        return version in self.managedTransportVer

    def getAllTransportsEnabled(self):
        """
        Check if Tor wants the application to spawn all its transpotrs.

        :returns: bool -- True if Tor wants the application to spawn all its transports.
        """

        return self.allTransportsEnabled

    def checkTransportEnabled(self, transport):
        """
        Check if Tor wants the application to spawn a specific transport.

        :param string transport: The name of a pluggable transport.

        :returns: bool -- True if Tor wants the application to spawn that transport.
        """

        return self.allTransportsEnabled or transport in self.transports

    def writeEnvError(self, message):  # ENV-ERROR
        """
        Announce that an error occured while parsing the environment.

        :param str message: Error message.
        """

        self.emit('ENV-ERROR %s' % message)

    def writeVersion(self, version):  # VERSION
        """
        Announce that a specific managed-proxy protocol version is supported.

        :param str version: A managed-proxy protocol version.
        """

        self.emit('VERSION %s' % version)

    def writeVersionError(self):  # VERSION-ERROR
        """
        Announce that we could not find a supported managed-proxy
        protocol version.
        """

        self.emit('VERSION-ERROR no-version')

    def check(self, key):
        """
        Check the environment for a specific environment variable.

        :param str key: Environment variable key.

        :returns: bool -- True if the environment variable is set.
        """

        return key in os.environ

    def get(self, key):
        """
        Get the value of an environment variable.

        :param str key: Environment variable key.

        :returns: str -- The value of the envrionment variable.

        :raises: :class:`pyptlib.config.EnvError` if environment
        variable could not be found.
        """

        if key in os.environ:
            return os.environ[key]
        else:
            message = 'Missing environment variable %s' % key
            self.writeEnvError(message)
            raise EnvError(message)

    def emit(self, msg):
        """
        Announce a message.

        :param str msg: A message.
        """

        print msg
        sys.stdout.flush()

class EnvError(Exception):
    """
    Thrown when the environment is incomplete or corrupted.
    """
    pass
