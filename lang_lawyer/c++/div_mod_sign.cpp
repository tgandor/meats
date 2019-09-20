#include <iostream>

using namespace std;

int main()
{
    cout << "(n, (n // 3, n % 3), (n // -3, n % -3))" << endl;
    for (int i=-6; i < 7; ++i)
    {
        cout << '(' << i << ", (" << i / 3 << ", " << i % 3 << "), "
             << '(' << i / -3 << ", " << i % -3 << "))" << endl;
    }

    return 0;
}

/* Results:
(trunc division - towards 0, modulus == dividend - divisor * result, e.g.:
2 % (-3) == 2 - (-3) * 0 == 2)

This means that the  modulus has the sign of the DIVIDEND

and:

modulus == sign(dividend) * (abs(dividend) % abs(divisor))

(-6, (-2, 0), (2, 0))
(-5, (-1, -2), (1, -2))
(-4, (-1, -1), (1, -1))
(-3, (-1, 0), (1, 0))
(-2, (0, -2), (0, -2))
(-1, (0, -1), (0, -1))
(0, (0, 0), (0, 0))
(1, (0, 1), (0, 1))
(2, (0, 2), (0, 2))
(3, (1, 0), (-1, 0))
(4, (1, 1), (-1, 1))
(5, (1, 2), (-1, 2))
(6, (2, 0), (-2, 0))

*/

