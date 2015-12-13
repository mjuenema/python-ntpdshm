%module ntpdshm

%{
#include "ntpdshm.h"
%}

struct shmTime *shm_get(unsigned int unit);
