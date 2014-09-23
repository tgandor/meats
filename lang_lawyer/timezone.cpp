#include <time.h>
#include <stdio.h>

int main(void)
{
    tzset();
    printf("%ld, %d\n", timezone, daylight);
    puts(tzname[0]);
    puts(tzname[1]);
    return 0;
}

