#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Public server-side pyptlib API.
"""

from pyptlib.config import EnvError
from pyptlib.server_config import ServerConfig


def init(supported_transports):
    """
    Bootstrap server-side managed-proxy mode.

    *Call in the beginning of your application.*

    :param list supported_transports: Names of the transports that the application supports.

    :returns: dictionary that contains information for the application:

	    ===============   ========== ==========
	    Key               Type       Value
	    ================  ========== ==========
	    state_loc         string     Directory where the managed proxy should dump its state files (if needed).
	    orport            tuple      (ip,port) tuple pointing to Tor's ORPort.
	    ext_orport        tuple      (ip,port) tuple pointing to Tor's Extended ORPort. None if Extended ORPort is not supported.
	    transports        dict       A dictionary 'transport => (ip,port)' where 'transport' is the name of the transport that should be spawned, and '(ip,port)' is the location where the transport should bind. The dictionary can be empty.
            auth_cookie_file  string     Directory where the managed proxy should find the Extended ORPort authentication cookie.
	    ================  ========== ==========

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """
    config = ServerConfig()
    wanted = config.declareSupports(supported_transports)
    transports = dict(((k, v) for k, v in config.getServerBindAddresses().items()
                              if k in wanted['transports']))
    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['orport'] = config.getORPort()
    retval['ext_orport'] = config.getExtendedORPort()
    retval['transports'] = transports
    retval['auth_cookie_file'] = config.getAuthCookieFile()

    return retval

def reportSuccess(name, addrport, options):
    """
    Report that a server transport was launched succesfully.

    *Always call after successfully launching a transport.*

    :param str name: Name of transport.
    :param tuple addrport: (addr,port) where this transport is listening for connections.
    :param str options: Transport options.
    """

    config = ServerConfig()
    config.writeMethod(name, addrport, options)


def reportFailure(name, message):
    """
    Report that a server transport failed to launch.

    *Always call after failing to launch a transport.*

    :param str name: Name of transport.
    :param str message: Error message.
    """

    config = ServerConfig()
    config.writeMethodError(name, message)


def reportEnd():
    """
    Report that we are done launching transports.

    *Call after you have launched all the transports you could launch.*
    """

    config = ServerConfig()
    config.writeMethodEnd()
