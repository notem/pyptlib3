#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This is an example server which shows how to call the pyptlib.easy high-level API. """

from pyptlib.easy.server import init, reportSuccess, reportFailure, \
    reportEnd


class TransportLaunchException(Exception):

    pass


def launchServer(self, name, port):
    if name != 'dummy':
        raise TransportLaunchException('Tried to launch unsupported transport %s'
                 % name)


if __name__ == '__main__':
    supportedTransports = ['dummy', 'rot13']

    managed_info = init(supportedTransports)
    if managed_info is None:
        print "Failed!"
        return

    for transport, transport_bindaddr in managed_info['transports'].items():
        try:
            launchServer(transport, transport_bindaddr[1])
            reportSuccess(transport, transport_bindaddr, None)
        except TransportLaunchException:
            reportFailure(transport, 'Failed to launch')
    reportEnd()
