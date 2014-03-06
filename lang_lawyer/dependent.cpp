#include <stdio.h>

struct ConcreteBase {
	static const int VAL = 1;
};

template<typename T>
struct TemplateDerived : public ConcreteBase
{
	void f() { printf("Look ma! VAL is %d (not dependent)\n", VAL); }
};

int main()
{
	TemplateDerived<int> td;
	td.f();
	return 0;
}

