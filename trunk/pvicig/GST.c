#include "GST.h"

/*
 * Adding a match to the queue
 * ---
 *  Dodawanie kandydata na kafel do kolejek
 */
static void record_match_private(QUEUES *queues, Match m, int update_pointer)
{
	QUEUES q = *queues, temp;
	/* queues empty -- pierwszy element */
	if (q == 0)
	{
		q = (QUEUES) malloc (sizeof(struct match_priority_queue));
		q->right = q->left = 0;
		q->first = q->last = 
			(struct match_item*) malloc (sizeof (struct match_item));
		q->first->next = 0;
    	q->first->match = m;
		q->L = m.L;
		/* 
		 * update pointer even if not asked
		 * zmieñ wska¼nik nawet je¿eli to nie by³o wskazane
		 */
		*queues = q;
		return;
	}
	/* scroll pointer left if match is bigger */
	if ( m.L > q->L )
	{
		while (q->L < m.L && q->left)
			q = q->left;
		if ( m.L > q->L ) /* still too big */
		{
			q->left = (QUEUES) malloc (sizeof(struct match_priority_queue));
			q->left->right = q;
			q = q->left;
			q->left = 0;
			q->L = m.L;
			q->first = q->last = 
				(struct match_item*) malloc (sizeof(struct match_item));
			q->first->next = 0;
			q->first->match = m;
			if (update_pointer)
				*queues = q;
			return;
		}
		else if ( m.L < q->L ) /* not as big */
		{
		  temp = (QUEUES) malloc (sizeof(struct match_priority_queue));
		  temp->right = q->right;
		  temp->left = q;
		  temp->L = m.L;
		  if ( temp->right )
		    temp->right->left = temp;
		  temp->first = temp->last =
				(struct match_item*) malloc (sizeof(struct match_item));
		  temp->first->next=0;
		  temp->first->match = m;
		  q->right = temp;
		  if (update_pointer)
			  *queues = temp;
		  return;
		}
	}
	else if ( m.L < q->L)
	{
		while (q->L > m.L && q->right)
			q = q->right;
		if ( m.L < q->L ) /* still too small */
		{
			q->right = (QUEUES) malloc (sizeof(struct match_priority_queue));
			q->right->left = q;
			q = q->right;
			q->right = 0;
			q->L = m.L;
			q->first = q->last = 
				(struct match_item*) malloc (sizeof(struct match_item));
			q->first->next = 0;
			q->first->match = m;
			if (update_pointer)
				*queues = q;
			return;
		}
		else if ( m.L > q->L ) /* not as small */
		{
		  temp = (QUEUES) malloc (sizeof(struct match_priority_queue));
		  temp->left = q->left;
		  temp->right = q;
		  temp->L = m.L;
		  if ( temp->left )
		    temp->left->right = temp;
		  temp->first = temp->last =
				(struct match_item*) malloc (sizeof(struct match_item));
		  temp->first->next=0;
		  temp->first->match = m;
		  q->left = temp;
		  if (update_pointer)
			  *queues = temp;
		  return;
		}
	}
	/* now we're almost there - on the right queue */
	assert(q->L == m.L);
	q->last->next = (struct match_item*) malloc (sizeof(struct match_item));
	q->last = q->last->next;
	q->last->next = 0;
	q->last->match = m;
	if (update_pointer)
		*queues = q;
}

/*
 * Wrapper for record_match, updates current queue
 * ---
 *  Opakowanie dla record_match, zmienia wska¼nik aktualny
 */
void record_match(QUEUES *queues, Match m)
{
	record_match_private(queues, m, 1);
}

/*
 * Wrapper for record_match, updates not current queue
 * ---
 *  Opakowanie dla record_match, nie zmienia wska¼nika
 */
void replace_match(QUEUES *queues, Match m)
{
	record_match_private(queues, m, 0);
}

/*
 * Fetch next maximal match
 * ---
 *  Wyci±gniêcie nastêpnego maksymalnego dopasowania z kolejek
 */
struct match_item * remove_match(QUEUES *queues)
{
	QUEUES q = *queues, temp;
	struct match_item *ret;
	/* Check if we have any elements */
	if (!q)
		return 0;
	/* Scroll to the leftmost queue */
	while (q->left)
		q = q->left;
    ret = q->first;
	q->first = q->first->next;
	/* Current queue emptied */
	if ( !q->first )
	{
		temp = q;
		q = q->right;
		if (q)
			q->left = 0;
		free(temp);
	}
	*queues = q;
	return ret;
}

/*
 * Empty the queues from maximal matches (doubling s)
 * ---
 *  Opró¿nienie kolejek przed podwojeniem s
 */
