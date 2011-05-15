#include <stdio.h>
#include <math.h>
#include <algorithm>
#include <list>
#include <deque>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

#define I int
#define IN(x) I x; scanf("%d", &x)
#define OUT(x) printf("%d\n", x)
#define FRN(ii, ll, uu) for(I ii = (ll); ii < uu; ++ii)
#define FOR(ii, nn) FRN(ii, 0, nn)

#define PB push_back
#define IT iterator
// caution
#define POPB(x) x.back(); x.pop_back()

#define PII pair<I,I>
#define p1 first
#define p2 second
#define UNPACK(a, b, pi) int a = (pi).p1, b = (pi).p2

using namespace std;

// #define DBG(fmt, args...) printf(fmt "\n", args)
#define DBG(fmt, args...)

template<class T1, class T2>
ostream& operator<< (ostream& o, const pair<T1, T2> &p) {
    return o << '(' << p.p1 << ", " << p.p2 << ')';    
}

template<class T>
ostream& operator<< (ostream& o, const list<T> &l) {
    typename list<T>::const_iterator i = l.begin();
    o << '[';
    if ( i != l.end() )
        o << *i++;
    for(; i != l.end(); ++i) 
        o << ", " << *i;
    return o << ']';
}

template<class T>
ostream& operator<< (ostream& o, const deque<T> &l) {
    typename deque<T>::const_iterator i = l.begin();
    o << "deq[";
    if ( i != l.end() )
        o << *i++;
    for(; i != l.end(); ++i) 
        o << ", " << *i;
    return o << ']';
}

template<int N>
ostream& operator<< (ostream& o, const PII (&a)[N]) {
    o << "arr(" << N << ")[" << a[0];
    FRN(i, 1, N) {
        o << ", " << a[i];
    }
    return o << ']';
}

ostream_iterator<int> iout(cout, " ");

#define BNM 10000
class bn {
    vector<long long> limbs;
public:
    bn(long long x = 0LL) {
        load(x);
    }
    
    void load(long long x) {
        limbs.clear();
        do { 
            limbs.PB(x % BNM);
            x /= BNM;
        } while (x);        
    }
    void mul(long long x) {
        long long carry=0, m = x % BNM;
        vector<long long> result;
        FOR(i, limbs.size()) {
            long long temp = limbs[i] * m + carry;
            result.PB(temp % BNM);
            carry = temp / BNM;
        }
        if ( carry )
            result.PB(carry);
        x /= BNM;
        I j = 1;
        while( x ) {
            m = x % BNM;
            carry = 0;
            FOR(i, limbs.size()) {
                long long temp = limbs[i] * m + carry;
                if ( i+j == result.size() )
                    result.PB(temp%BNM);
                else {
                    temp += result[i+j];
                    result[i+j] = temp % BNM;
                }
                carry = temp / BNM;
            }
            if ( carry )
                result.PB(carry);
            x /= BNM;
            ++j;
        }
        limbs.swap(result);
    }
    
    void add(long long x) {
        long long carry = 0;
        I i = 0;
        while ( x ) {
            long long temp = limbs[i] + x % BNM + carry;
            if ( i == limbs.size() ) 
                limbs.PB(temp % BNM);
            else
                limbs[i] = temp % BNM;
            carry = temp / BNM;
            x /= BNM; ++i;
        }
    }
    
    void out() {
        I n = limbs.size();
        printf("%lld", limbs[n-1]);
        FOR(i, n-1) {
            printf("%04lld", limbs[n-2-i]);
        }
    }
};

/// END OF BOILERPLATE ;)

int main() {
    
    return 0;
}
