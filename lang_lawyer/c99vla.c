#include <stdio.h>

#define FOR(ii, ll, uu)  for(int ii##lim = (uu), ii = (ll); ii < ii##lim; ++ii)
#define REP(ii, nn) FOR(ii, 0, nn)

int main()
{
	int n = 0;
	printf("# elements? ");
	scanf("%d", &n);
	int buf[n];
	REP(i, n)
		scanf("%d", &buf[i]);
	puts("In reverse:");
	REP(i, n)
		printf("%d\n", buf[n-1-i]);
	return 0;
}
