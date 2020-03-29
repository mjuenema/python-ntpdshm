/*
 *
 *
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "shm.h"


struct shmTime {
     int             mode; 
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


struct shmTime *shm_get(unsigned int unit, unsigned int shm_key_base) {
    int shmid;
    void *shm_time;

    // Try to create a new shared memory segment, in case ntpd has not started yet.
    shmid = shmget((key_t)(shm_key_base+unit), sizeof(struct shmTime), IPC_CREAT | IPC_EXCL | 0600);
    if (shmid < 0)
    {
        // Try to open an existing 
        shmid = shmget((key_t)(shm_key_base+unit), 0, 0600);
        if (shmid < 0) {
            return NULL;
        }
    }

    shm_time = (struct shmTime *)shmat(shmid, NULL, 0);
    if (shm_time == (void *)(-1)) {
        return NULL;
    }

    return shm_time;
}

int get_mode(struct shmTime *shm_time) {
    return shm_time->mode;
}

void set_mode(struct shmTime *shm_time, int mode) {
    shm_time->mode = mode;
}


int get_count(struct shmTime *shm_time) {
    return shm_time->count;
}

void set_count(struct shmTime *shm_time, int count) {
    shm_time->count = count;
}


int get_clockTimeStampSec(struct shmTime *shm_time) {
    return (int)shm_time->clockTimeStampSec;
}

void set_clockTimeStampSec(struct shmTime *shm_time, int clockTimeStampSec) {
    shm_time->clockTimeStampSec = (time_t)clockTimeStampSec;
}


int get_clockTimeStampUSec(struct shmTime *shm_time) {
    return shm_time->clockTimeStampUSec;
}

void set_clockTimeStampUSec(struct shmTime *shm_time, int clockTimeStampUSec) {
    shm_time->clockTimeStampUSec = clockTimeStampUSec;
}


unsigned int get_clockTimeStampNSec(struct shmTime *shm_time) {
    return shm_time->clockTimeStampNSec;
}

void set_clockTimeStampNSec(struct shmTime *shm_time, unsigned int clockTimeStampNSec) {
    shm_time->clockTimeStampNSec = clockTimeStampNSec;
}


int get_receiveTimeStampSec(struct shmTime *shm_time) {
    return (int)shm_time->receiveTimeStampSec;
}

void set_receiveTimeStampSec(struct shmTime *shm_time, int receiveTimeStampSec) {
    shm_time->receiveTimeStampSec = (time_t)receiveTimeStampSec;
}


int get_receiveTimeStampUSec(struct shmTime *shm_time) {
    return shm_time->receiveTimeStampUSec;
}

void set_receiveTimeStampUSec(struct shmTime *shm_time, int receiveTimeStampUSec) {
    shm_time->receiveTimeStampUSec = receiveTimeStampUSec;
}


unsigned int get_receiveTimeStampNSec(struct shmTime *shm_time) {
    return shm_time->receiveTimeStampNSec;
}

void set_receiveTimeStampNSec(struct shmTime *shm_time, unsigned int receiveTimeStampNSec) {
    shm_time->receiveTimeStampNSec = receiveTimeStampNSec;
}


int get_leap(struct shmTime *shm_time) {
    return shm_time->leap;
}

void set_leap(struct shmTime *shm_time, int leap) {
    shm_time->leap = leap;
}


int get_precision(struct shmTime *shm_time) {
    return shm_time->precision;
}

void set_precision(struct shmTime *shm_time, int precision) {
    shm_time->precision = precision;
}


int get_nsamples(struct shmTime *shm_time) {
    return shm_time->nsamples;
}

void set_nsamples(struct shmTime *shm_time, int nsamples) {
    shm_time->nsamples = nsamples;
}


int get_valid(struct shmTime *shm_time) {
    return shm_time->valid;
}

void set_valid(struct shmTime *shm_time, int valid) {
    shm_time->valid = valid;
}
