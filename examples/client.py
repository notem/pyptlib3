#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This is an example client which shows how to call the pyptlib.easy high-level API. """

from pyptlib.client import init, reportSuccess, reportFailure, \
    reportEnd


class TransportLaunchException(Exception):

    pass


def launchClient(self, name, port):
    if name != 'dummy':
        raise TransportLaunchException('Tried to launch unsupported transport %s'
                 % name)


if __name__ == '__main__':
    supportedTransports = ['dummy', 'rot13']

    managed_info = init(supportedTransports)
    if managed_info is None:
        print "Failed!"
        return

    for transport in managed_info['transports']:
        try:
            launchClient(transport, 8182)
            reportSuccess(transport, 5, ('127.0.0.1', 8182), None, None)
        except TransportLaunchException:
            reportFailure(transport, 'Failed to launch')
    reportEnd()
