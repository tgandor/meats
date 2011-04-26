#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <algorithm>

using namespace std;

#define SIZ 23170
char siv[SIZ];
int fp[SIZ];
int np;

/* read code first; when in trouble, more comments below */

int main() {
  int t=0;
  int lim = sqrt(SIZ);
  for(int i=1; i<lim; ++i) {
    if ( !siv[i] ) {
      int step = 2*i+1;
      for(int j=step*step/2; j<SIZ; j+=step)
        siv[j] = 1;
    }
  }
  for(int i=1; i<SIZ; ++i) 
    if ( !siv[i] ) fp[np++] = 2*i+1;
  scanf("%d", &t);
  while(t--) {
    int L, U;
    scanf("%d%d", &L, &U);

    // the number 2
    if ( L == 2 ) printf("%d\n", L++);
    if ( L > U ) continue;

    // numbers 3..fp[np-1]
    if ( L < fp[np-1] ) {
      int *pp = lower_bound(fp, fp+np, L);
      while(pp < fp+np && *pp <= U) {
        printf("%d\n", *pp++);
      }
      if ( pp < fp+np ) continue;
      L = *--pp + 2;
    }
    if ( ~L&1 ) ++L;
    if ( ~U&1 ) --U;
    if ( L > U ) continue;

    // hard sieving ;)
    int sl = (U-L)/2 + 1;
    char *s = (char*)calloc(sl, 1);
    int lim = sqrt(U)+1;
    for(int *pp=fp; *pp < lim; ++pp) {
      int p = *pp;
      for(int j=(2*p - (L+p)%(2*p))/2%p; j<sl; j += p) 
        s[j] = 1;
    }
    for(int i=0; i<sl; ++i) 
      if ( !s[i] ) printf("%d\n", L+2*i);
    free(s);
  }
  return 0;
}
/* 
   This is a toy program to print all primes no smaller than L
   and no greater than U. It reads the number of pairs (L, U)
   as the first integer in the input, and expects a corresponding
   number of integer pairs thereafter.

   The number 2 has a special case at the very beginning. Then 
   there follows a collection of first primes fp, which are taken
   from a sieve of size SIZ. The size of fp is an overkill added 
   later (on archivization), it should be enough to hold all primes
   in the sieve of size SIZ. This collection is binary searched
   and printed one by one.

   Finally, a sieve large enough is allocated and it is sieved by
   the first primes from fp (it only deals with odd numbers, btw.).
   Then the sieve is scanned (I see no way of printing it while scanning, 
   because there is no if(!siv[i]), as we're not sieving from the 
   beginning.

   This works correct, of course, if U < SIZ*SIZ (adjust SIZ for 
   that). I suppose this is not susceptible for arithmetic overflow,
   because we're just making the numbers smaller or closer to each
   other. The only limit I see (e.g. for 64 bits etc.) is that
   the arrays may get too big, and sieving will take forever.
 */