static void dispose_queues(QUEUES *queues)
{
	QUEUES q = *queues, nq;
	struct match_item *temp;
	if (!q)      /* nothing to dispose - kolejki i tak s± puste */
		return;
	while (q->left)
		q = q->left;
	while(q)
	{
		temp = q->first;
		while(q->first)
		{
			temp = q->first;
			q->first=q->first->next;
			free(temp);
		}
		nq = q;
		q = q->right;
		free(nq);
	}
	*queues = 0;
}

/*
 * Top level algorithm
 * ---
 *  G³ówny algorytm GST i inicjalizacja
 */
TILES perform_GST(ATOM *pattern_atoms, int lp, ATOM *text_atoms, int lt)
{
	TILES temp;
	/* initial search length */
	int s = GST_initial;
	/* maximal length of found match */
	int L_max;
	/* 
	 * Initialize GST control structure (class)
	 * ---
	 *  Inicjalizacja struktury steruj±cej algorytmem GST
	 */
	GST gst = (GST) malloc (sizeof(*gst));
	gst->p_marks = calloc(lp+1, sizeof(int));
	gst->p_marks[lp] = 1; 
	gst->t_marks = calloc(lt+1, sizeof(int));
	gst->t_marks[lt] = 1;
	gst->theTiles = (TILES) calloc(1, sizeof(struct tiles));
	gst->T = text_atoms;
	gst->P = pattern_atoms;
	gst->lp = lp;
	gst->lt = lt;
	gst->theQ = 0;

	for(;;)
	{
		L_max = scan_patterns(s, gst);
		if ( L_max > 2 * s )
			s = L_max;
		else
		{
			mark_strings(s, gst);
			if ( s > 2 * GST_shortest )
				s /= 2;
			else if ( s > GST_shortest )
				s = GST_shortest;
			else 
				break;
		}
	}
	temp = gst->theTiles;
	free(gst->t_marks);
	free(gst->p_marks);
	free(gst);
	return temp;
}

/*
 * Scan patterns - using Running Karp-Rabin and hashtable
 * ---
 *  Operacja scan patterns - z wykorzystaniem RKR i tablicy haszuj±cej
 */

struct link
{
  int key;
  int val;
  struct link *next;
};

struct chain
{
  int count;
  struct link *first;
  struct link *last;
};

/*
 * Check if n is prime
 * ---
 *  Sprawd¼, czy n jest liczb± pierwsz±
 */
int is_prime (int n)
{
  int i=3;
  if ( n % 2 == 0 )
    return 0;
  while(i*i <= n)
  {
    if (n % i == 0)
      return 0;
    i += 2;
  }
  return 1;
}

/*
 * Searches for a prime >= n
 * ---
 *  Najbli¿sza wiêksza liczba pierwsza
 */
static int find_appropriate_prime(int lower_bound)
{
  while ( ! is_prime(lower_bound) )
    ++lower_bound;
  return lower_bound;
}

/*
 * Raising a number to power in modular arithmetics
 * ---
 *  Podniesienie do potêgi w ciele Galois
 */
static int modular_power(int base, int exponent)
{
  int result=1, factor=base;
  while ( exponent ) 
  {
    if ( exponent & 1 )
	  result = result * factor % KR_modulus;
	factor = factor * factor % KR_modulus;
	exponent /= 2;
  }
  return result % KR_modulus;
}

/*
 * Hash function for hashtable
 * ---
 *  Funkcja haszuj±ca dla tablicy haszuj±cej
 */
static int h(int key, int N)
{
  return key * key % N;
}

/*
 * Search for possible matches with Karp Rabin
 * ---
 *  Szukaj potencjalnych dopasowañ algorytmem Karpa Rabina
 */
