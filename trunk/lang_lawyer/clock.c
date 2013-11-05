#include<time.h>
#include<stdio.h>
main() { return !printf("%zd\n", sizeof(clock_t)); }

