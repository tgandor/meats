#ifndef _INC_GST_H
#define _INC_GST_H

#include <malloc.h>
#include <alloca.h>
#include <stdio.h>
#include <assert.h>

#include "atom.h"
#include "main.h"

struct tile
{
	ATOM *p_atoms;
	ATOM *t_atoms;
	int L;
	struct tile *next;
};
typedef struct tile * TILE;

struct tiles
{
	TILE first;
	TILE last;
	int num;
	int sum_lengths;
};
typedef struct tiles * TILES;

struct match
{
	/* pattern pointer -- miejsce w tek¶cie wzorca */
	int p;
	/* text pointer -- miejsce w tek¶cie */
	int t;
	/* match length -- d³ugo¶æ dopasowania */
	int L;
};
typedef struct match Match;

struct match_item
{
	Match match;
	struct match_item *next;
};

struct match_priority_queue
{
	int L;
	struct match_priority_queue *left;
	struct match_priority_queue *right;
	struct match_item *first;
	struct match_item *last;
};
typedef struct match_priority_queue * QUEUES;

struct greedy_string_tiling
{
	/* length of pattern, length of text */
	int lp, lt;
	/* marks for already tiled sequences */
	int *p_marks;
	int *t_marks;
	/* pointers to arrays of atoms */
	ATOM *P;
	ATOM *T;
	/* matches queue */
	QUEUES theQ;
	/* recorded tiles */
	TILES theTiles;
};
typedef struct greedy_string_tiling *GST;

void record_match(QUEUES *queues, Match m);

struct match_item * remove_match(QUEUES *queues);

TILES perform_GST(ATOM *pattern_atoms, int lp, ATOM *text_atoms, int lt);

int scan_patterns(int s, GST gst);

void mark_strings(int s, GST gst);

void output_match(Match m);

int is_prime (int n);

void output_tile(TILE t);

#endif
