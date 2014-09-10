#include <stdio.h>

#define FOR(ii, ll, uu)  for(int ii##lim = (uu), ii = (ll); ii < ii##lim; ++ii)
#define REP(ii, nn) FOR(ii, 0, nn)

inline int gis()
{
	int n = 0;
	int ch = getchar_unlocked(), sign = 0;
	while (ch < '0' || ch > '9')
	{
		if (ch == '-') sign=-1;
		ch = getchar_unlocked();
	}
	while (ch >= '0' && ch <= '9')
		n = (n<<3)+(n<<1) + ch-'0', ch = getchar_unlocked();
	return sign ? -n : n;
}
#define GI (gis())

inline int giu()
{
	int n = 0;
	int ch=getchar_unlocked();
	while (ch < '0' || ch > '9')
	{
		ch = getchar_unlocked();
	}
	while (ch >= '0' && ch <= '9')
		n = (n<<3)+(n<<1) + ch-'0', ch = getchar_unlocked();
	return n;
}
#define GU (giu())


inline int ins(char *buf)
{
	int ch = getchar_unlocked();
	while (ch <= ' ')
	{
		if ((ch = getchar_unlocked()) == -1)
			return 0;
	}
	char *oldbuf = buf;
	while (ch > ' ')
	{
		*buf++ = ch;
		ch = getchar_unlocked();
	}
	*buf = '\0';
	return (int)(buf-oldbuf);
}


int main()
{
	return 0;
}
