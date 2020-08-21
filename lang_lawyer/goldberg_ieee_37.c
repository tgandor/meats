#include <stdio.h>

/* On x86_64 this always works (I guess: because of no x87) */
/* check disasm for constant folding? */

int main()
{
    double q;
    q = 3.0 / 7.0;

    if (q == 3.0 / 7.0)
        puts("Equal");
    else
        puts("Unequal");

    return 0;
}

