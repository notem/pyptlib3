#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This is a client-side example of the pyptlib API."""

import sys

import pyptlib
import pyptlib.client

if __name__ == '__main__':
    try:
        managed_info = pyptlib.client.init(["blackfish", "bluefish"])
    except pyptlib.config.EnvError, err:
        print "pyptlib could not bootstrap ('%s')." % str(err)
        sys.exit(1)

    for transport in managed_info['transports']:
        # Spawn all the transports in the list, and for each spawned
        # transport report back the port where it is listening, and
        # the SOCKS version it supports.

        try:
            socks_version, bind_addrport = your_function_that_launches_transports(transport)
        except YourFailException, err:
            reportFailure(transport, "Failed to launch ('%s')." % str(err))
            continue

        pyptlib.client.reportSuccess(transport, socks_version, bind_addrport, None, None)

    # After spawning our transports, report that we are done.
    pyptlib.client.reportEnd()
