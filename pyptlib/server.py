#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The pyptlib.easy.server module includes a convenient API for writing pluggable transport servers. """

from pyptlib.config import EnvError
from pyptlib.server_config import ServerConfig


def init(supported_transports):
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
    port of Tor's Extended ORPort, or None if the Extended ORPort it's
    not supported.

    'transports' : A dictionary {<transport> : [<addr>, <port>]},
    where <transport> is the name of the transport that must be
    spawned, and [<addr>, <port>] is a list containing the location
    where that transport should bind. The dictionary can be empty.

    Throws EnvError.
    """

    supportedTransportVersion = '1'

    config = ServerConfig()

    if config.checkManagedTransportVersion(supportedTransportVersion):
        config.writeVersion(supportedTransportVersion)
    else:
        config.writeVersionError()
        raise EnvError("Unsupported managed proxy protocol version (%s)" %
                           str(config.getManagedTransportVersions()))

    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['orport'] = config.getORPort()
    retval['ext_orport'] = config.getExtendedORPort()
    retval['transports'] = getTransportsDict(supported_transports, config)

    return retval

def getTransportsDict(supported_transports, config):
    """
    Given the transport names that the managed proxy support in
    'transports', and Tor's configuration in 'config', figure out
    which transports Tor wants us to spawn and create the appropriate
    dictionary.
    """
    transports = {}

    if config.getAllTransportsEnabled():
        return config.getServerBindAddresses()

    for transport in config.getServerTransports():
        if transport in supported_transports:
            assert(transport in config.getServerBindAddresses())
            transports[transport] = config.getServerBindAddresses()[transport]
        else:
            # Issue SMETHOD-ERROR when Tor asks us to spawn a
            # transport that we do not support.
            config.writeMethodError(transport, "not supported")

    return transports

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
