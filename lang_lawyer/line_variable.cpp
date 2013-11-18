#include <stdio.h>

// test with e.g. gcc -E

#define CAT(a, b) CAT2(a, b)
#define CAT2(a, b) CAT3(~, a ## b)
#define CAT3(a, b) b

#define FOR(ii, ll, uu) int CAT(FORlim, __LINE__) = (uu); for(int ii = (ll); ii < CAT(FORlim, __LINE__); ++ii)
#define REP(ii, nn) FOR(ii, 0, nn)

// not even CAT2 ...
#define WLINE(x) CAT(x, __LINE__)

int main()
{
	int WLINE(i) = 1;
	int WLINE(i) = 2;
	REP(i, 3) puts("La");
	REP(i, 2) puts("La-la");
	return 0;
}
