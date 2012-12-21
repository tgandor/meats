#include <math.h>
#include <stdio.h>

int main()
{
	double sumlog=0;
	int C,N,i,j,ai, err=0;
	scanf("%d", &C);
	for(i=0;i<C;i++)
	{
		scanf("%d", &N);
		sumlog = 0;
		for(j=0;j<N;j++)
		{
			scanf("%d", &ai);
			if (!ai)
			{
			  printf("0\n");
			  err=1;
			  break;
			}
			sumlog += log10(fabs(ai));
		}
		if(!err)
		  printf("%d\n", (int)floor(sumlog)+1 );
		else
		  err=0;
	}
	return 0;
}
