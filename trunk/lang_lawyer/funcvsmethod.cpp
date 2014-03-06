#include <iostream>

using namespace std;

int Test( void )
{
    return -1;
}

struct A
{
    int Test( void ) const
    {
        return 100;
    }
};

struct B : public A
{
    void Foo( void )
    {
        cout << Test() << endl;
    }
};

int main( void )
{
    B b;
    b.Foo();
    return 0;
}
