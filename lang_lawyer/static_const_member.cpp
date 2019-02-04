#include <vector>

#ifdef _MSC_VER

class Foo
{
public:
	static const int MEMBER = 1;
};

#else

// e.g. GCC

class Foo
{
public:
	static const int MEMBER;
};

const int Foo::MEMBER = 1;

#endif

int main()
{
	std::vector<int> v;
	v.push_back( Foo::MEMBER );       // by reference
	v.push_back( (int) Foo::MEMBER ); // by value
	return 0;
}
