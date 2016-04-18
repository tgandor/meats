#include <iostream>
#include <unistd.h>

// actually this can be done in the shell:
// $ getconf CLK_TCK
// and this just shows the jiffies per second, arbitrarily configured as 100 Hz (10 ms)
// and not related to internal kernel interrupts
int main()
{
	std::cout << sysconf(_SC_CLK_TCK) << std::endl;
	return 0;
}
