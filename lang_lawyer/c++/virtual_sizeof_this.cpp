#include <iostream>

using namespace std;

struct TellsSize
{
    size_t get_my_size()
    {
        return sizeof(*this);
    }
};

struct TellsSizeVirt
{
    virtual size_t get_my_size()
    {
        return sizeof(*this);
    }
};

class A : public TellsSize
{
    int x;
};

class B : public TellsSizeVirt
{
    long long x;
};

class C : public TellsSizeVirt
{
    int x;
};

int main(int argc, char const *argv[])
{
// nothing helps, the size is always 1 for non-virt and 8 for virt
// regardless of actual type?
#define CHECK(type) cout << #type ": " << type().get_my_size() << "; sizeof " << sizeof(type) << endl
    CHECK(TellsSize);
    CHECK(TellsSizeVirt);
    CHECK(A);
    CHECK(B);
    CHECK(C);
#undef CHECK
    cout << "---" << endl;
#define CHECK(type) type v##type; cout << #type " variable: " << v##type.get_my_size() << endl
    CHECK(TellsSize);
    CHECK(TellsSizeVirt);
    CHECK(A);
    CHECK(B);
    CHECK(C);
#undef CHECK
    cout << "---" << endl;
#define CHECK(type) cout << #type " pointer: " << (&v##type)->get_my_size() << endl
    CHECK(TellsSize);
    CHECK(TellsSizeVirt);
    CHECK(A);
    CHECK(B);
    CHECK(C);
#undef CHECK
    return 0;
}
