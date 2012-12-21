#include <stdio.h>
#include <string.h>

/* tu pozawia siê komentarz */

char no[256];

/* autorem zest kto inny ? */
int main()
{
	int n,i;
	int addr,z,len;
	scanf("%d", &n);
	for(i=0; i<n; i++)
	{
		scanf(" %s", no);
		for(addr=0,z=strlen(no)-1; z>=0; z--)
			addr = (addr*2 + (no[z]=='1')) % 3;
		printf("%c\n", "011"[addr]);
	}
	return 0;
}

