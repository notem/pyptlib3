import unittest

import signal
import subprocess
import time

from pyptlib.util.subproc import auto_killall, create_sink, Popen, SINK
from subprocess import PIPE

# We ought to run auto_killall(), instead of manually calling proc.terminate()
# but it's not very good form to use something inside the test for itself. :p

def proc_wait(proc, wait_s):
    time.sleep(wait_s)
    proc.poll() # otherwise it doesn't exit properly

def proc_is_alive(pid):
    r = subprocess.call(("ps -p %s" % pid).split(), stdout=create_sink())
    return True if r == 0 else False


class SubprocTest(unittest.TestCase):

    def name(self):
        return self.id().split(".")[-1].replace("test_", "")

    def getMainArgs(self):
        return ["python", "./util_subproc_main.py", self.name()]

    def spawnMain(self, cmd=None, stdout=PIPE, **kwargs):
        # spawn the main test process and wait a bit for it to initialise
        proc = Popen(cmd or self.getMainArgs(), stdout = stdout, **kwargs)
        time.sleep(0.2)
        return proc

    def readChildPid(self, proc):
        line = proc.stdout.readline()
        self.assertTrue(line.startswith("child "))
        return int(line.replace("child ", ""))

    def test_Popen_IOpassthru(self):
        output = subprocess.check_output(self.getMainArgs())
        self.assertTrue(len(output) > 0)

    def test_Popen_SINK(self):
        output = subprocess.check_output(self.getMainArgs())
        self.assertTrue(len(output) == 0)

    def test_trap_sigint_multiple(self):
        proc = self.spawnMain()
        proc.send_signal(signal.SIGINT)
        self.assertEquals("run h1\n", proc.stdout.readline())
        proc.send_signal(signal.SIGINT)
        self.assertEquals("run h2\n", proc.stdout.readline())
        self.assertEquals("run h1\n", proc.stdout.readline())
        proc.terminate()

    def test_trap_sigint_reset(self):
        proc = self.spawnMain()
        proc.send_signal(signal.SIGINT)
        self.assertEquals("run h2\n", proc.stdout.readline())
        proc.terminate()

    def test_killall_kill(self):
        proc = self.spawnMain()
        pid = proc.pid
        cid = self.readChildPid(proc)
        self.assertTrue(proc_is_alive(cid), "child did not hang")
        time.sleep(2)
        self.assertTrue(proc_is_alive(cid), "child did not ignore TERM")
        time.sleep(4)
        self.assertFalse(proc_is_alive(cid), "child was not killed by parent")
        proc.terminate()

    def test_auto_killall_2_int(self):
        proc = self.spawnMain()
        pid = proc.pid
        cid = self.readChildPid(proc)
        # test first signal is ignored
        proc.send_signal(signal.SIGINT)
        proc_wait(proc, 3)
        self.assertTrue(proc_is_alive(pid), "1 INT not ignored")
        self.assertTrue(proc_is_alive(cid), "1 INT not ignored")
        # test second signal is handled
        proc.send_signal(signal.SIGINT)
        proc_wait(proc, 3)
        self.assertFalse(proc_is_alive(pid), "2 INT not handled")
        self.assertFalse(proc_is_alive(cid), "2 INT not handled")

    def test_auto_killall_term(self):
        proc = self.spawnMain()
        pid = proc.pid
        cid = self.readChildPid(proc)
        # test TERM is handled
        proc.send_signal(signal.SIGTERM)
        proc_wait(proc, 3)
        self.assertFalse(proc_is_alive(pid), "TERM not handled")
        self.assertFalse(proc_is_alive(cid), "TERM not handled")

    def test_auto_killall_exit(self):
        proc = self.spawnMain()
        pid = proc.pid
        cid = self.readChildPid(proc)
        # test exit is handled. main exits by itself after 1 seconds
        # exit handler takes ~2s to run, usually
        proc_wait(proc, 3)
        self.assertFalse(proc_is_alive(pid), "unexpectedly did not exit")
        self.assertFalse(proc_is_alive(cid), "parent did not kill child")

if __name__ == "__main__":
    unittest.main()
