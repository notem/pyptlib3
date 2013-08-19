#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-level parts of pyptlib that are only useful to servers.
"""

import pyptlib.config as config
import pyptlib.util as util
import sys

from pyptlib.config import env_has_k, env_id, get_env, SUPPORTED_TRANSPORT_VERSIONS

class ServerConfig(config.Config):
    """
    A client-side pyptlib configuration.

    :var tuple ORPort: (ip,port) pointing to Tor's ORPort.
    :var tuple extendedORPort: (ip,port) pointing to Tor's Extended ORPort. None if Extended ORPort is not supported.
    :var dict serverBindAddr: A dictionary {<transport> : [<addr>, <port>]}, where <transport> is the name of the transport that must be spawned, and [<addr>, <port>] is a list containing the location where that transport should bind. The dictionary can be empty.
    :var string authCookieFile: String representing the filesystem path where the Extended ORPort Authentication cookie is stored. None if Extended ORPort authentication is not supported.
    """

    @classmethod
    def fromEnv(cls):
        """
        Build a ServerConfig from environment variables.

        :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
        """

        # TOR_PT_EXTENDED_SERVER_PORT is optional; tor uses the empty
        # string as its value if it does not support the Extended
        # ORPort.
        def empty_or_valid_addr(k, v):
            v = env_has_k(k, v)
            if v == '': return None
            return util.parse_addr_spec(v)

        extendedORPort = get_env('TOR_PT_EXTENDED_SERVER_PORT', empty_or_valid_addr)

        # Check that either both Extended ORPort and the Extended
        # ORPort Authentication Cookie are present, or neither.
        if extendedORPort:
            def validate_authcookie(k, v):
                if v is None: raise ValueError("Extended ORPort address provided, but no cookie file.")
                return v
        else:
            def validate_authcookie(k, v):
                if v is not None: raise ValueError("Extended ORPort Authentication cookie file provided, but no Extended ORPort address.")
                return v
        authCookieFile = get_env('TOR_PT_AUTH_COOKIE_FILE', validate_authcookie)

        # Get ORPort.
        ORPort = get_env('TOR_PT_ORPORT', empty_or_valid_addr)

        # Get bind addresses.
        def validate_server_bindaddr(k, bindaddrs):
            serverBindAddr = {}
            bindaddrs = env_has_k(k, bindaddrs).split(',')
            for bindaddr in bindaddrs:
                (transport_name, addrport) = bindaddr.split('-')
                (addr, port) = util.parse_addr_spec(addrport)
                serverBindAddr[transport_name] = (addr, port)
            return serverBindAddr
        serverBindAddr = get_env('TOR_PT_SERVER_BINDADDR', validate_server_bindaddr)

        # Get transports.
        def validate_transports(k, transports):
            transports = env_has_k(k, transports).split(',')
            t = sorted(transports)
            b = sorted(serverBindAddr.keys())
            if t != b:
                raise ValueError("Can't match transports with bind addresses (%s, %s)" % (t, b))
            return transports
        transports = get_env('TOR_PT_SERVER_TRANSPORTS', validate_transports)

        return cls(
            stateLocation = get_env('TOR_PT_STATE_LOCATION'),
            managedTransportVer = get_env('TOR_PT_MANAGED_TRANSPORT_VER').split(','),
            transports = transports,
            serverBindAddr = serverBindAddr,
            ORPort = ORPort,
            extendedORPort = extendedORPort,
            authCookieFile = authCookieFile
            )

    def __init__(self, stateLocation,
                 managedTransportVer=SUPPORTED_TRANSPORT_VERSIONS,
                 transports=[],
                 serverBindAddr={},
                 ORPort=None,
                 extendedORPort=None,
                 authCookieFile=None):
        config.Config.__init__(self,
            stateLocation, managedTransportVer, transports)
        self.serverBindAddr = serverBindAddr
        self.ORPort = ORPort
        self.extendedORPort = extendedORPort
        self.authCookieFile = authCookieFile

    def getExtendedORPort(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.extendedORPort`
        """
        return self.extendedORPort

    def getORPort(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.ORPort`
        """
        return self.ORPort

    def getServerBindAddresses(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.serverBindAddr`
        """
        return self.serverBindAddr

    def getServerTransports(self):
        """
        :returns: :attr:`pyptlib.config.Config.transports`
        """
        return self.transports

    def getAuthCookieFile(self):
        """
        :returns: :attr:`pyptlib.server_config.ServerConfig.authCookieFile`
        """
        return self.authCookieFile
