#!/usr/bin/python

import os
import signal
import sys
import time

from pyptlib.util.subproc import auto_killall, killall, trap_sigint, Popen, SINK
from subprocess import PIPE


def startChild(subcmd, stdout=SINK, **kwargs):
    return Popen(
        ["python", "util_subproc_child.py", subcmd],
        stdout = stdout,
        **kwargs
    )

def sleepIgnoreInts(ignoreNumInts=3):
    for i in xrange(ignoreNumInts):
        time.sleep(100)

def handler1(signum=0, sframe=None):
    print "run h1"
    sys.stdout.flush()

def handler2(signum=0, sframe=None):
    print "run h2"
    sys.stdout.flush()

def main_Popen_IOpassthru(testname, *argv):
    child = startChild("default_io", stdout=None)
    child.wait()

def main_Popen_SINK(testname, *argv):
    child = startChild("default_io")
    child.wait()

def main_trap_sigint_multiple(testname, *argv):
    trap_sigint(handler1)
    trap_sigint(handler2, 1)
    sleepIgnoreInts(2)

def main_trap_sigint_reset(testname, *argv):
    trap_sigint(handler1)
    signal.signal(signal.SIGINT, lambda signum, sframe: None)
    trap_sigint(handler2)
    sleepIgnoreInts(1)

def main_killall_kill(testname, *argv):
    child = startChild(testname)
    time.sleep(1)
    killall(4)
    time.sleep(100)

def main_auto_killall_2_int(testname, *argv):
    auto_killall(1)
    child = startChild("default")
    child.wait()

def main_auto_killall_term(testname, *argv):
    auto_killall()
    child = startChild("default")
    child.wait()

def main_auto_killall_exit(testname, *argv):
    auto_killall()
    child = startChild("default")
    time.sleep(1)

if __name__ == "__main__":
    getattr(sys.modules[__name__], "main_%s" % sys.argv[1])(*sys.argv[1:])