int scan_patterns(int s, GST gst)
{
	int k, max_len=0;
	int t, p;
	int last_hash = -2;
	int hash;
	int bs = modular_power(KR_base, s-1);
	int mbs = bs ? KR_modulus - bs : 0;
	int hash_modulus = find_appropriate_prime(gst->lt);
	struct link **hashtab = (struct link **) calloc(hash_modulus, sizeof(struct link*));
	int position;
	struct link *hash_link;
	int recorded = 0;
	
	t=0; 
	while (t + s <= gst->lt)
	{
		if(gst->t_marks[t] || gst->t_marks[t+s-1]) 
		{
			t++;
			continue;
		}
		
		if (t == last_hash+1) /* quick hashing */
		{
			hash = ((hash + mbs * gst->T[t-1]->code) * KR_base + gst->T[t+s-1]->code) % KR_modulus;
		}
		else                 /* complete hashing */
		{
			int i, thash = gst->T[t]->code;
			for (i=1; i<s; i++)
			{
				thash = (thash * KR_base % KR_modulus + gst->T[t+i]->code) % KR_modulus;
			}
			hash = thash;
		}
		last_hash = t;
		hash_link = (struct link*) alloca(sizeof(struct link));
		hash_link->key = hash;
		hash_link->val = t;
		position = h(hash, hash_modulus);
		hash_link->next = hashtab[position];
		hashtab[position] = hash_link;
		t++;
	}

	p=0;
	last_hash = -2;
	while (p + s <= gst->lp)
	{
		if(gst->p_marks[p] || gst->p_marks[p+s-1])
		{
			p++;
			continue;
		}	
		
		if (p == last_hash+1) /* quick hashing */
		{
			hash = ((hash + mbs * gst->P[p-1]->code) * KR_base + gst->P[p+s-1]->code) % KR_modulus;
		}
		else                 /* complete hashing */
		{
			int i, thash = gst->P[p]->code;
			for (i=1; i<s; i++)
			{
				thash = (thash * KR_base % KR_modulus + gst->P[p+i]->code) % KR_modulus;
			}
			hash = thash;
		}
		last_hash = p;
		position = h(hash, hash_modulus);
		hash_link = hashtab[position];
		while ( hash_link )
		{
			int L=s;
			int t = hash_link->val;
			Match m = {p, t, 0};
			while( !gst->t_marks[t+L] && !gst->p_marks[p+L] )
			{
				if( gst->T[t+L]->code == gst->P[p+L]->code )
					++L;
				else
					break;
			}
			if (L > 2 * s)
			{
				int i, hit = 1;
				for (i=s-1; i>=0; i--)
					if( gst->T[t+i]->code != gst->P[p+i]->code )
					{
						hit=0;
						break;
					}
				if (hit)
				{
					free(hashtab);
					dispose_queues(&gst->theQ);
					return L;
				}
			}
			else
			{
				m.L = L;
				if ( L > max_len )
					max_len = L;
				record_match(&gst->theQ, m);
				++recorded;
			}
			hash_link = hash_link->next;
		}
		p++;
	}
	free(hashtab);
	/* fprintf(stderr, "Recorded matches: %d, for s=%d\n", recorded, s); */
	return max_len;
}

int match_occluded(Match *m, GST gst)
{
	if (gst->t_marks[m->t] || gst->p_marks[m->p]
			|| gst->t_marks[m->t+m->L-1]
			|| gst->p_marks[m->p+m->L-1] )
	{
		int L = m->L, pref=0;
		/* check occluded ending (reduce length) */
		while(L >= 0 && (gst->t_marks[m->t+L-1] || gst->p_marks[m->p+L-1] ) )
			--L;
		if (L < GST_shortest)
		{
			m->L = 0;  // make sure it won't be considered
			return 1;  // upewniamy siê, ¿e na pewno nie bêdzie wykorzystane
		}
		/* check occluded prefix */
		while(pref < L && (gst->t_marks[m->t+pref] || gst->p_marks[m->p+pref]) )
			++pref;
		m->p += pref;
		m->t += pref;
		m->L = L - pref;
		return 1;
	}
	return 0;
}

void mark_strings(int s, GST gst)
{
	struct match_item *mi;
	while( mi = remove_match(&gst->theQ) )
	{
		if ( !match_occluded(&mi->match, gst) )
		{
			int hit = 1, i;
			Match m = mi->match;
			for(i=0; i<s; i++)
			  if (gst->T[m.t+i]->code != gst->P[m.p+i]->code)
			  {
			    hit=0;   /* hash artifact  -- kolizja haszowania */
			    break;
			  }
			if ( hit )
			{
				TILE myTile = malloc(sizeof(struct tile));
				myTile->L = m.L;
				myTile->p_atoms = &gst->P[m.p];
				myTile->t_atoms = &gst->T[m.t];
				myTile->next = 0;
				if(gst->theTiles->first)
				{
					gst->theTiles->last->next = myTile;
					gst->theTiles->last = myTile;
				}
				else
				{
					gst->theTiles->first = myTile;
					gst->theTiles->last = myTile;
				}
				gst->theTiles->num++;
				gst->theTiles->sum_lengths += m.L;
				/* 
				 * marking tokens
				 * ---
				 *  zaznaczanie atomów
				 */
				for (i=0; i<m.L; i++) 
				{
				  gst->t_marks[m.t+i] = 1;
				  gst->p_marks[m.p+i] = 1;
				}
			}
		}
		else if ( mi->match.L >= s )
			replace_match(&gst->theQ, mi->match);
		free(mi);
	}
}

/*
 * For special assignments
 */
void output_match(Match m)
{
  printf("(%d, %d, %d) ", m.t, m.p, m.L);
}

void output_tile(TILE t)
{
	int i;
	printf(_("Atoms: "));
	for(i=0; i<t->L; i++)
		printf("%s ", atom_names[t->p_atoms[i]->code]);
	printf("\n");
}
