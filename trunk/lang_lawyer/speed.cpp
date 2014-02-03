#include <stdio.h>
#include <time.h>
#include <string.h>

#define BUFSIZE 4096

int stats[256];
unsigned char buf[BUFSIZE];

int textual = 1;
#define TEXTONLY(f) if (textual) TIMEIT(f); else printf("%-15s not timed: binary file\n", #f)

char **argv; // why not ;)

void timeit(void (*fcn)(), const char *name)
{
    clock_t t = clock();
    fcn();
    t = clock() - t;
    long long total = 0;
    for (int i=0; i < 256; ++i) total += stats[i];
    float sec = ((float)t)/CLOCKS_PER_SEC;
    float mbps = (float)total / sec / 1024 / 1024;
    printf ("%-15s took me: %.4f seconds (%7.3f MB/s),\n", name, sec, mbps);
    printf("    first few stats: %d %d %d\n", *stats, stats[1], stats[2]);
    if (stats[0]) textual = 0;
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

void getc_unlocked_test()
{
    FILE *input = fopen(argv[1], "rb");
    int c;
    while ((c=getc_unlocked(input)) != EOF)
        ++stats[c];
    fclose(input);
}

#ifdef unix
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
#endif

void fgets_strlen()
{
    FILE *input = fopen(argv[1], "rb");
    size_t s;
    while (fgets((char*)buf, BUFSIZE, input))
    {
        s = strlen((char*)buf);
        do ++stats[buf[--s]]; while(s);
    }
    fclose(input);
}

void fgets_test()
{
    FILE *input = fopen(argv[1], "rb");
    size_t s;
    while (fgets((char*)buf, BUFSIZE, input))
    {
        unsigned char *p = buf;
        do ++stats[*p]; while(*++p);
    }
    fclose(input);
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
    TIMEIT(getc_unlocked_test);
#ifdef unix
    TIMEIT(read_test);
#endif
    TEXTONLY(fgets_strlen);
    TEXTONLY(fgets_test);
    return 0;
}

