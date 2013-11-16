#include <stdio.h>

// for feeding to compilers, and seeing what happens.
// the standard says about undefined behavior

#ifndef NOEXPL
void explicit_()
{
	int x = 5;
	x /= 0; // warning or error? or runtime error?
}
#endif

int main()
{
	int a = 1, b = 0;
#ifndef NOEXPL
	explicit_();
#endif
	printf("Enter 0: ");
	scanf("%d", &b);
	int c = a / b; // runtime error? SIGFPE?
	printf("1 divided by %d = %d", b, c);
	return 0;
}
