#include <iostream>

using namespace std;

class ThreadPrivate_OrNot
{
public:
    ThreadPrivate_OrNot() { cout << "Constructed normally at " << this << endl; }
    ThreadPrivate_OrNot(const ThreadPrivate_OrNot& rhs) {
        #pragma omp critical
        cout << "Copy-constructed from " << (void*)&rhs << " to " << this << endl;
    }
    void use(int n) { 
        #pragma omp critical
        cout << "Used at " << this << " in iteration " << n << endl; 
    }
};

int main()
{
    ThreadPrivate_OrNot tpon;
    #pragma omp parallel for firstprivate(tpon)
    for (int i=0; i < 8; ++i)
    {
        tpon.use(i);
    }
    return 0;
}
