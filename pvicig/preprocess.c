#include "preprocess.h"

/**
 * Tries to preprocess given string with the C preprocessor.
 * If the preprocessor is not in the path, returns the
 * unchanged string.
 * --------------
 * Próbuje poddaæ podany napis (kod ¼ród³owy) przetwarzaniu
 * preprocesorem CPP. Je¿eli nie uda siê to (nie mo¿na
 * znale¼æ programu cpp), zwracany jest napis oryginalny.
 */

#define RD 0
#define WR 1

#include <signal.h>


char *preprocess(char *source)
{
  int send[2], recv[2];
  int filter_status;
  pid_t pid;

  // printf("Zaraz beda pipy\n");
  if (pipe(send)  || pipe(recv))
	  return source;

  // printf("Proces glowny - zaczynam forkowac\n");
  pid = fork();
  if (pid < 0)
	  return source;

  // child process, filter -- proces potomny, filtr
  if (!pid)
  {
	  int c, exec_error;
	  /*
	  signal(SIGSEGV, sigFilter);
	  fprintf(stderr, "Filtr: Tu proces filtr, zaraz sie zastapie\n");
	  */
	  close(send[WR]);
	  close(recv[RD]);

	  close(0); // close standard input -- podmiana standardowego wej¶cia
	  dup(send[RD]);
	  close(send[RD]);

	  close(1);
	  dup(recv[WR]);
	  close(recv[WR]);

	  exec_error = execlp("cpp", "cpp", (char*)0);

	  fprintf(stderr, "Error (%d): could not execute cpp\n", exec_error);
	  while ((c = getchar()) != EOF)
		  putchar(c);

	  exit(1); // return non-zero status -- zwracamy nie 0
  }
  else // parent process or sender -- proces rodzic lub nadawca
  {
	  FILE *out, *in;
	  char *ret=0;
	  pid_t pid2;

	  close(send[RD]);
	  close(recv[WR]);

	  pid2 = fork();
	  if (pid2 < 0)
		  return source;
	  if (!pid2) {  // the sender -- nadawca
		  /*
		  signal(SIGSEGV, sigSender);
		  printf("Nadawca: Pozdrowienia od nadawcy\n");
		  */
		  out = fdopen(send[WR], "w");
		  // printf("Nadawca: Plik otwarty\n");
		  fputs(source, out);
		  // printf("Nadawca: Wys³ane\n");
		  fclose(out);
		  // printf("Nadawca: Plik zamkniêty\n");
		  close(send[WR]);
		  exit(0);
	  }
	  // the main process, parent -- rodzic, proces g³ówny
	  /*
	  signal(SIGSEGV, sigMain);
	  */
	  close(send[WR]);
	  // printf("Main: Pozdrawia proces glowny po uruchomieniu\n");
	  waitpid(pid2, NULL, 0);
	  waitpid(pid, &filter_status, 0);

	  // printf("Main: Pozdrawia proces glowny po odczekaniu\n");

	  in = fdopen(recv[RD], "r");
	  // printf("Main: otwarlem sobie plik\n");
	  afgettoch(&ret, in, '\0');
	  // printf("Main: wciagnalem plik\n");
	  fclose(in);
	  // printf("Main: zamknalem plik\n");
	  close(recv[RD]);

	  if (filter_status != 0) {
		  astrfree(&ret);
	  }

	  return ret;
  }

  return source;
}

void preprocess_from(char **source)
{
	char *temp;
	temp = *source;
	*source = preprocess(*source);
	free(temp);
}

/*
void sigMain(int dummy) {
	fprintf(stderr, "To ja, glowny dostalem\n");
	fflush(stderr);
	exit(0);
}

void sigSender(int dummy) {
	fprintf(stderr, "To ja, nadawca dostalem\n");
	fflush(stderr);
}

void sigFilter(int dummy) {
	fprintf(stderr, "To ja, filtr dostalem\n");
	fflush(stderr);
}
*/
