#include <stdlib.h>
#include <stdio.h>
float x[4] = { 1, 2, 3, 4 };
float y[4] = { .1, .01, .001, .0001 };
int four = 4;
int one = 1;
extern "C" double sdot_(...);
int main() {
  int i;
  double r = sdot_(&four, x, &one, y, &one);
  printf("%lf\n", r);
  exit((float)r != (float).1234);
}
