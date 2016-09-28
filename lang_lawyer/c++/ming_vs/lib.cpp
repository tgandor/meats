#include "lib.h"

extern "C"
{
    int DLLFUNC max_div(int n)
    {
        if (n <= 1)
            return 0;
        for (int i=2; i <= n/2; ++i)
        {
            if (n % i == 0)
            {
                return n / i;
            }
        }
        return n;
    }
}
