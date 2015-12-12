"""
Python interface to NTP Shared Memory.

"""

NAME = 'ntpdshm'
VERSION = '0.1.0'
LICENSE = 'BSD License'
AUTHOR = 'Markus Juenemann'
EMAIL = 'markus@juenemann.net'
DESCRIPTION = 'Python interface to NTP Shared Memory'
URL = 'https://github.com/mjuenema/python-ntpdshm'


import struct 
import ctypes
import sysv_ipc

NTPD_SHM_KEY = 0x4e545030

_INT = struct.Struct('i')
_UINT = struct.Struct('I')
_SIZE = _INT.size

LEAP_NOWARNING = 0x0
LEAP_ADDSECOND = 0x1
LEAP_DELSECOND = 0x2
LEAP_NOTINSYNC = 0x3


class NtpdShm(object):
    """NTP Shared Memory.

       One of the convenient thing about the NTP shared memory is
       that all fields are of the same size (integer, unsigned integer
       or time_t). This makes it easy to calulate the offset
       into the shared memory as a multiple of the size of an
       integer.

    """


    def __init__(self, unit=0):
        self.unit = 0

        if unit < 0:
            raise ValueError("unit must be posotive")

        if unit in [0,1]:
            mode = 0600
        else:
            mode = 0666

        try:
            # Open new shared memory segment.
            self.shm = sysv_ipc.SharedMemory(key=NTPD_SHM_KEY + unit, 
                                    flags=sysv_ipc.IPC_CREX,
                                    mode=mode,
                                    size=20*_SIZE)
        except sysv_ipc.ExistentialError:
            # Open existing shared memory segment.
            self.shm = sysv_ipc.SharedMemory(key=NTPD_SHM_KEY + unit, 
                                    flags=0,
                                    mode=mode,
                                    size=0)

    def __del__(self):
        self.shm.detach()
        self.shm.remove()	# in case ntpd is not running.

    def _get(self, n, s=_INT):
        """Get a field from shared memory.
 
           :param n: Get the n'th field.
           :type n: Integer greater or equal zero.
           :param s: Converter into integer or unsigned integer.
           :type s: Instance of `struct.Struct`.
           :returns: The value of the field.
           :rtype: Integer as appropriate for the field. 
          
        """

        return s.unpack(self.shm.read(_SIZE, n*_SIZE))[0]


    def _set(self, v, n, s=_INT):
        """Set a field in shared memory.

           :param v: The value to set the field to.
           :type v: Integer as appropriate for the field. 
           :param n: Get the n'th field.
           :type n: Integer greater or equal zero.
           :param s: Converter into integer or unsigned integer.
           :type s: Instance of `struct.Struct`.

        """

        self.shm.write(s.pack(v), n*_SIZE)

    mode = property(lambda self: self._get(0), 
                    lambda self,v: self._set(v, 0))

    count = property(lambda self: self._get(1), 
                     lambda self,v: self._set(v, 1))

    clockTimeStampSec = property(lambda self: self._get(2), 
                                 lambda self,v: self._set(v, 2))

    clockTimeStampUSec = property(lambda self: self._get(3), 
                                  lambda self,v: self._set(v, 3))

    clockTimeStampNSec = property(lambda self: self._get(10, _UINT), 
                                  lambda self,v: self._set(v, 10, _UINT))

    receiveTimeStampSec = property(lambda self: self._get(4), 
                                   lambda self,v: self._set(v, 4))

    receiveTimeStampUSec = property(lambda self: self._get(5), 
                                    lambda self,v: self._set(v, 5))

    receiveTimeStampNSec = property(lambda self: self._get(11, _UINT), 
                                    lambda self,v: self._set(v, 11, _UINT))

    leap = property(lambda self: self._get(6),
                    lambda self,v: self._set(v, 6))

    precision = property(lambda self: self._get(7),
                         lambda self,v: self._set(v, 7))

    nsamples = property(lambda self: self._get(8),
                        lambda self,v: self._set(v, 8))

    _valid = property(lambda self: self._get(9),
                      lambda self,v: self._set(v, 9))

    def _get_valid(self):
        return self._valid == True

    def _set_valid(self, v):
        if v:
            self._valid = 1
        else:
            self._valid = 0

    valid = property(_get_valid, _set_valid)

    def _get_clockTimeStamp(self):
        return float(self.clockTimeStampSec) + float(self.clockTimeStampUSec) / 10**6

    def _set_clockTimeStamp(self, v):
        self.clockTimeStampSec = int(v)
        self.clockTimeStampUSec = int(v % 1.0 * 10**6)
        self.clockTimeStampNSec = int(v % 1.0 * 10**9)

    clockTimeStamp = property(_get_clockTimeStamp, _set_clockTimeStamp)

    def _get_receiveTimeStamp(self):
        return float(self.receiveTimeStampSec) + float(self.receiveTimeStampUSec) / 10**6

    def _set_receiveTimeStamp(self, v):
        self.receiveTimeStampSec = int(v)
        self.receiveTimeStampUSec = int(v % 1.0 * 10**6)
        self.receiveTimeStampNSec = int(v % 1.0 * 10**9)

    receiveTimeStamp = property(_get_receiveTimeStamp, _set_receiveTimeStamp)

    def update(self,
               clockTimeStamp,
               receiveTimeStamp=None,
               mode=None,
               leap=None,
               precision=None,
               nsamples=None):

        self.valid = False
        self.count += 1
        self.clockTimeStamp = clockTimeStamp

        if receiveTimeStamp is not None:
            self.receiveTimeStamp = receiveTimeStamp

        if mode is not None:
            self.mode = mode

        if leap is not None:
            self.leap = leap

        if precision is not None:
            self.precision = precision

        if nsamples is not None:
            self.nsamples = nsamples

        self.valid = True
               
        
        
