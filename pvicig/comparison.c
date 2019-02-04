#include "comparison.h"

/*
 * A callback function to sort comparisons descending
 * --
 *  Funkcja zwrotna do sortowania porównañ w porz±dku malej±cym
 */
#define min(a,b) (a<b?a:b)
#define max(a,b) (a<b?b:a)
static void calculate_score(COMPARISON c)
{
  int A, B, AB;
  int numMetrics=0;
  double gstScore, metricScore;
  /*
   * Checking for verbatim identity
   * ---
   *  Sprawdzanie dos³ownej identyczno¶ci
   */
  if ( c->identity )
  {
    c->overall = 1.0;
    return;
  }
  /*
   * Calculating simmilarity via GST
   * ---
   * Obliczanie podobieñstwa kafli
   */
  if ( use_metric != 2 )
  {
    A = c->a->num_lex_atoms;
    B = c->b->num_lex_atoms;
    AB = c->atom_tiles->sum_lengths;
    gstScore = (double) 2 * AB / (A+B);
  }
  if ( use_metric )
  {
	  int num_metrics = sizeof(struct metrics) / sizeof(int), i;
	  int *metr_a = (int*) &c->a->theMetrics;
	  int *metr_b = (int*) &c->b->theMetrics;
	  for(i=0; i < num_metrics; i++)
	  {
		 if ( zeros_matter )
		 {
			 if (metr_b[i] == metr_a[i])
			 {
				 metricScore += 1;
			 }
			 else
			 {
				 metricScore += (double)min(metr_a[i], metr_b[i]) / (double)max(metr_a[i], metr_b[i]);
			 }
			 numMetrics++;
		 }
		 else if ( metr_b[i] && metr_a[i] )
		 {
		   metricScore += (double)min(metr_a[i], metr_b[i]) / (double)max(metr_a[i], metr_b[i]);
           numMetrics++;
		 }
	  }
	  if (numMetrics)
	    metricScore /= (double) numMetrics;
	  else
        metricScore = 0;
  }
  switch ( use_metric )
  {
  case 2:
    c->overall = metricScore;
	break;
  case 1:
    c->overall = (gstScore + metricScore) / 2;
	break;
  default:
    c->overall = gstScore;
	break;
  }
}

/*
 * Callback function for qusort used to compare values
 * ---
 *  Funkcja pomocnicza dla sortowania szybkiego realizuj±ca porównanie
 */
int compare_comparison(const void * a, const void * b)
{
	const COMPARISON ca = *(const COMPARISON*)a;
	const COMPARISON cb = *(const COMPARISON*)b;
	/* ascending: see below -- rosn±co: poni¿ej */
	if ( sort_asc )
	  return (ca->overall > cb->overall) - (ca->overall < cb->overall);
	/* for descending sort -- do sortowania malej±co */
	return (ca->overall < cb->overall) - (ca->overall > cb->overall);
}

void print_substring(char *string, int from, int to)
{
	// printf("Substr: %s,\n from %d - to %d\n", string, from, to);
	for ( ; from < to; from++)
		putchar(string[from]);
	printf("\n");
}

void output_tiles(COMPARISON comp, TILES t)
{
	int i=1;
	TILE tile = t->first;
	printf(_("Number of tiles: %d\n"), t->num);
	while (tile)
	{
		printf("%d:\n", i++);
		output_tile(tile);
		printf(_("Fragment of %s:\n"), comp->a->filename);
	    print_substring(comp->a->source,
				tile->p_atoms[0]->start,
				tile->p_atoms[tile->L-1]->start + tile->p_atoms[tile->L-1]->len);
		printf(_("Fragment of %s:\n"), comp->b->filename);
	    print_substring(comp->b->source,
				tile->t_atoms[0]->start,
				tile->t_atoms[tile->L-1]->start + tile->t_atoms[tile->L-1]->len);
		tile = tile->next;
	}
}

static char *percentage(int a, int b)
{
	static char buf[50];
	if ( !a && !b && zeros_matter )
	{
		sprintf(buf, "100");
		return buf;
	}
	if ( !zeros_matter && (!a || !b) )
	{
		sprintf(buf, "---");
		return buf;
	}
	sprintf(buf, "%5.2f", (double)min(a,b) / (double)max(a,b) * 100);
	return buf;
}

void output_comparison(COMPARISON comp)
{
	puts("--------------------------------------------------------");
	printf("%s\t-\t%s\t%6.2f%%\n", comp->a->filename, comp->b->filename, comp->overall*100);
	if ( ! quiet_flag )
	{
	  printf(_("\tTiles: %d, Sum: %d\n"), comp->atom_tiles->num, comp->atom_tiles->sum_lengths);
	  if ( use_metric != 2 )
  		output_tiles(comp, comp->atom_tiles);
  	  if ( use_metric )
	  {
		printf(_("Metrics values: \n"));
	    int num_metrics = sizeof(struct metrics) / sizeof(int), i;
	    int *metr_a = (int*) &comp->a->theMetrics;
	    int *metr_b = (int*) &comp->b->theMetrics;
	    for(i=0; i < num_metrics; i++)
			printf("  %4d - %4d  %10s %%\n", metr_a[i], metr_b[i], percentage(metr_a[i], metr_b[i]));
	  }
	}
}

COMPARISON compare_programs(struct program * a, struct program * b)
{
	/*
	 * Initialization
	 * ---
	 *  Inicjalizacja
	 */
	COMPARISON ret = (COMPARISON) malloc (sizeof(*ret));
	if (!quiet_flag)
		fprintf(stderr, _("Comparing %s and %s\n"), a->filename, b->filename);
	ret->a = a;
	ret->b = b;

	/*
	 * Processing
	 * ---------------------------------------------
	 *  Przetwarzanie
	 */

	/*
	 * Testing for verbatim identity
	 * ---
	 *  Sprawdzanie dos³ownej identyczno¶ci
	 */
	ret->identity = !strcmp(a->source, b->source);

	/*
	 * Performing GST on lexical atoms
	 * ---
	 *  Wykonanie algorytmu GST na atomach leksykalnych
	 */
	ret->atom_tiles = perform_GST(a->lex_atoms, a->num_lex_atoms, b->lex_atoms, b->num_lex_atoms);

	/*
	 * Final calculation
	 * ---
	 *  Obliczenie koñcowego wyniku
	 */
	calculate_score(ret);
	return ret;
}

