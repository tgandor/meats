#include  <iostream>

using namespace std;

int main()
{
    constexpr bool x = 257;
    int y = x + 3;
    cout << x << endl;
    cout << int(x) << endl;
    cout << y << endl;
    return 0;
}
