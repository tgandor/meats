#ifndef _INC_ATOM_H
#define _INC_ATOM_H

#include <stdio.h>

struct atom
{
  int code;
  char *content; // redundant?
  int start;
  int len;
  int line;
};
typedef struct atom* ATOM;

extern const char *atom_names[];

void atom_info(const ATOM a);

#endif

