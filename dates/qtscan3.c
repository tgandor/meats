#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
 

unsigned int swapBytes(unsigned int x) {
  unsigned int ret=0;
  unsigned int i;
  for(i=0; i<sizeof(unsigned int); i++) {
    ret <<= 8;
    ret += (x & 255);
    x >>= 8;
  }
  return ret;
}

int main(int argc, char **argv) {
  int i, size, fsize, crtime;
  char sig[5] = "    ";
  FILE *fp;
  char buf[100], bufn[100], *ext;
  char *dateFormat = "%Y-%m-%d_%H-%M-%S";
  int first = 0;
  int help = 0;
  int verbose = 1;
  int quiet = 0;
  int opt;

  time_t qtera, fdate;
  struct tm* qtera_tm = (struct tm*) calloc (1, sizeof(struct tm));
  qtera_tm->tm_year = 4;
  qtera_tm->tm_mday = 1;
  qtera = mktime(qtera_tm);
  free(qtera_tm);
  printf("%d\n", (int)qtera);

  do {
    switch(opt = getopt(argc, argv, "fs:hqv")) {
        case 'f':
            first = 1;
            break;
        case 's':
            dateFormat = optarg;
            break;
        case 'h':
        case '?':
            help = 1;
            break;
        case 'v':
            verbose = 1;
            break;
        case 'q':
            verbose = 0;
            quiet = 1;
            break;
    }
  } while (opt != -1);

  if ( argc == optind || help ) {
    printf(
           "Usage: %s [-f] file.mov [file1.mov ...]\n-f\tdo actual rename\n"
            "-s'format'\tformat to pass to strftime\n-v\tbe more verbose (show pattern)\n",
           argv[0]);
    return 0;
  }

  if ( verbose ) {
      printf("Current format: '%s', verbose: %d, first: %d\n", dateFormat, verbose, first);
  }

  while (--argc >= optind) {
    ext = strrchr(argv[argc], '.');
    if ( strlen(argv[argc]) != strcspn(argv[argc], "/ ") ) {
      printf("Plik: %s nie jest w tym katalogu, niestety...\n", argv[argc]);
      continue;
    }
    if ( strcmp(ext, ".mov") ) {
      printf("Plik: %s nie jest .mov, nawet nie ryzykuje...\n", argv[argc]);
      continue;
    }
    fp = fopen(argv[argc], "r");
    if ( !fp ) {
      printf("Skopany plik: %s\n", argv[argc]);
      continue;
    }

    fseek(fp, 0, SEEK_END);
    fsize = ftell(fp);
    printf("The file %s is %10d bytes big.\n", argv[argc], fsize);

    fseek(fp, 0, SEEK_SET);
    while(ftell(fp) < fsize) {
      fread(&size, 1, sizeof(int), fp);
      size = swapBytes(size);
      fread(sig, 1, 4, fp);
      if ( *(int*)sig == 'voom' ) {
        fseek(fp, 12, SEEK_CUR);
        fread(&crtime, 1, sizeof(int), fp);
        fdate = swapBytes(crtime)+qtera;
        strftime(buf, 100, dateFormat, localtime(&fdate));
        sprintf(bufn, "%s%s", buf, ext);
        // puts(ctime(&fdate));
        // puts(bufn);
        fclose(fp);
        fp = 0;
        if ( strcmp(bufn, argv[argc]) ) {
          printf("mv %s %s\n", argv[argc], bufn);
          if ( first )
            rename(argv[argc], bufn);
        } else {
          printf("File %s is already ok\n", bufn);
          break;
        }
        break;
        // fseek(fp, size-20, SEEK_CUR);
      }
      else
        fseek(fp, size-8, SEEK_CUR);
    }
    if ( fp )
      fclose(fp);
  }

  return 0;
}
