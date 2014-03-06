#include <iostream>

using namespace std;


int Test( void )
{
    return -1;
}

template<typename T>
struct A
{
    int Test( void ) const
    {
        return 100;
    }
};

template<typename T>
struct B : public A<T>
{
    void Foo( void )
    {
        cout << Test() << endl;
    }
    void Goo( void )
    {
        cout << this->Test() << endl;
    }
};

int main( void )
{
    B<int> b;
    b.Foo();
    b.Goo();
    return 0;
}
