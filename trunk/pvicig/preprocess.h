#ifndef _INC_PREPROCESS_H
#define _INC_PREPROCESS_H

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#include "astring.h"

char *preprocess(char *source);
void preprocess_from(char **source);

#endif
