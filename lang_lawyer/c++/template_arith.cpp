#include <iostream>

using namespace std;

template <int N, int K>
struct Power;

template <int N>
struct Power<N, 0>
{
    enum { value = 1 };
};

template <int N, int K>
struct Power
{
    enum { value = Power<N, K-1>::value * N };
};

int main()
{
    cout << Power<3, 3>::value << endl;
    return 0;
}

