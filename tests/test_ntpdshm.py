"""
Tests for ntpdshm.

WARNING: Running these tests may confuse the hell out of ntpd!!!

Markus Juenemann, 12-Dec-2015

"""


from nose.tools import *

import ntpdshm
import random
import time
import copy
import sys

#def setup():
#    sys.stderr.write('Testing, whether ntpd is accessing the shared memory... ')
#    for unit in [0, 1, 2, 3]:
#        shm = ntpdshm.NtpdShm(unit)
#
#        count1 = copy.copy(shm.count)
#        time.sleep(1.2)
#        count2 = copy.copy(shm.count)
#
#        if count1 != count2:
#            raise EnvironmentError("don't run the tests while ntpd is accessing the shared memory\n")
#
#    sys.stderr.write('no\n')


class NtpdShmTests(object):
    unit = None

    def setup(self):
        self.shm = ntpdshm.NtpdShm(self.unit)

    def teardown(self):
        del(self.shm)

    def test_mode(self):
        self.shm.mode = 0
        assert self.shm.mode == 0
        self.shm.mode = 1
        assert self.shm.mode == 1

    def test_leap(self):
        self.shm.leap = 0
        assert self.shm.leap == 0
        self.shm.leap = 1
        assert self.shm.leap == 1

    def test_nsamples(self):
        self.shm.nsamples = 0
        assert self.shm.nsamples == 0
        self.shm.nsamples = 1
        assert self.shm.nsamples == 1

    def test_precision(self):
        self.shm.precision = 0
        assert self.shm.precision == 0
        self.shm.precision = 1
        assert self.shm.precision == 1

    def test_count(self):
        self.shm.count = 0
        assert self.shm.count == 0
        self.shm.count = 1
        assert self.shm.count == 1

    def test_valid(self):
        self.shm.valid = True
        assert self.shm.valid == True
        assert self.shm._valid == 1

        self.shm.valid = False
        assert self.shm.valid == False
        assert self.shm._valid == 0

        self.shm.valid = 1
        assert self.shm.valid == True
        assert self.shm._valid == 1

        self.shm.valid = 0
        assert self.shm.valid == False
        assert self.shm._valid == 0

    def test_clockTimeStamp(self):
        self.shm.clockTimeStamp = 12345.987654321
        assert self.shm.clockTimeStamp == 12345.987654	          # no nansoeconds!
        assert self.shm.clockTimeStampSec == 12345
        assert self.shm.clockTimeStampUSec == 987654
        assert abs(self.shm.clockTimeStampNSec - 987654321) <= 1  # conversion errors

    def test_receiveTimeStamp(self):
        self.shm.receiveTimeStamp = 54321.123456789
        assert self.shm.receiveTimeStamp == 54321.123456            # no nansoeconds!
        assert self.shm.receiveTimeStampSec == 54321
        assert self.shm.receiveTimeStampUSec == 123456
        assert abs(self.shm.receiveTimeStampNSec - 123456789) <= 1  # conversion errors


class NtpdShmUpdateTests(object):
    unit = None

    def setup(self):
        self.shm = ntpdshm.NtpdShm(self.unit)
        self.shm.valid = False
        self.shm.count = 0
        self.shm.leap = 0
        self.shm.precision = 0
        self.shm.nsamples = 0
        self.shm.mode = 0

    def test_update(self):
        self.shm.update(654321.214365879)
        assert int(self.shm.receiveTimeStamp) == int(time.time())	
        assert self.shm.clockTimeStamp == 654321.214365
        assert self.shm.clockTimeStampSec == 654321
        assert self.shm.clockTimeStampUSec == 214365
        assert abs(self.shm.clockTimeStampNSec - 214365879) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 0
        assert self.shm.precision == 0
        assert self.shm.nsamples == 0
        assert self.shm.mode == 0
       
    def test_update_leap(self):
        self.shm.update(654322.314365879, leap=1)
        assert self.shm.clockTimeStamp == 654322.314365
        assert self.shm.clockTimeStampSec == 654322
        assert self.shm.clockTimeStampUSec == 314365
        assert abs(self.shm.clockTimeStampNSec - 314365879) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 1
        assert self.shm.precision == 0
        assert self.shm.nsamples == 0
        assert self.shm.mode == 0

    def test_update_precision(self):
        self.shm.update(654323.414365879, precision=-1)
        assert self.shm.clockTimeStamp == 654323.414365
        assert self.shm.clockTimeStampSec == 654323
        assert self.shm.clockTimeStampUSec == 414365
        assert abs(self.shm.clockTimeStampNSec - 414365879) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 0
        assert self.shm.precision == -1
        assert self.shm.nsamples == 0
        assert self.shm.mode == 0

    def test_update_nsamples(self):
        self.shm.update(654324.514365879, nsamples=5)
        assert self.shm.clockTimeStamp == 654324.514365
        assert self.shm.clockTimeStampSec == 654324
        assert self.shm.clockTimeStampUSec == 514365
        assert abs(self.shm.clockTimeStampNSec - 514365879) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 0
        assert self.shm.precision == 0
        assert self.shm.nsamples == 5
        assert self.shm.mode == 0

    def test_update_mode(self):
        self.shm.update(254324.524365879, mode=6)
        assert self.shm.clockTimeStamp == 254324.524365
        assert self.shm.clockTimeStampSec == 254324
        assert self.shm.clockTimeStampUSec == 524365
        assert abs(self.shm.clockTimeStampNSec - 524365879) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 0
        assert self.shm.precision == 0
        assert self.shm.nsamples == 0
        assert self.shm.mode == 6

    def test_update_receiveTimestamp(self):
        self.shm.update(254324.524365879, receiveTimeStamp=76543.219876543)
        assert self.shm.clockTimeStamp == 254324.524365
        assert self.shm.clockTimeStampSec == 254324
        assert self.shm.clockTimeStampUSec == 524365
        assert abs(self.shm.clockTimeStampNSec - 524365879) <= 1
        assert self.shm.receiveTimeStamp == 76543.219876
        assert self.shm.receiveTimeStampSec == 76543
        assert self.shm.receiveTimeStampUSec == 219876
        assert abs(self.shm.receiveTimeStampNSec - 219876543) <= 1
        assert self.shm.valid is True
        assert self.shm.count == 1
        assert self.shm.leap == 0
        assert self.shm.precision == 0
        assert self.shm.nsamples == 0
        assert self.shm.mode == 0
        

class TestNtpdShmUnit0(NtpdShmTests):
    unit = 0

class TestNtpdShmUnit1(NtpdShmTests):
    unit = 1

class TestNtpdShmUnit2(NtpdShmTests):
    unit = 2

class TestNtpdShmUnit3(NtpdShmTests):
    unit = 3

class TestNtpdShmUpdateUnit0(NtpdShmUpdateTests):
    unit = 0

class TestNtpdShmUpdateUnit1(NtpdShmUpdateTests):
    unit = 1

class TestNtpdShmUpdateUnit2(NtpdShmUpdateTests):
    unit = 2

class TestNtpdShmUpdateUnit3(NtpdShmUpdateTests):
    unit = 3
