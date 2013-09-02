#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Public server-side pyptlib API.
"""

from pyptlib.core import TransportPlugin
from pyptlib.server_config import ServerConfig


class ServerTransportPlugin(TransportPlugin):
    """
    Runtime process for a server TransportPlugin.
    """
    configType = ServerConfig
    methodName = 'SMETHOD'

    def reportMethodSuccess(self, name, addrport, options):
        """
        Write a message to stdout announcing that a server transport was
        successfully launched.

        :param str name: Name of transport.
        :param tuple addrport: (addr,port) where this transport is listening for connections.
        :param str options: Transport options.
        """

        if options:
            self.emit('SMETHOD %s %s:%s %s' % (name, addrport[0],
                      addrport[1], options))
        else:
            self.emit('SMETHOD %s %s:%s' % (name, addrport[0],
                      addrport[1]))

    def getBindAddresses(self):
        """
        :returns: dict of names of the transports that this plugin can serve,
            each mapped to the (ip,port) where the transport should bind.
        :raises: :class:`ValueError` if called before :func:`init`.
        """
        return dict((k, v)
                    for k, v in self.config.serverBindAddr.iteritems()
                    if k in self.getTransports())


def init(supported_transports):
    """DEPRECATED. Use ServerTransportPlugin().init() instead."""
    server = ServerTransportPlugin()
    server.init(supported_transports)
    config = server.config
    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['orport'] = config.getORPort()
    retval['ext_orport'] = config.getExtendedORPort()
    retval['transports'] = server.getBindAddresses()
    retval['auth_cookie_file'] = config.getAuthCookieFile()

    return retval

def reportSuccess(name, addrport, options):
    """DEPRECATED. Use ClientTransportPlugin().reportMethodSuccess() instead."""
    config = ServerTransportPlugin()
    config.reportMethodSuccess(name, addrport, options)


def reportFailure(name, message):
    """DEPRECATED. Use ClientTransportPlugin().reportMethodError() instead."""
    config = ServerTransportPlugin()
    config.reportMethodError(name, message)


def reportEnd():
    """DEPRECATED. Use ClientTransportPlugin().reportMethodsEnd() instead."""
    config = ServerTransportPlugin()
    config.reportMethodsEnd()
