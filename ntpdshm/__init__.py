"""
Python interface to NTP Shared Memory.

"""

import time 
import ntpdshm.shm 

#NTPD_SHM_KEY = 0x4e545030

LEAP_NOWARNING = 0x0
LEAP_ADDSECOND = 0x1
LEAP_DELSECOND = 0x2
LEAP_NOTINSYNC = 0x3


class NtpdShm(object):
    """NTP Shared Memory.

    """

    def __init__(self, unit=0):
        if unit < 0 or unit > 5:
            raise ValueError("unit must be 0 <= unit <= 5")

        self.ntpd_shm = ntpdshm.shm.shm_get(unit)
        if self.ntpd_shm is None:
            raise OSError('Unable to attach to ntpd shared memory unit %d', unit)

    mode = property(lambda self: ntpdshm.shm.get_mode(self.ntpd_shm),
                    lambda self,mode: ntpdshm.shm.set_mode(self.ntpd_shm, mode))

    count = property(lambda self: ntpdshm.shm.get_count(self.ntpd_shm),
                     lambda self,count: ntpdshm.shm.set_count(self.ntpd_shm, count))

    clockTimeStampSec = property(lambda self: ntpdshm.shm.get_clockTimeStampSec(self.ntpd_shm),
                                 lambda self,clockTimeStampSec: ntpdshm.shm.set_clockTimeStampSec(self.ntpd_shm, clockTimeStampSec))

    clockTimeStampUSec = property(lambda self: ntpdshm.shm.get_clockTimeStampUSec(self.ntpd_shm),
                                  lambda self,clockTimeStampUSec: ntpdshm.shm.set_clockTimeStampUSec(self.ntpd_shm, clockTimeStampUSec))

    clockTimeStampNSec = property(lambda self: ntpdshm.shm.get_clockTimeStampNSec(self.ntpd_shm),
                                  lambda self,clockTimeStampNSec: ntpdshm.shm.set_clockTimeStampNSec(self.ntpd_shm, clockTimeStampNSec))

    receiveTimeStampSec = property(lambda self: ntpdshm.shm.get_receiveTimeStampSec(self.ntpd_shm),
                                   lambda self,receiveTimeStampSec: ntpdshm.shm.set_receiveTimeStampSec(self.ntpd_shm, receiveTimeStampSec))

    receiveTimeStampUSec = property(lambda self: ntpdshm.shm.get_receiveTimeStampUSec(self.ntpd_shm),
                                    lambda self,receiveTimeStampUSec: ntpdshm.shm.set_receiveTimeStampUSec(self.ntpd_shm, receiveTimeStampUSec))

    receiveTimeStampNSec = property(lambda self: ntpdshm.shm.get_receiveTimeStampNSec(self.ntpd_shm),
                                    lambda self,receiveTimeStampNSec: ntpdshm.shm.set_receiveTimeStampNSec(self.ntpd_shm, receiveTimeStampNSec))

    leap = property(lambda self: ntpdshm.shm.get_leap(self.ntpd_shm),
                    lambda self,leap: ntpdshm.shm.set_leap(self.ntpd_shm, leap))

    precision = property(lambda self: ntpdshm.shm.get_precision(self.ntpd_shm),
                         lambda self,precision: ntpdshm.shm.set_precision(self.ntpd_shm, precision))

    nsamples = property(lambda self: ntpdshm.shm.get_nsamples(self.ntpd_shm),
                        lambda self,nsamples: ntpdshm.shm.set_nsamples(self.ntpd_shm, nsamples))

    _valid = property(lambda self: ntpdshm.shm.get_valid(self.ntpd_shm),
                      lambda self,valid: ntpdshm.shm.set_valid(self.ntpd_shm, valid))


    # valid
    #
    def _get_valid(self):
        return self._valid == True

    def _set_valid(self, v):
        if v:
            self._valid = 1
        else:
            self._valid = 0

    valid = property(_get_valid, _set_valid)


    # clockTimeStamp
    #
    def _get_clockTimeStamp(self):
        return float(self.clockTimeStampSec) + float(self.clockTimeStampUSec) / 10**6

    def _set_clockTimeStamp(self, v):
        self.clockTimeStampSec = int(v)
        self.clockTimeStampUSec = int(v % 1.0 * 10**6)
        self.clockTimeStampNSec = int(v % 1.0 * 10**9)

    clockTimeStamp = property(_get_clockTimeStamp, _set_clockTimeStamp)


    # receiveTimeStamp
    #
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
        self.count = self.count + 1
        self.clockTimeStamp = clockTimeStamp

        if receiveTimeStamp is None:
            self.receiveTimeStamp = time.time()
        else:
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
