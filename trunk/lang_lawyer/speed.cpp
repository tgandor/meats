#include <stdio.h>
#include <time.h>
#include <string.h>

#define BUFSIZE 4096

int stats[256];
unsigned char buf[BUFSIZE];

char **argv; // why not ;)

void timeit(void (*fcn)(), const char *name)
{
    clock_t t = clock();
    fcn();
    t = clock() - t;
    printf ("%-12s took me: %10lld clicks (%f seconds).\n", 
		    name, (long long)t, ((float)t)/CLOCKS_PER_SEC);
    printf("    First few stats: %d %d %d\n", *stats, stats[1], stats[2]);
    memset(stats, 0, 256*sizeof(int));
}
#define TIMEIT(f) timeit(f, #f)

void fread_test()
{
    FILE *input = fopen(argv[1], "rb");
    size_t s;
    while (s = fread(buf, 1, BUFSIZE, input))
        do ++stats[buf[--s]]; while(s);
    fclose(input);
}

void getc_test()
{
    FILE *input = fopen(argv[1], "rb");
    int c;
    while ((c=getc(input)) != EOF)
        ++stats[c];
    fclose(input);
}

#include <unistd.h>
#include <fcntl.h>
void read_test()
{
    int input = open(argv[1], O_RDONLY);
    size_t s;
    while (s = read(input, buf, BUFSIZE))
        do ++stats[buf[--s]]; while(s);
    close(input);
}

int main(int argc, char **_argv)
{
    argv = _argv;
    if (argc < 2)
    {
        printf("Usage: [time] %s <big_file>\n", *argv);
        return 1;
    }
    TIMEIT(fread_test);
    TIMEIT(getc_test);
    TIMEIT(read_test);
    return 0;
}

