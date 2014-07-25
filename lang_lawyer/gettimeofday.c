#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <errno.h>

int main()
{
	struct timeval tv;
	struct timezone tz;
	if (!gettimeofday(&tv, &tz))
	{
		puts("Success:");
		printf("tv_sec: %d\n", (int)tv.tv_sec);
		printf("tv_usec: %ld\n", tv.tv_usec);
		puts("Timezone info:");
		printf("tz_minuteswest: %d\n", tz.tz_minuteswest);
		printf("tz_dsttime: %d\n", tz.tz_dsttime);
	}
	else
	{
		printf("Error: errno %d\n", errno);
	}
	return 0;
}
