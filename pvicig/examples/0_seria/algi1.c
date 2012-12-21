#include <stdio.h>
#include <math.h>

double  A,r1,r2,B;

int main(int argc, char **argv)
{
    r2 = (3.-sqrt(5))/2.;
    r1 = (3.+sqrt(5))/2.;
    A = (3.+sqrt(5.))/(2.*sqrt(5.));
    B = 1. - A;
    for (int i=0; i<20000; i++) 
    {    
      printf("%d: %fe\n", i, B + A);
      B *= r2;
      A *= r1;
    }
    return 0;
}
