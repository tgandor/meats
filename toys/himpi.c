#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include "mpi.h"

int main (int argc, char * argv[])
{
  int size;
  int rank;
  char myhostname[256];

  MPI_Init (&argc, &argv);
  MPI_Comm_rank (MPI_COMM_WORLD, &rank);
  MPI_Comm_size (MPI_COMM_WORLD, &size);

  gethostname(myhostname, sizeof(myhostname));
  printf ("(Rank:%d) PID:%ld hostname:%s\n",
          rank, (long int) getpid(), myhostname);
  MPI_Barrier(MPI_COMM_WORLD);
  if ( rank == 0 )
    printf("Total processes: %d\n", size);
  
  MPI_Finalize ();
  return 0;
}
