#include <cstdio>

#define STRINGIFY(x) #x
#define STRINGIFY_VALUE(x) STRINGIFY(x)
#define STRINGIFY_VALUE2(x) STRINGIFY(#x)

#ifndef SYMBOL
#  define SYMBOL test
#endif

int main()
{
	puts(STRINGIFY(SYMBOL)); // SYMBOL
	puts(STRINGIFY(STRINGIFY(SYMBOL))); // STRINGIFY(SYMBOL)
	puts(STRINGIFY_VALUE2(SYMBOL)); // "SYMBOL"
	puts(STRINGIFY_VALUE(SYMBOL)); // test
	return 0;
}
