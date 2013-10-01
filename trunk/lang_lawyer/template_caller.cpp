#include <stdio.h>
#include <iostream>

using namespace std;

// -std=c++0x/c++11, maybe

void be_called()
{
	puts("OK, I was called");
}

void be_called_args(const char *str)
{
	printf("I was called with arg: %s\n", str);
}

void be_called_with_nontrivial(string s) // by value
{
	cout << "Nontrivial with argument: " << s << endl;
}

template <typename F>
inline void caller(F f)
{
	f();
}

#ifdef __GXX_EXPERIMENTAL_CXX0X__
template <typename F, typename... Args>
inline void caller(F f, Args... args)
{
	f(args...);
}
#endif

int main()
{
	caller(be_called);
#ifdef __GXX_EXPERIMENTAL_CXX0X__
	caller(be_called_args, "C++0x is more complex");
	caller(be_called_with_nontrivial, "will you let non-POD through?");
#endif
	return 0;
}
