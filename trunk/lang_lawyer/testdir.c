#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

int main( int argc, char *argv[] )
{

   if(chdir( argv[1] ) )
   {
      switch (errno)
      {
      case ENOENT:
         printf( "Unable to locate the directory: %s\n", argv[1] );
         break;
      case EINVAL:
         printf( "Invalid buffer.\n");
         break;
      default:
         printf( "Unknown error.\n");
      }
   }
   else
      system( "dir *.exe");
}
