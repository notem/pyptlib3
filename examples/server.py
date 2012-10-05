#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This is a server-side example of the pyptlib API."""

import sys

import pyptlib
import pyptlib.server

if __name__ == '__main__':
    try:
        managed_info = pyptlib.server.init(["blackfish", "bluefish"])
    except pyptlib.config.EnvError, err:
        print "pyptlib could not bootstrap ('%s')." % str(err)
        sys.exit(1)

    for transport, transport_bindaddr in managed_info['transports'].items():
        # Try to spawn transports and make them listen in the ports
        # that Tor wants. Report failure or success appropriately.

        # 'transport' is a string with the name of the transport.
        # 'transport_bindaddr' is the (<ip>,<port>) where that
        # transport should listen for connections.

        try:
            bind_addrport = your_function_that_launches_transports(transport, transport_bindaddr)
        except YourFailException, err:
            reportFailure(transport, "Failed to launch ('%s')." % str(err))
            continue

        pyptlib.server.reportSuccess(transport, bind_addrport, None)

    # Report back after we finish spawning transports.
    pyptlib.server.reportEnd()
