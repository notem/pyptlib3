#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Utility functions.
"""

from pyptlib.config import Config, EnvError

def checkClientMode(): # XXX WTF!???! This also exists in config.py.
    """
    Check whether Tor wants us to run as a client or as a server.

    :returns: bool -- True if Tor wants us to run as a client.
    """
    try:
        c = Config()
        return c.checkClientMode()
    except EnvError:
        return False


