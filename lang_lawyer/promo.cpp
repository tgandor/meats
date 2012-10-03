#include <iostream>

using namespace std;

template<typename T1, typename T2>
class Promotion;

template<bool C, typename Ta, typename Tb>
class IfThenElse;

template<typename Ta, typename Tb>
class IfThenElse<true, Ta, Tb>
{
  public :
    typedef Ta ResultT;
};

template<typename Ta, typename Tb>
class IfThenElse<false, Ta, Tb>
{
  public :
    typedef Tb ResultT;
};

// #define ORIG

#ifdef ORIG
template<typename T1, typename T2>
class Promotion
{
  public :
    typedef typename IfThenElse< (sizeof(T1) > sizeof(T2)),
                                  T1,
                                  typename IfThenElse<(sizeof(T1) < sizeof(T2)),
                                  T2,
                                  void>::ResultT>::ResultT ResultT;
};
#else
template<typename T1, typename T2>
class Promotion
{
  public :
	    typedef typename IfThenElse< (sizeof(T1) > sizeof(T2)), T1, T2>::ResultT ResultT;
};
#endif

struct Foo {
	Foo() : d(987.65) { }
	double d;
};

struct Bar : public Foo {
	Bar() : c('x') { }
	char c;
};

main()
{
	Promotion< Foo, Bar >::ResultT x;

	cout << sizeof( Foo ) << endl;
	cout << sizeof( Bar ) << endl;
	cout << sizeof( x    ) << endl;
	cout << sizeof( x.c  ) << endl;
	cout << sizeof( x.d  ) << endl;
}
