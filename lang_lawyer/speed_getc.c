#include <stdio.h>
#include <time.h>


int stats[256];

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Usage: time %s <big_file>\n", *argv);
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    int c;
    clock_t t = clock();
    while ((c=getc(input)) != EOF)
        ++stats[c];
    t = clock() - t;
    printf ("It took me %lld clicks (%f seconds).\n",
            (long long)t,
            ((float)t)/CLOCKS_PER_SEC);
    printf("First few stats: %d %d %d\n", *stats, stats[1], stats[2]);
    fclose(input);
    return 0;
}

