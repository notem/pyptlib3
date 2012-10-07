API overview
============

Be sure to read :file:`API.rst` and :file:`glossary.rst` before
reading this file.

General Overview
################

Applications begin by initializing pyptlib.

Then pyptlib informs the application about which transports it should
spawn, in which ports they should listen for connections, etc.

Then the application launches the appropriate transports as
instructed, and for each transport it reports to pyptlib whether it
was launched successfully or not. Finally, the application announces
to pyptlib that it finished launching transports.

From that point and on the application should forget about pyptlib
and start accepting connections.

Detailed API Overview
#####################

0) Find if it's a client or a server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An application using pyptlib should start by calling
:func:`pyptlib.util.checkClientMode` to learn whether Tor wants it
to run as a client or as a server.

1) Get transport information from Tor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If Tor wants the application to run as a client, the next step is to
run :func:`pyptlib.client.init`. Otherwise, the application should run
:func:`pyptlib.server.init`.

:func:`init` expects to be passed a list with the names of the
transports your application supports.

The application should be prepared for
:exc:`pyptlib.config.EnvError`, which signifies that the
environment was not prepared by Tor.

The application should store the return value of the :func:`init`
function.

Consider an example of the fictional application *rot0r* which
implements the pluggable transports *rot13* and *rot26*. If
*rot0r*, in step 1, learned that Tor expects it to act as a client,
it should now do:

.. code-block::
   python

   import pyptlib.client
   import pyptlib.config

   try:
       managed_info = pyptlib.client.init(["rot13", "rot26"])
   except pyptlib.config.EnvError, err:
       print "pyptlib could not bootstrap ('%s')." % str(err)

2) Launch transports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Client case (skip if you are a server)
"""""""""""""""""""""""""""""""""""""""""""

If your application is a client, the return value of
:func:`pyptlib.client.init` is a dictionary of the format:

==========  ========== ==========
Key         Type       Value
==========  ========== ==========
state_loc   string     Directory where the managed proxy should dump its state files (if needed).
transports  list       Strings of the names of the transports that should be launched. The list can be empty.
==========  ========== ==========

Your application should then use the *transports* key to learn which transports it should launch.

Proceeding with the previous example:

.. code-block::
   python

   if 'rot13' in managed_info['transports']:
       launch_rot13_client()
   if 'rot26' in managed_info['transports']:
       launch_rot26_client()


.. note:: Since the application runs as a client, it should launch a
          SOCKS server in the upstream side of the proxy.

Server case (skip if you are a client):
""""""""""""""""""""""""""""""""""""""""""""

If your application is a server, the return value of
:func:`pyptlib.server.init` is a dictionary of the format:

==========  ========== ==========
Key         Type       Value
==========  ========== ==========
state_loc   string     Directory where the managed proxy should dump its state files (if needed).
orport      tuple      (ip,port) tuple pointing to Tor's ORPort.
ext_orport  tuple      (ip,port) tuple pointing to Tor's Extended ORPort. None if Extended ORPort is not supported.
transports  dict       A dictionary 'transport => (ip,port)' where 'transport' is the name of the transport that should be spawned, and '(ip,port)' is the location where the transport should bind. The dictionary can be empty.
==========  ========== ==========

Your application should then use the *transports* key and attempt to
launch the appropriate transports. Furthermore, since the application
runs as a server, it should push data to Tor's ORPort. The TCP/IP
location of the ORPort is provided in the *orport* key.

Proceeding with the previous example:

.. code-block::
   python

   if 'rot13' in managed_info['transports']:
       launch_rot13_server(managed_info['transports']['rot13'], managed_info['orport'])
   if 'rot26' in managed_info['transports']:
       launch_rot26_server(managed_info['transports']['rot26'], managed_info['orport'])

3) Report results back to Tor.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For every transport that the application launches, it reports to
pyptlib whether it was launched successfully or not. This way, Tor is
informed on whether a transport is expected to work or not.

Client case (skip if you are a server):
""""""""""""""""""""""""""""""""""""""""""""

Everytime a transport is successfully launched, the application calls
:func:`pyptlib.client.reportSuccess` with the name of the transport
that was launched, the address where it is listening for connections,
and the SOCKS version that the upstream SOCKS server supports.

For example, if *rot13* was launched successfully, waits for
connections in '127.0.0.1:42042' and supports SOCKSv4, the appropriate
call would be:

.. code-block::
   python

   pyptlib.client.reportSuccess('rot13', 5, ('127.0.0.1', 42042))

Everytime a transport failed to launch, the application calls
:func:`pyptlib.client.reportFailure` with the name of the transport
and a message.

For example, if *rot26* failed to launch, the appropriate call
would be:

.. code-block::
   python

   pyptlib.client.reportFailure('rot26', 'Could not bind to 127.0.0.1:666 (Operation not permitted)')

Server case (skip if you are a client):
""""""""""""""""""""""""""""""""""""""""""""

Everytime a transport is successfully launched, the application calls
:func:`pyptlib.server.reportSuccess` with the name of the transport
that was launched, and the address where it is listening for connections.

For example, if *rot13* was launched successfully and waits for
connections in '127.0.0.1:42042', the appropriate call would be:

.. code-block::
   python

   pyptlib.server.reportSuccess('rot13', ('127.0.0.1', 42042))

Everytime a transport failed to launch, the application calls
:func:`pyptlib.server.reportFailure` with the name of the transport
and a message.

For example, if *rot26* failed to launch, the appropriate call
would be:

.. code-block::
   python

   pyptlib.server.reportFailure('rot26', 'Could not bind to 127.0.0.1:666 (Operation not permitted)')

4) Stop using pyptlib and start accepting connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the application finishes launching connections, it should call
:func:`pyptlib.client.reportEnd` (or
:func:`pyptlib.server.reportEnd`), to announce to pyptlib that all
transports were launched. This way, Tor knows that it can start
pushing traffic to the application.

After this point, pyptlib has no other use.
