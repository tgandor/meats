#include <stdio.h>

#define FOR(ii, ll, uu)  for(int ii##lim = (uu), ii = (ll); ii < ii##lim; ++ii)
#define REP(ii, nn) FOR(ii, 0, nn)
#define GI ({int t; scanf("%d", &t); t;})

// from stackoverflow
#define getcx getchar_unlocked
inline void inp(int &n)
{
	n=0;
	int ch=getcx(), sign=1;
	while (ch < '0' || ch > '9')
	{
		if (ch=='-') sign=-1;
		ch = getcx();
	}
	while (ch >= '0' && ch <= '9')
		n = (n<<3)+(n<<1) + ch-'0', ch=getcx();
	n = n * sign;
}

#define GI2 ({int t; inp(t); t;})

inline int ins(char *buf)
{
	int ch=getcx();
	while (ch <= ' ')
	{
		if ((ch = getcx()) == -1)
			return 0;
	}
	char *oldbuf = buf;
	while (ch > ' ')
	{
		*buf++ = ch;
		ch = getcx();
	}
	*buf = '\0';
	return (int)(buf-oldbuf);
}


int main()
{
	return 0;
}
