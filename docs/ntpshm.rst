******************
ntpd Shared Memory
******************

The Shared Memory interface to *ntpd* is defined in `driver 28`_: "This driver receives 
its reference clock info from a shared memory-segment. The shared memory-segment is created 
with owner-only access for unit 0 and 1, and world access for unit 2 and 3".

.. _`driver 28`: http://doc.ntp.org/4.2.6/drivers/driver28.html

As of the most recent version of *ntpd* (4.2.8) the C struct for the shared memory segment 
looks as shown below (I added some comments for clarification). The members for nanosecond 
precision, ``clockTimeStampNSec`` and ``receiveTimeStampNSec``, have been added in 
version `4.2.7p303`_, reducing the size of the traling ``dummy`` member from 10 to 8 integers. 

.. _`4.2.7p303`: http://bugs.ntp.org/show_bug.cgi?id=1232

.. code-block:: c

   struct shmTime {
        int    mode; /* 0 - if valid is set:
                      *       use values,
                      *       clear valid
                      * 1 - if valid is set:
                      *       if count before and after read of data is equal:
                      *         use values
                      *       clear valid
                      */
        volatile int    count;
        time_t          clockTimeStampSec;      /* external clock */
        int             clockTimeStampUSec;     /* external clock */
        time_t          receiveTimeStampSec;    /* internal clock, when external value was received */
        int             receiveTimeStampUSec;   /* internal clock, when external value was received */
        int             leap;
        int             precision;
        int             nsamples;
        volatile int    valid;
        unsigned        clockTimeStampNSec;     /* Unsigned ns timestamps */
        unsigned        receiveTimeStampNSec;   /* Unsigned ns timestamps */
        int             dummy[8];
   };

``mode``
  Indicates two different modes of operation. If set to ``1``, *ntpd* will read the shared memory
  twice and will only accept the timestamps if ``count`` hasn't changed in between. If set to
  ``0``, *ntpd* will accept the timestamps immediately. The page for `driver 28`_ provides a more
  detailed description.

``count``
  Sequential counter that indicates whether the shared memory has been read (by *ntpd*, subject to 
  setting of ``mode``) or written to.

``clockTimeStampSec`` and ``clockTimeStampUSec``
  The time received from an external devices (GSP, radio clock, whatever...) split into 
  seconds (``clockTimeStampSec``) and its microseconds (``clockTimeStampUSec``) fraction.

``receiveTimeStampSec`` and ``receiveTimeStampUSec``
  The system time when the external time was received, split into seconds (``receiveTimeStampSec``)
  and its microsecond (``receiveTimeStampUSec``) fraction. *ntpd* will compare the clock and receive
  times to work out the offset.

``leap``
  The leap second indicator can have any of the following four values to indicate that a leap
  second is imminent: ``0`` (no leap second), ``1`` (add second), ``2`` (delete second) and
  ``3`` (clock not in sync). These values are define in ``ntp.h`` of the *ntpd* source code.

``precision``
  According to the file ``ntpshm.h`` of the *gpsd* source code, the ``precision`` value is the
  log(2) value of the time source's jitter in seconds. Example values are ``-1`` (0.5 seconds = 2^-1),
  ``-2`` (0.25 seconds), ``-4`` (0.0625), ``-8`` (0.00390625).
``nsamples``
  According to one source_ this field is set by *ntpd* only. *gpsd* does not set ``nsamples`` either.
 
``valid``
  This field must be set to ``1`` (true) to indicate to *ntpd* that a new value has been written
  to the shared memory. 

``clockTimeStampNSec`` and ``receiveTimeStampNSec``
  Similar to ``clockTimeStampUSec`` and ``receiveTimeStampUSec`` but in nanoseconds instead of 
  microseconds. These fields were only introduced in *ntpd* version `4.2.7p303`_. In earlier versions
  they were part of the ``dummy`` field.

.. _source: http://stackoverflow.com/questions/11220627/ntp-shared-memory-driver-structure

**Note: One of the two next paragraphs will be removed once I have decided whether to use Python's ctypes_ or struct_ modules.**

The purpose of the shared memory driver is to allow other processes to pass time information
into *ntpd*. The most prominent implementation is probably `gpsd`_. The process can be described 
as shown below. The file ``ntpshmwrite.c`` of the *gspd* distribution provides an example in 
C code.

1. Read time from externel source (GPS, radio clock, ...).
2. Read the current system time.
3. Set ``valid`` to ``0``, i.e. false.
4. Set ``clockTimeStampSec``, ``clockTimeStampUSec`` and ``clockTimeStampNSec`` to the time
   read in step 1.
5. Set ``receiveTimeStampSec``, ``receiveTimeStampUSec`` and ``receiveTimeStampNSec`` to the system 
   time read in step 2.
6. Set ``leap`` as indicated by the external source or ``0`` if unknown.
7. Set ``precision``. 
8. Increase ``count``.
9. Set ``valid`` to ``1``, i.e. true.


The file ``ntpshmwrite.c`` of the *gspd* distribution provides an example in C code.

.. code-block:: c

   ...
   void ntp_write(volatile struct shmTime *shmseg,
               struct timedelta_t *td, int precision, int leap_notify)
   /* put a received fix time into shared memory for NTP */
   {
       struct tm tm;
      
       /* insist that leap seconds only happen in june and december
        * GPS emits leap pending for 3 months prior to insertion
        * NTP expects leap pending for only 1 month prior to insertion
        * Per http://bugs.ntp.org/1090 */
       (void)gmtime_r( &(td->real.tv_sec), &tm);
       if ( 5 != tm.tm_mon && 11 != tm.tm_mon ) {
           /* Not june, not December, no way */
           leap_notify = LEAP_NOWARNING;
       }
   
       /* we use the shmTime mode 1 protocol
        *
        * ntpd does this:
        *
        * reads valid.
        * IFF valid is 1
        *    reads count
        *    reads values
        *    reads count
        *    IFF count unchanged
        *        use values
        *    clear valid
        *
        */
   
       shmseg->valid = 0;
       shmseg->count++;
       /* We need a memory barrier here to prevent write reordering by
        * the compiler or CPU cache */
       memory_barrier();
       shmseg->clockTimeStampSec = (time_t)td->real.tv_sec;
       shmseg->clockTimeStampUSec = (int)(td->real.tv_nsec/1000);
       shmseg->clockTimeStampNSec = (unsigned)td->real.tv_nsec;
       shmseg->receiveTimeStampSec = (time_t)td->clock.tv_sec;
       shmseg->receiveTimeStampUSec = (int)(td->clock.tv_nsec/1000);
       shmseg->receiveTimeStampNSec = (unsigned)td->clock.tv_nsec;
       shmseg->leap = leap_notify;
       shmseg->precision = precision;
       memory_barrier();
       shmseg->count++;
       shmseg->valid = 1;
   }
   ...

.. _`gps`: http://www.catb.org/gpsd/gpsd-time-service-howto.html

