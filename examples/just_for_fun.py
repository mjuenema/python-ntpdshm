#!/usr/bin/env python

"""
Just for fun example as described in README.rst.

Markus Juenemann, 12-Dec-2015
"""



import time
import ntpdshm
import struct

def get_clock_time():
    return time.time() - 1.0     # always be exactly one second behind.

def main():
    ntpd_shm = ntpdshm.NtpdShm(unit=2)
    ntpd_shm.mode = 0            # set mode
    ntpd_shm.precision = -6      # set precision once
    ntpd_shm.leap = 0            # how would we know about leap seconds?

    while True:
        clock_time = get_clock_time()
        ntpd_shm.update(clock_time)
        print clock_time, ntpd_shm.count
        #print struct.unpack('iiiiiiiiiiII8i', ntpd_shm.shm.read())
        print len(ntpd_shm.shm.read())
        time.sleep(1.0)

if __name__ == '__main__':
    main()
