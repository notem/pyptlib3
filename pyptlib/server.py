#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The pyptlib.easy.server module includes a convenient API for writing pluggable transport servers. """

from pyptlib.config import EnvException
from pyptlib.server_config import ServerConfig


def init(transports):
    """
    Initialize the pluggable transport by parsing the environment
    variables and generating output to report any errors.  The
    given transports are checked against the transports enabled by
    Tor and a dictionary containing information for the managed
    proxy is returned.

    The dictionary contains the following keys and values:

    'state_loc' : Directory where the managed proxy should dump its
    state files (if needed).

    'orport' : [<addr>, <port>] tuple containing the address and port
    of Tor's ORPort.

    'ext_orport' : [<addr>, <port>] tuple containing the address and
    port of Tor's Extended ORPort.

    'transports' : A dictionary {<transport> : [<addr>, <port>]},
    where <transport> is the name of the transport that must be
    spawned, and [<addr>, <port>] is a list containing the location
    where that transport should bind.

    Returns None if something went wrong.
    """

    supportedTransportVersion = '1'

    try:
        config = ServerConfig()
    except EnvException: # don't throw exceptions; return None
        return None

    if config.checkManagedTransportVersion(supportedTransportVersion):
        config.writeVersion(supportedTransportVersion)
    else:
        config.writeVersionError()
        return None

    matchedTransports = []
    for transport in transports:
        if config.checkTransportEnabled(transport):
            matchedTransports.append(transport)

    # XXX Must issue SMETHOD-ERROR when Tor asked us to spawn a
    # XXX transport but we don't support it!!!!

    # XXX what to do if matchedTransports is empty ???

    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['orport'] = config.getORPort()
    retval['ext_orport'] = config.getExtendedORPort()
    retval['transports'] = config.getServerBindAddresses()

    return retval

def reportSuccess(name, address, options):
    """
        This method should be called to report when a transport has been successfully launched.
        It generates output to Tor informing that the transport launched successfully and can be used.
        After all transports have been launched, the server should call reportEnd().
    """

    config = ServerConfig()
    config.writeMethod(name, address, options)


def reportFailure(name, message):
    """
        This method should be called to report when a transport has failed to launch.
        It generates output to Tor informing that the transport failed to launch and cannot be used.
        After all transports have been launched, the server should call reportEnd().
    """

    config = ServerConfig()
    config.writeMethodError(name, message)


def reportEnd():
    """
        This method should be called after all transports have been launched.
        It generates output to Tor informing that all transports have been launched.
    """

    config = ServerConfig()
    config.writeMethodEnd()
