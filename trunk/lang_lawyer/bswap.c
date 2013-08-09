#include <stdio.h>
/*
gcc: -mpopcnt
*/

int main()
{
    int x;
    scanf("%d", &x);
    printf("%d\n", __builtin_bswap32(x));
    printf("%u\n", __builtin_popcount(x));
    return 0;
}
