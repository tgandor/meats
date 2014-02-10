
namespace redundant
{
	typedef int type;
	redundant::type f(redundant::type x)
	{
		return x;
	}

	redundant::type g(redundant::type x);
}

redundant::type redundant::g(redundant::type x)
{
	return x;
}

int main ()
{
	redundant::f(41);
	redundant::g(42);
	return 0;
}
