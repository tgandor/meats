#include <iostream>
#include <unistd.h>

int main()
{
	std::cout << sysconf(_SC_CLK_TCK) << std::endl;
	return 0;
}