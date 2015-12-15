python-ntpdshm
**************

Overview
========

*python-ntpdshm* provides a Python interface to *ntpd's* shared memory `driver 28`_. A single
class ``NtpdShm`` exposes the fields of the shared memory structure as attributes that can be read and written.
In addition there are properties to set the clock and receive timestamps from float values. There is also a convenience ``update()`` function for setting the time related fields in a single step.

*python-ntpdshm* is implemented using Swig_.

.. _Swig: http://www.swig.org/Doc1.3/Python.html

*python-ntpdshm* works with the following Python versions.

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* PyPy (but not PyPy3!)

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
   ntpd_shm.valid = 0                     # don't use Python boolean
   ntpd_shm.clockTimeStamp = clock_time   
   ntpd_shm.receiveTimeStamp = recv_time  
   ntpd_shm.precision = -5                # 2^-5 = 0.03125 seconds in this case
   ntpd_shm.count += 1
   ntpd_shm.valid = 1
     
As this is somewhat cumbersome, there is a convenience method ``update()`` that achieves the same in 
a single line. It requires the ``clock_time`` as mandatory argument and accepts several optional
arguments.

.. code-block:: python

   ntpd_shm.update(clock_time, recv_time=recv_time, precision=-5)
   
   # Or simply, if no other fields are to be changed. The receive timestamp is set
   # automatically.
   ntpd_shm.update(clock_time)

.. _`driver 28`: http://doc.ntp.org/4.2.8/drivers/driver28.html


Applications
============

"Off by one second" reference time
----------------------------------

A just for fun example of using *python-ntpdshm* is to implement an "off by one second" reference time source for *ntpd*. While this example makes no sense at all for practical purposes it provides a useful template for how it all fits together.

First we write the code for the reference clock.

.. code-block:: python

   import time
   import ntpdshm
   
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
           time.sleep(1.0)
           
   if __name__ == '__main__':
       main()
       
Then add the shared memory reference clock to ``ntp.conf``:: 

  # ntp.conf
  ...
  server 127.127.28.2 noselect     # unit=2, never select this reference
  fudge 127.127.28.2 refid PYTH stratum 10

Restart *ntpd* and monitor the output of ``ntpq -pn``. The offset should be exactly -1000 msec:

.. code-block:: console

   $ ntpq -pn
        remote           refid      st t when poll reach   delay   offset  jitter
   ==============================================================================
   ...
    127.127.28.2    .PYTH.          10 l    9   16  377    0.000  -1000.0   0.017

"HyperTextNetworkTimeProtocol" (htntp)
--------------------------------------
  
**Note: This is currently in the planning stage.**
  
While there are already other (htpdate_, htp_) solutions for synchronising "a computer's time with web servers as reference time source", the *python-ntpdshm* project includes yet another implementation. The main difference is that this implementation "feeds" *ntpd's* shared memory driver while htpdate_ and htp_ take control of a system's time themselves. More importantly the *python-ntpdshm*/*ntpd* variant can achieve a much higher accuracy of +-0.1 seconds [*to be tested*] in comparison to +-0.5 seconds quoted by htpdate_ and htp_.
  
  .. _htpdate: http://www.vervest.org/htp/
  .. _htp: http://www.rkeene.org/oss/htp/
  
Add the shared memory reference clock to ``ntp.conf``. Set ``minpoll`` and  ``maxpoll`` to intervals larger than the ``-i/--interval`` command line argument to ``htntp.py``::

  # ntp.conf
  ...
  server 127.127.28.2 minpoll 9 maxpoll 9      # unit=2, poll every 2^9 = 512 seconds
  fudge 127.127.28.2 refid HTTP stratum 5
  
Then start ``htntp.py`` as shown below. Chose web servers that provide quick response times; three to five servers should be sufficient.
  
  .. code-block:: console
  
     # python htntp.py --unit 2 --interval 300 --proxy 192.168.1.1:3128 www.google.com.au www.ebay.com.au www.abc.net.au
