/*
 *
 *
 *
 */

struct shmTime *_shm_get(unsigned int unit);
int _get_mode(struct shmTime *shm_time);
void _set_mode(struct shmTime *shm_time, int mode);
int _get_count(struct shmTime *shm_time);
void _set_count(struct shmTime *shm_time, int count);
int _get_clockTimeStampSec(struct shmTime *shm_time);
void _set_clockTimeStampSec(struct shmTime *shm_time, int clockTimeStampSec);
int _get_clockTimeStampUSec(struct shmTime *shm_time);
void _set_clockTimeStampUSec(struct shmTime *shm_time, int clockTimeStampUSec);
unsigned int _get_clockTimeStampNSec(struct shmTime *shm_time);
void _set_clockTimeStampNSec(struct shmTime *shm_time, unsigned int clockTimeStampNSec);
int _get_receiveTimeStampSec(struct shmTime *shm_time);
void _set_receiveTimeStampSec(struct shmTime *shm_time, int receiveTimeStampSec);
int _get_receiveTimeStampUSec(struct shmTime *shm_time);
void _set_receiveTimeStampUSec(struct shmTime *shm_time, int receiveTimeStampUSec);
unsigned int _get_receiveTimeStampNSec(struct shmTime *shm_time);
void _set_receiveTimeStampNSec(struct shmTime *shm_time, unsigned int receiveTimeStampNSec);
int _get_leap(struct shmTime *shm_time);
void _set_leap(struct shmTime *shm_time, int leap);
int _get_precision(struct shmTime *shm_time);
void _set_precision(struct shmTime *shm_time, int precision);
int _get_nsamples(struct shmTime *shm_time);
void _set_nsamples(struct shmTime *shm_time, int nsamples);
int _get_valid(struct shmTime *shm_time);
void _set_valid(struct shmTime *shm_time, int valid);

