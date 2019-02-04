#include <stdio.h>
#include <math.h>

long double r1, r2, A, B;

int main()
{
    A = (3.+sqrt(5.))/(2.*sqrt(5.));
    B = 1. - A;
    r1 = (3.+sqrt(5))/2.;
    r2 = (3.-sqrt(5))/2.;

    for (int i=0; i<20000; i++) {
      printf("%d: %Le\n", i, A + B);
      A *= r1;
      B *= r2;
    }
    // scanf("%lf", &A);
    return 0;
}
