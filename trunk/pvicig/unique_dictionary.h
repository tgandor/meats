#ifndef _INC_UNIQUE_DICTIONARY_H
#define _INC_UNIQUE_DICTIONARY_H

#include <string.h>
#include <malloc.h>
#include <stdio.h>

struct dictionary_entry 
{
  struct dictionary_entry *next;
  char *word;
  int data;
};
typedef struct dictionary_entry* DICTIONARY_ENTRY;

struct unique_dictionary
{
	DICTIONARY_ENTRY entries;
	int count;
};
typedef struct unique_dictionary* UNIQUE_DICTIONARY;

void 
unique_dictionary_add(UNIQUE_DICTIONARY dictionary, const char *word);

/*
 * Constructor
 * ---
 *  Konstruktor
 */
UNIQUE_DICTIONARY
new_unique_dictionary();

/*
 * Destructor
 * ---
 *  Destruktor
 */
void 
free_unique_dictionary(UNIQUE_DICTIONARY dictionary);

DICTIONARY_ENTRY 
lookup_unique_dictionary(UNIQUE_DICTIONARY dictionary, const char *word);

void
output_unique_dictionary(UNIQUE_DICTIONARY dictionary);

int 
delete_from_unique_dictionary(UNIQUE_DICTIONARY dictionary, const char *word);

#endif
