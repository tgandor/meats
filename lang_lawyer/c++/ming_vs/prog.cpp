#include <iostream>
#include "lib.h"

using namespace std;

int main()
{
    int n;
    cout << "Enter integer: ";
    cin >> n;
    int divisor = max_div(n);
    if (!divisor)
    {
        cout << "Error" << endl;
    }
    else if (divisor == n)
    {
        cout << "Prime number" << endl;
    }
    else
    {
        cout << "Greatest divisor: " << divisor << endl;
    }
    return 0;
}
