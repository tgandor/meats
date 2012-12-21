#include <stdio.h>
#include <limits.h>

int FIB[47];
int MOD = INT_MAX;

int fib(int x)
{
	int n,k,fn1,fn;
	long long ret;
	switch ( x<6 )
	{
		case 1:
		  return FIB[x] % MOD;
	}
	switch ( x%2 )
	{
	case 1:
		n = (x-3)/2;
		k = 3;
		break;
	case 0:
		n = (x-2)/2;
		k = 2;
	}
	fn1 = fib(n+1);
	fn = fib(n);
	
	ret = (long long) FIB[k] * fn1 % MOD;
	ret = ret * fn1 % MOD;
	ret = (ret + (long long)fn1*fn*FIB[k-1]) % MOD;
	ret = (ret + (long long)fn*fn*FIB[k-2]) % MOD;
	return (int)ret;
}

int main()
{
	int i,C,a,b,n;
	long long ans;
	FIB[1]=1; for(i=2; i<47; i++) FIB[i] = FIB[i-1] + FIB[i-2];
	i=6; 
	while(i<47)
	{
		if (fib(i) != FIB[i])
			printf("%d! jest: %d, powinno: %d\n", i, fib(i), FIB[i]);
	    i++;
	}
	scanf("%d", &C);
	i=0;
	while(i<C) { 
		scanf("%d%d%d%d", &a, &b, &n, &MOD);
		ans = (long long) a * fib(n+1) % MOD + b * fib(n+2) % MOD;
		ans %= MOD;
		printf("%lld\n", ans);
		i++;
	}
	return 0;
}
