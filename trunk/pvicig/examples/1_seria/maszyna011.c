#include <stdio.h>
#include <string.h>

char no[256];

int main()
{
	int n,i;
	int addr,j,len;
	scanf("%d", &n);
	for(i=0; i<n; i++)
	{
		scanf(" %s", no);
		for(addr=0,j=strlen(no)-1; j>=0; j--)
			addr = (addr*2 + (no[j]=='1')) % 3;
		printf("%c\n", "011"[addr]);
	}
	return 0;
}

