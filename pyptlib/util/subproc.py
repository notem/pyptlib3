"""Common tasks for managing child processes.

To have child processes actually be managed by this module, you should use
the Popen() here rather than subprocess.Popen() directly.
"""

import atexit
import inspect
import os
import signal
import subprocess
import time

_CHILD_PROCS = []
# TODO(infinity0): add functionality to detect when any child dies, and
# offer different response strategies for them (e.g. restart the child? or die
# and kill the other children too).

SINK = object()

a = inspect.getargspec(subprocess.Popen.__init__)
_Popen_defaults = zip(a.args[-len(a.defaults):],a.defaults); del a
class Popen(subprocess.Popen):
    """Wrapper for subprocess.Popen that tracks every child process.

    See the subprocess module for documentation.

    Additionally, you may use subproc.SINK as the value for either of the
    stdout, stderr arguments to tell subprocess to discard anything written
    to those channels.
    """

    def __init__(self, *args, **kwargs):
        kwargs = dict(_Popen_defaults + kwargs.items())
        for f in ['stdout', 'stderr']:
            if kwargs[f] is SINK:
                kwargs[f] = create_sink()
        # super() does some magic that makes **kwargs not work, so just call
        # our super-constructor directly
        subprocess.Popen.__init__(self, *args, **kwargs)
        _CHILD_PROCS.append(self)

    # TODO(infinity0): perhaps replace Popen.std* with wrapped file objects
    # that don't buffer readlines() et. al. Currently one must avoid these and
    # use while/readline(); see man page for "python -u" for more details.

def create_sink():
    return open(os.devnull, "w", 0)

_SIGINT_RUN = {}
def trap_sigint(handler, ignoreNum=0):
    """Register a handler for an INT signal.

    Successive traps registered via this function are cumulative, and override
    any previous handlers registered using signal.signal(). To reset these
    cumulative traps, call signal.signal() with another (maybe dummy) handler.

    Args:
        handler: a signal handler; see signal.signal() for details
        ignoreNum: number of signals to ignore before activating the handler,
            which will be run on all subsequent signals.
    """
    prev_handler = signal.signal(signal.SIGINT, _run_sigint_handlers)
    if prev_handler != _run_sigint_handlers:
        _SIGINT_RUN.clear()
    _SIGINT_RUN.setdefault(ignoreNum, []).append(handler)

_intsReceived = 0
def _run_sigint_handlers(signum=0, sframe=None):
    global _intsReceived
    _intsReceived += 1

    # code snippet adapted from atexit._run_exitfuncs
    exc_info = None
    for i in xrange(_intsReceived).__reversed__():
        for handler in _SIGINT_RUN.get(i, []).__reversed__():
            try:
                handler(signum, sframe)
            except SystemExit:
                exc_info = sys.exc_info()
            except:
                import traceback
                print >> sys.stderr, "Error in subproc._run_sigint_handlers:"
                traceback.print_exc()
                exc_info = sys.exc_info()

    if exc_info is not None:
        raise exc_info[0], exc_info[1], exc_info[2]

_isTerminating = False
def killall(wait_s=16):
    """Attempt to gracefully terminate all child processes.

    All children are told to terminate gracefully. A waiting period is then
    applied, after which all children are killed forcefully. If all children
    terminate before this waiting period is over, the function exits early.
    """
    # TODO(infinity0): log this somewhere, maybe
    global _isTerminating, _CHILD_PROCS
    if _isTerminating: return
    _isTerminating = True
    # terminate all
    for proc in _CHILD_PROCS:
        if proc.poll() is None:
            proc.terminate()
    # wait and make sure they're dead
    for i in xrange(wait_s):
        _CHILD_PROCS = [proc for proc in _CHILD_PROCS
                        if proc.poll() is None]
        if not _CHILD_PROCS: break
        time.sleep(1)
    # if still existing, kill them
    for proc in _CHILD_PROCS:
        if proc.poll() is None:
            proc.kill()
    time.sleep(0.5)
    # reap any zombies
    for proc in _CHILD_PROCS:
        proc.poll()

def auto_killall(ignoreNumSigInts=0):
    """Automatically terminate all child processes on exit.

    Args:
        ignoreNumSigInts: this number of INT signals will be ignored before
            attempting termination. This will be attempted unconditionally in
            all other cases, such as on normal exit, or on a TERM signal.
    """
    killall_handler = lambda signum, sframe: killall()
    trap_sigint(killall_handler, ignoreNumSigInts)
    signal.signal(signal.SIGTERM, killall_handler)
    atexit.register(killall)
