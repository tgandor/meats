#ifndef _INC_COMPARISON_H
#define _INC_COMPARISON_H

#include <stdio.h>
#include <malloc.h>

#include "program.h"
#include "GST.h"

/*
 * A structure holding the results of a comparison of programs
 * ---
 *  Struktura z wynikiem por�wnania dw�ch program�w
 */
struct comparison
{
	/*
	 * The complete score of the comparison - a number between 0 and 1
	 * ---
	 *  Warto�� podobie�stwa program�w - liczba z przedzia�u [0, 1]
	 */
	double overall;
	/*
	 * The flag indicating a verbatim copy
	 * ---
	 *  Zmienna logiczna wskazuj�ca na kopi� dos�own�
	 */
	int identity;

	/*
	 * A set of tiles as a result of Greedy String Tiling
	 * ---
	 *  Struktura zawieraj�ca kafle pochodz�ce z GST
	 */
	struct tiles * atom_tiles; 
	
	/*
	 * pointers to compared programs 
	 * ---
	 *  wska�niki do por�wnywanych program�w 
	 */
	struct program *a;
	struct program *b;
};
typedef struct comparison * COMPARISON;

int compare_comparison(const void * a, const void * b);

COMPARISON compare_programs(struct program * a, struct program * b);

void output_tiles(COMPARISON comp, struct tiles * t);

#endif
