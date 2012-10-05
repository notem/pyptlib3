import os
import unittest

import pyptlib
import pyptlib.client

class testClient(unittest.TestCase):
    def test_legit_environment(self):
        """Legit environment"""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        pyptlib.client.init(["dummy"])

    def test_bad_environment(self):
        """Missing TOR_PT_MANAGED_TRANSPORT_VER."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.client.init, ["dummy"])

    def test_bad_environment_2(self):
        """Missing TOR_PT_CLIENT_TRANSPORTS."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.client.init, ["dummy"])

    def test_unknown_transports(self):
        """Unknown transports"""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "are,you,a,badfish,too?" }

        os.environ = TEST_ENVIRON
        retval = pyptlib.client.init(["dummy"])
        self.assertEqual(len(retval['transports']), 0)

    def test_bad_protocol_version(self):
        """Unsupported managed-proxy configuration protocol version."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "666",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.client.init, ["dummy"])

if __name__ == '__main__':
    unittest.main()

