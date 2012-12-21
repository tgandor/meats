#ifndef _INC_MAIN_H
#define _INC_MAIN_H

/*
 * Standard and GNU libraries
 * ---
 *  Biblioteki standardowe i GNU
 */
#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <locale.h>
#include <libintl.h>
#include <limits.h>

/*
 * Non standard includes 
 * ---
 *  Pozosta³e nag³ówki
 */
#include "comparison.h"
#include "program.h"
#include "unique_dictionary.h"
#include "GST.h"

/*
 * Program global variables - control options
 * ---
 *  Zmienne globalne programu - opcje steruj±ce
 */

extern int verbose_flag;
extern int quiet_flag;

extern int KR_base;
extern int KR_modulus;

extern int GST_initial;
extern int GST_shortest;

extern int use_metric;
extern int zeros_matter;
extern int use_cpp;

extern int output_source;
extern int sort_asc;

int 
report(char *error);

int 
babble(char *message);

/*
 * Gettext macros
 * ---
 *  Makra biblioteki gettext
 */
#define _(str) gettext(str)
#define N_(str) (str)

/*
 * Constants to configure
 * --
 *  Sta³e konfiguracyjne
 */

#ifndef LOCALEDIR
  #define LOCALEDIR "/usr/share/locale"
#endif

#ifndef DEFAULT_KR_BASE
  #define DEFAULT_KR_BASE 3
#endif

#ifndef DEFAULT_KR_MODULUS
  #define DEFAULT_KR_MODULUS 61
#endif

#ifndef DEFAULT_GST_INITIAL
  #define DEFAULT_GST_INITIAL 20
#endif

#ifndef DEFAULT_GST_SHORTEST
  #define DEFAULT_GST_SHORTEST 10
#endif

#endif
