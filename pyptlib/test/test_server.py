import os
import unittest

import pyptlib
import pyptlib.server

class testServer(unittest.TestCase):
    def test_legit_environment(self):
        """Legit environment."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        pyptlib.server.init(["dummy"])

    def test_bad_environment(self):
        """Missing TOR_PT_MANAGED_TRANSPORT_VER."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_2(self):
        """Missing TOR_PT_ORPORT."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_3(self):
        """Missing TOR_PT_EXTENDED_SERVER_PORT."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_4(self):
        """TOR_PT_EXTENDED_SERVER_PORT not an addport."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "cakez",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_5(self):
        """TOR_PT_ORPORT not an addport."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "lulz",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_6(self):
        """TOR_PT_SERVER_BINDADDR not an addport."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-lyrical_content,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_7(self):
        """Assymetric TOR_PT_SERVER_TRANSPORTS and TOR_PT_SERVER_BINDADDR."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,laughs-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_8(self):
        """Assymetric TOR_PT_SERVER_TRANSPORTS and TOR_PT_SERVER_BINDADDR."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,laughs-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_bad_environment_9(self):
        """Assymetric TOR_PT_SERVER_TRANSPORTS and TOR_PT_SERVER_BINDADDR."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,laughs" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["dummy"])

    def test_disabled_extorport(self):
        """Disabled TOR_PT_EXTENDED_SERVER_PORT."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        retval = pyptlib.server.init(["dummy"])
        self.assertIsNone(retval['ext_orport'])

    def test_unknown_transport(self):
        """Application only supports unknown transport."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "dummy-127.0.0.1:5556,boom-127.0.0.1:6666",
                         "TOR_PT_SERVER_TRANSPORTS" : "dummy,boom" }

        os.environ = TEST_ENVIRON
        retval = pyptlib.server.init(["inexistent"])
        self.assertEqual(len(retval['transports']), 0)

    def test_matched_transports(self):
        """Application only supports some transport."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "midnight-127.0.0.1:5556,herbie-127.0.0.1:6666,landing-127.0.0.1:9999",
                         "TOR_PT_SERVER_TRANSPORTS" : "midnight,herbie,landing" }

        os.environ = TEST_ENVIRON
        retval = pyptlib.server.init(["midnight","landing"])
        self.assertIn("midnight",retval['transports'])
        self.assertIn("landing",retval['transports'])
        self.assertEquals(len(retval['transports']), 2)

    def test_correct_ext_orport(self):
        """Correct Extended ORPort configuration."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "127.0.0.1:5555",
                         "TOR_PT_AUTH_COOKIE_FILE" : "/lulzie",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "what-127.0.0.1:5556",
                         "TOR_PT_SERVER_TRANSPORTS" : "what" }

        os.environ = TEST_ENVIRON
        retval = pyptlib.server.init(["what"])
        self.assertEquals(retval['auth_cookie_file'], '/lulzie')
        self.assertEquals(retval['ext_orport'], ('127.0.0.1', 5555))

    def test_ext_or_but_no_auth_cookie(self):
        """TOR_PT_EXTENDED_SERVER_PORT without TOR_PT_AUTH_COOKIE_FILE."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_EXTENDED_SERVER_PORT" : "127.0.0.1:5555",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "what-127.0.0.1:5556",
                         "TOR_PT_SERVER_TRANSPORTS" : "what" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["what"])

    def test_auth_cookie_but_no_ext_or(self):
        """TOR_PT_AUTH_COOKIE_FILE without TOR_PT_EXTENDED_SERVER_PORT."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_AUTH_COOKIE_FILE" : "/lulzie",
                         "TOR_PT_ORPORT" : "127.0.0.1:43210",
                         "TOR_PT_SERVER_BINDADDR" : "what-127.0.0.1:5556",
                         "TOR_PT_SERVER_TRANSPORTS" : "what" }

        os.environ = TEST_ENVIRON
        self.assertRaises(pyptlib.config.EnvError, pyptlib.server.init, ["what"])

if __name__ == '__main__':
    unittest.main()

