#include <stdio.h>
#include <time.h>

#define BUFSIZE 1024

int stats[256];
unsigned char buf[BUFSIZE];

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Usage: [time] %s <big_file>\n", *argv);
        return 1;
    }
    FILE *input = fopen(argv[1], "rb");
    size_t s;
    clock_t t = clock();
    while (s = fread(buf, 1, BUFSIZE, input))
        do ++stats[buf[--s]]; while(s);
    t = clock() - t;
    printf ("It took me %lld clicks (%f seconds).\n",
            (long long)t,
            ((float)t)/CLOCKS_PER_SEC);
    printf("First few stats: %d %d %d\n", *stats, stats[1], stats[2]);
    fclose(input);
    return 0;
}

