#include <stdio.h>
#include <stdlib.h>

int main()
{
    srand(time(0));
    unsigned first = rand();
    printf("%d - first\n", first);
    printf("%d - next\n", rand());
    puts("Reseeding with first");
    srand(first);
    printf("%d - next\n", rand());
    return 0;
}
