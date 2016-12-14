
#if __cplusplus < 201103L
#define override
#warning This sould be compiled with C++11 or better
#endif

class Base
{
public:
	virtual void method();
	virtual ~Base();
};

void Base::method() {}
Base::~Base() {}

class DerivedAbstract : public Base
{
public:
	virtual void method() override = 0;
};

class DerivedConcrete : public DerivedAbstract
{
public:
	virtual void method() override;
};

void DerivedConcrete::method() {}

int main()
{
	Base b;
	DerivedConcrete dc;
	b.method();
	dc.method();
	// DerivedAbstract da; - error
	return 0;
}

