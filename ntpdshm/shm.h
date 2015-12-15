/*
 *
 *
 *
 */

struct shmTime *shm_get(unsigned int unit);
int get_mode(struct shmTime *shm_time);
void set_mode(struct shmTime *shm_time, int mode);
int get_count(struct shmTime *shm_time);
void set_count(struct shmTime *shm_time, int count);
int get_clockTimeStampSec(struct shmTime *shm_time);
void set_clockTimeStampSec(struct shmTime *shm_time, int clockTimeStampSec);
int get_clockTimeStampUSec(struct shmTime *shm_time);
void set_clockTimeStampUSec(struct shmTime *shm_time, int clockTimeStampUSec);
unsigned int get_clockTimeStampNSec(struct shmTime *shm_time);
void set_clockTimeStampNSec(struct shmTime *shm_time, unsigned int clockTimeStampNSec);
int get_receiveTimeStampSec(struct shmTime *shm_time);
void set_receiveTimeStampSec(struct shmTime *shm_time, int receiveTimeStampSec);
int get_receiveTimeStampUSec(struct shmTime *shm_time);
void set_receiveTimeStampUSec(struct shmTime *shm_time, int receiveTimeStampUSec);
unsigned int get_receiveTimeStampNSec(struct shmTime *shm_time);
void set_receiveTimeStampNSec(struct shmTime *shm_time, unsigned int receiveTimeStampNSec);
int get_leap(struct shmTime *shm_time);
void set_leap(struct shmTime *shm_time, int leap);
int get_precision(struct shmTime *shm_time);
void set_precision(struct shmTime *shm_time, int precision);
int get_nsamples(struct shmTime *shm_time);
void set_nsamples(struct shmTime *shm_time, int nsamples);
int get_valid(struct shmTime *shm_time);
void set_valid(struct shmTime *shm_time, int valid);

