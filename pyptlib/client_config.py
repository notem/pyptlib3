#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-level parts of pyptlib that are only useful to clients.
"""

import sys

from pyptlib.config import Config

class ClientConfig(Config):
    """
    A client-side pyptlib configuration.
    """

    @classmethod
    def fromEnv(cls):
        """
        Build a ClientConfig from environment variables.

        :raises: :class:`pyptlib.config.EnvError` if environment was incomplete or corrupted.
        """
        return cls(
            stateLocation = cls.getEnv('TOR_PT_STATE_LOCATION'),
            managedTransportVer = cls.getEnv('TOR_PT_MANAGED_TRANSPORT_VER').split(','),
            transports = cls.getEnv('TOR_PT_CLIENT_TRANSPORTS').split(','),
            )
