#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The pyptlib.util module contains useful functions that don't fit in anywhere else. """

from pyptlib.config import Config, EnvError


def checkClientMode():
    """ Checks to see if the daemon has been launched in client mode or server mode. Returns True if it is in client mode, otherwise False. """

    try:
        c = Config()
        return c.checkClientMode()
    except EnvError:
        return False


