from array import array
from cffi import FFI

ffi = FFI()

ffi.cdef("""
#define EVBACKEND_SELECT ...
#define EV_READ ...
#define EV_WRITE ...
#define EVBREAK_ALL ...

typedef ... ev_loop;

struct ev_loop *ev_loop_new (unsigned int flags);
void ev_loop_destroy (struct ev_loop*);
void ev_break (struct ev_loop*, int);
int ev_run (struct ev_loop*, int);

typedef struct { ...; } ev_io;
typedef void (*io_cb) (struct ev_loop*, ev_io*, int);
void ev_io_init(ev_io*, io_cb, int, int);
void ev_io_start(struct ev_loop*, ev_io*);
void ev_io_stop(struct ev_loop*, ev_io*);

typedef struct { ...; } ev_signal;
typedef void (*signal_cb) (struct ev_loop*, ev_signal*, int);
void ev_signal_init(ev_signal*, signal_cb, int);
void ev_signal_start(struct ev_loop*, ev_signal*);
void ev_signal_stop(struct ev_loop*, ev_signal*);

typedef double ev_tstamp;
typedef struct { ...; } ev_timer;
typedef void (*timer_cb) (struct ev_loop*, ev_timer*, int);
void ev_timer_init(ev_timer*, timer_cb, ev_tstamp, ev_tstamp);
void ev_timer_start(struct ev_loop*, ev_timer*);
void ev_timer_again(struct ev_loop*, ev_timer*);
void ev_timer_stop(struct ev_loop*, ev_timer*);
""")

C = ffi.verify("""
#include <ev.h>
""", libraries=['ev'])

NULL = ffi.NULL
globals().update(C.__dict__)


class Loop(object):
    def __init__(self):
        self._loop = ev_loop_new(EVBACKEND_SELECT)

    def destroy(self):
        ev_loop_destroy(self._loop)

    def run(self, flags=0):
        ev_run(self._loop, flags)

    def break_(self, flags=EVBREAK_ALL):
        ev_break(self._loop, flags)


class IOWatcher(object):
    def __init__(self, cb, fd, flags):
        self._watcher = ffi.new('ev_io*')
        self._cb = ffi.callback('io_cb', cb)
        ev_io_init(self._watcher, self._cb, fd, flags)

    def start(self, loop):
        ev_io_start(loop._loop, self._watcher)

    def stop(self, loop):
        ev_io_stop(loop._loop, self._watcher)


class SignalWatcher(object):
    def __init__(self, cb, signal):
        self._watcher = ffi.new('ev_signal*')
        self._cb = ffi.callback('signal_cb', cb)
        ev_signal_init(self._watcher, self._cb, signal)

    def start(self, loop):
        ev_signal_start(loop._loop, self._watcher)

    def stop(self, loop):
        ev_signal_stop(loop._loop, self._watcher)


class TimerWatcher(object):
    def __init__(self, cb, after, repeat=0.0):
        self._watcher = ffi.new('ev_timer*')
        self._cb = ffi.callback('timer_cb', cb)
        ev_timer_init(self._watcher, self._cb, after, repeat)

    def start(self, loop):
        ev_timer_start(loop._loop, self._watcher)

    def stop(self, loop):
        ev_timer_stop(loop._loop, self._watcher)

    def again(self, loop):
        ev_timer_again(loop._loop, self._watcher)