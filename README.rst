python-ntpdshm
**************

Status
======

**This Python package is currently in the planning phase. There is no actual code yet.**

Overview
========

*python-ntpdshm* provides a Python interface to *ntpd's* shared memory `driver 28`_. A single
class ``NtpdShm`` exposes the fields of the shared memory structure as attributes that can be read and written.
In addition is a convenience ``update()`` function for updating the time related fields in a
single step.

*python-ntpdshm* is implemented entirely in Python, building on the ctypes_ module of the Python Standard Library and Philip Semanchuk's posix_ipc_ package.

.. _ctypes: https://docs.python.org/2/library/ctypes.html
.. _posix_ipc: https://pypi.python.org/pypi/posix_ipc

*python-ntpdshm* works with all Python versions since 2.6 (well, we'll see!)

Example
=======

.. code-block:: python

   import ntpdshm
   
   ntpd_shm = ntpdshm.NtpdShm(unit=0)

The members of the C struct (except for ``dummy``) can be accessed by their original names. These have **not**
been converted into PEP-8 compliant names.

.. code-block:: python
   
   print ntpd_shm.mode
   print ntpd_shm.clockTimeStampSec
   print ntpd_shm.clockTimeStampUSec
   print ntpd_shm.clockTimeStampNSec      # only ntpd 4.2.7p303 or later, probably random value otherwise
   print ntpd_shm.receiveTimeStampSec
   print ntpd_shm.receiveTimeStampUSec
   print ntpd_shm.receiveTimeStampNSec    # only ntpd 4.2.7p303 or later, probably random value otherwise
   print ntpd_shm.leap
   print ntpd_shm.precision
   print ntpd_shm.valid

In addition there are two pseudo properties that combine the second and microsecond attributes into 
"float" timestamps. These don't support nanosecond precision as (as far as I know) it is not possible
to detect whether *ntpd* does support nanosecond resolution.

.. code-block:: python

   print ntpd_shm.clockTimeStamp          # clockTimeStampSec.clockTimeStampUSec
   print ntpd_shm.receiveTimeStamp         # receiveTimeStampSec.receiveTimeStampUSec

The process to feed *ntpd* an external reference time is shown below.

.. code-block:: python

   import time
   
   clock_time = get_clock_time()          # `get_clock_time` must be implemented somewhere else and
                                          # return a float.
   recev_time = time.time()
   ntpd_shm.valid = False                 # can use Python boolean here
   ntpd_shm.clockTimeStamp = clock_time   
   ntpd_shm.receiveTimeStamp = recv_time  
   ntpd_shm.precision = -5                # 2^-5 = 0.03125 seconds in this case
   ntpd_shm.count += 1
   ntpd_shm.valid = True
     
As this is somewhat cumbersome, there is a convenience method ``update()`` that achieves the same in 
a single line. It requires the ``clock_time`` as mandatory argument and accepts several optional
arguments.

.. code-block:: python

   ntpd_shm.update(clock_time, recv_time=recv_time, precision=-5)
   
   # Or simply, if no other fields are to be changed. The receive timestamp is set
   # automatically.
   ntpd_shm.update(clock_time)

.. _`driver 28`: http://doc.ntp.org/4.2.8/drivers/driver28.html

Just for fun
============

A just for fun example of using *python-ntpdshm* is to implement an "off by one second" reference time source for *ntpd*. While this example makes no sense at all for practical purposes it provides a useful template for how it all hangs together.

First we write the code for the reference clock.

.. code-block:: python

   import time
   import ntpdshm
   
   def get_clock_time():
       return time.time() - 1.0     # always be exactly one second behind.
       
   def main():
       ntpd_shm = ntpdshm.NtpdShm(unit=2)
       ntpd_shm.precision = -6      # set precision once
       ntpd_shm.leap = 0            # how would we know about leap seconds?
       
       while True:
           clock_time = get_clock_time()
           ntpd_shm.update(clock_time)
           time.sleep(1.0)
           
   if __name__ == '__main__':
       main()
       
Then add the shared memory reference clock to ``ntp.conf``:: 

  # ntp.conf
  server 127.127.28.2 noselect     # unit=2, never select this reference
  fudge 127.127.28.2 refid PYTH stratum 10

Restart *ntpd* and monitor the output of ``ntpq -pn``. The offset should be exactly -1000 msec:

.. code-block:: console

   $ ntpq -pn
   TODO

  
