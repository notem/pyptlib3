#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parts of pyptlib that are useful both to clients and servers.
"""

import os, sys

SUPPORTED_TRANSPORT_VERSIONS = ['1']

def env_has_k(k, v):
    """
    A validator for Config.getEnv that returns the value of the envvar if it
    was found, or throws ValueError if it was not.
    """
    if v is None: raise ValueError('Missing environment variable %s' % k)
    return v

def env_id(k, v):
    """
    A validator for Config.getEnv that returns the value of the envvar if it
    was found, or None if it was not.
    """
    return v

class Config(object):
    """
    pyptlib's configuration.

    :var string stateLocation: Location where application should store state.
    :var list managedTransportVer: List of managed-proxy protocol versions that Tor supports.
    :var list transports: Strings of pluggable transport names that Tor wants us to handle.
    :var bool allTransportsEnabled: True if Tor wants us to spawn all the transports.

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """

    def __init__(self, stateLocation, managedTransportVer, transports,
                 stdout=sys.stdout):
        self.stateLocation = stateLocation
        self.managedTransportVer = managedTransportVer
        self.allTransportsEnabled = False
        if '*' in transports:
            self.allTransportsEnabled = True
            transports.remove('*')
        self.transports = transports
        self.stdout = stdout

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

    def getAllTransportsEnabled(self):
        """
        Check if Tor wants the application to spawn all its transpotrs.

        :returns: bool -- True if Tor wants the application to spawn all its transports.
        """

        return self.allTransportsEnabled

    def declareSupports(self, transports):
        """
        Declare to Tor the versions and transports that this PT supports.

        :param list transports: List of transport methods this PT supports.

        :returns: {"transports": wanted_transports} -- The subset of the
            declared inputs that were actually wanted by Tor.
        """
        versions = SUPPORTED_TRANSPORT_VERSIONS
        if type(transports) == str:
            transports = [transports]

        wanted_versions = [v for v in versions if v in self.managedTransportVer]
        if not wanted_versions:
            self.emit('VERSION-ERROR no-version')
            raise EnvError("Unsupported managed proxy protocol version (%s)" %
                           self.managedTransportVer)
        else:
            self.emit('VERSION %s' % wanted_versions[0])

        if self.allTransportsEnabled:
            wanted_transports = transports.keys()
            unwanted_transports = []
        else:
            # return able in priority-order determined by plugin
            wanted_transports = [t for t in transports if t in self.transports]
            # return unable in priority-order as requested by Tor
            unwanted_transports = [t for t in self.transports if t not in transports]

        for t in unwanted_transports:
            self.writeMethodError(t, 'unsupported transport')

        return { 'transports': wanted_transports }

    def writeMethodError(self, transportName, message):
        raise NotImplementedError

    def emit(self, msg):
        """
        Announce a message.

        :param str msg: A message.
        """

        print >>self.stdout, msg
        self.stdout.flush()

    @classmethod
    def getEnv(cls, key, validate=env_has_k):
        """
        Get the value of an environment variable.

        :param str key: Environment variable key.
        :param f validate: Function that takes a var and a value and returns
            a transformed value if it is valid, or throws an exception.
            If the environment does not define var, value is None. By default,
            we return the value if the environment has the variable, otherwise
            we raise a ValueError.

        :returns: str -- The value of the envrionment variable.

        :raises: :class:`pyptlib.config.EnvError` if environment
        variable could not be found.
        """
        try:
            return validate(key, os.getenv(key))
        except Exception, e:
            message = 'ENV-ERROR %s' % e.message
            print message
            sys.stdout.flush()
            raise EnvError(message)


class EnvError(Exception):
    """
    Thrown when the environment is incomplete or corrupted.
    """
    pass

def checkClientMode():
    """
    Read the environment and return true if we are supposed to be a
    client. Return false if we are supposed to be a server.

    Raise EnvError if the environment was not properly set up.
    """
    if 'TOR_PT_CLIENT_TRANSPORTS' in os.environ: return True
    if 'TOR_PT_SERVER_TRANSPORTS' in os.environ: return False
    raise EnvError('neither TOR_PT_{SERVER,CLIENT}_TRANSPORTS set')
