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
#include "ntpdshm.h"

#define NTPD_SHM_KEY 0x4e545030


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


struct shmTime *_shm_get(unsigned int unit) {
    int shmid;
    void *p;

    shmid = shmget(NTPD_SHM_KEY+unit, sizeof(struct shmTime), 0 | 0666);
    if (shmid < 0)
    {
        return NULL;
    }

    shm_time = (struct shmTime *)shmat (shmid, 0, 0);
    if (shm_time == (char *)(-1)) {
        return NULL;
    }

    return shm_time;
}

int _get_mode(struct shmTime *shm_time) {
    return shm_time->mode;
}

void _set_mode(struct shmTime *shm_time, int mode) {
    shm_time->mode = mode;
}


int _get_count(struct shmTime *shm_time) {
    return shm_time->count;
}

void _set_count(struct shmTime *shm_time, int count) {
    shm_time->count = count;
}


int _get_clockTimeStampSec(struct shmTime *shm_time) {
    return shm_time->clockTimeStampSec;
}

void _set_clockTimeStampSec(struct shmTime *shm_time, int clockTimeStampSec) {
    shm_time->clockTimeStampSec = clockTimeStampSec;
}


int _get_clockTimeStampUSec(struct shmTime *shm_time) {
    return shm_time->clockTimeStampUSec;
}

void _set_clockTimeStampUSec(struct shmTime *shm_time, int clockTimeStampUSec) {
    shm_time->clockTimeStampUSec = clockTimeStampUSec;
}


unsigned int _get_clockTimeStampNSec(struct shmTime *shm_time) {
    return shm_time->clockTimeStampNSec;
}

void _set_clockTimeStampNSec(struct shmTime *shm_time, unsigned int clockTimeStampNSec) {
    shm_time->clockTimeStampNSec = clockTimeStampNSec;
}


int _get_receiveTimeStampSec(struct shmTime *shm_time) {
    return shm_time->receiveTimeStampSec;
}

void _set_receiveTimeStampSec(struct shmTime *shm_time, int receiveTimeStampSec) {
    shm_time->receiveTimeStampSec = receiveTimeStampSec;
}


int _get_receiveTimeStampUSec(struct shmTime *shm_time) {
    return shm_time->receiveTimeStampUSec;
}

void _set_receiveTimeStampUSec(struct shmTime *shm_time, int receiveTimeStampUSec) {
    shm_time->receiveTimeStampUSec = receiveTimeStampUSec;
}


unsigned int _get_receiveTimeStampNSec(struct shmTime *shm_time) {
    return shm_time->receiveTimeStampNSec;
}

void _set_receiveTimeStampNSec(struct shmTime *shm_time, unsigned int receiveTimeStampNSec) {
    shm_time->receiveTimeStampNSec = receiveTimeStampNSec;
}


int _get_leap(struct shmTime *shm_time) {
    return shm_time->leap;
}

void _set_leap(struct shmTime *shm_time, int leap) {
    shm_time->leap = leap;
}


int _get_precision(struct shmTime *shm_time) {
    return shm_time->precision;
}

void _set_precision(struct shmTime *shm_time, int precision) {
    shm_time->precision = precision;
}


int _get_nsamples(struct shmTime *shm_time) {
    return shm_time->nsamples;
}

void _set_nsamples(struct shmTime *shm_time, int nsamples) {
    shm_time->nsamples = nsamples;
}


int _get_valid(struct shmTime *shm_time) {
    return shm_time->valid;
}

void _set_valid(struct shmTime *shm_time, int valid) {
    shm_time->valid = valid;
}
