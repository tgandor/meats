#ifndef _INC_PROGRAM_H
#define _INC_PROGRAM_H

#include <malloc.h>
#include <string.h>
#include <stdio.h>

#include "astring.h"
#include "trim_directives.h"
#include "preprocess.h"
#include "atom.h"
#include "atom_codes.h"
#include "main.h"
#include "metrics.h"

/*
 * External variable declarations for parsers and lexers
 * ---
 *  Zewnêtrzne deklaracje zmiennych do komunikacji z analizatorami
 */
extern FILE *atpasin;
extern ATOM atpaslex();
extern void init_atpaslex();
extern struct metrics atpasMetrics;

extern FILE *atcin;
extern ATOM atclex();
extern void init_atclex();
extern struct metrics atcMetrics;

extern FILE *atbanin;
extern ATOM atbanlex();
extern void init_atbanlex();
extern struct metrics atbanMetrics;

enum program_type
{
  NONE,
  BANAL,
  C,
  /* CPP, */  /* possible future feature */
  PASCAL
};

struct program
{
  char *filename;
  char *source;
  ATOM *lex_atoms;
  int num_lex_atoms;
  enum program_type kind;
  struct metrics theMetrics;
};
typedef struct program* PROGRAM;

/*
 * Construct a program structure
 * ---
 *  Konstruktor klasy program
 */
PROGRAM new_program(char *filename);

void free_program(PROGRAM prog);

enum program_type identify_program(char *filename);

void output_program(PROGRAM prog);

int process_program(PROGRAM prog);

#endif
