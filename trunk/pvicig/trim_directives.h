#ifndef _INC_TRIM_DIRECTIVES_H
#define _INC_TRIM_DIRECTIVES_H

#include <regex.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <assert.h>

char* trim_directives(char *source);
void trim_directives_from(char **source);
char *trim_all_directives(char *source);

static const char *neccessary_directives[] =
{
	"if",
	"ifdef",
	"ifndef",
	"elif",
	"else",
	"endif",
	"define",
	"undef",
};
#define NUM_DIRECTIVES (sizeof(neccessary_directives)/sizeof(neccessary_directives[0]))

#endif

