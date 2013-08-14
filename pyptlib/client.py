#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Public client-side pyptlib API.
"""

from pyptlib.config import EnvError
from pyptlib.client_config import ClientConfig


def init(supported_transports):
    """
    Bootstrap client-side managed-proxy mode.

    *Call in the beginning of your application.*

    :param list supported_transports: Names of the transports that the application supports.

    :returns: dictionary that contains information for the application.

	    ==========  ========== ==========
	    Key         Type       Value
	    ==========  ========== ==========
	    state_loc   string     Directory where the managed proxy should dump its state files (if needed).
	    transports  list       Strings of the names of the transports that should be launched. The list can be empty.
	    ==========  ========== ==========

    :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
    """
    config = ClientConfig()

    wanted = config.declareSupports(supported_transports)
    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['transports'] = wanted['transports']

    return retval

def reportSuccess(name, socksVersion, addrport, args=None, optArgs=None):
    """
    Report that a client transport was launched succesfully.

    *Always call after successfully launching a transport.*

    :param str name: Name of transport.
    :param int socksVersion: The SOCKS protocol version.
    :param tuple addrport: (addr,port) where this transport is listening for connections.
    :param str args: ARGS field for this transport.
    :param str args: OPT-ARGS field for this transport.
    """

    config = ClientConfig()
    config.writeMethod(name, socksVersion, addrport, args, optArgs)


def reportFailure(name, message):
    """
    Report that a client transport failed to launch.

    *Always call after failing to launch a transport.*

    :param str name: Name of transport.
    :param str message: Error message.
    """

    config = ClientConfig()
    config.writeMethodError(name, message)


def reportEnd():
    """
    Report that we are done launching transports.

    *Call after you have launched all the transports you could launch.*
    """

    config = ClientConfig()
    config.writeMethodEnd()
