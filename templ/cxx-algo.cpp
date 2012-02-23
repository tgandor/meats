#include <stdio.h>
#include <math.h>
#include <string.h>
#include <algorithm>
#include <numeric>
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
#define LI long long
#define LIN(x) LI x; scanf("%lld", &x)
#define LOUT(x) printf("%lld\n", x)
#define GETS(s) scanf(" %s", s)
// 2**62-1, won't overflow if doubled
#define LINF 4611686018427387903LL
#define BYTE unsigned char

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
ostream_iterator<int> ioutln(cout, "\n");

#define BNM 10000
class bn {
    vector<long long> limbs;
public:
    bn(long long x = 0LL) {
        load(x);
    }
    
    bn(const bn &tpl) : limbs(tpl.limbs) {}
    
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

    void mul(const bn& x) 
    {
        bn result(0);
	bn pattern(*this);
	for (int i=0; i < x.limbs.size(); ++i) {
	    pattern.mul(BNM);
            bn row(pattern);
	    row.mul(x.limbs[i]);
	    result += row;
	}
	limbs.swap(result.limbs);
    }
    
    void add(long long x) {
        *this += bn(x);
    }
    
    const bn& operator+=(const bn &x) {
        LI carry = 0;
        if ( x.limbs.size() > limbs.size() ) 
            limbs.resize(x.limbs.size(), 0LL);
        FOR(i, x.limbs.size()) {
            LI temp = limbs[i]+x.limbs[i]+carry;
            if ( i == limbs.size() ) 
                limbs.PB(temp % BNM);
            else
                limbs[i] = temp % BNM;
            carry = temp / BNM;
        }
        if ( carry ) {
            if ( x.limbs.size() == limbs.size() ) 
                limbs.PB(carry);
            else {
                I i = x.limbs.size();
                while ( carry ) { 
                    LI temp = limbs[i] + carry;
                    if ( i == limbs.size() ) 
                        limbs.PB(temp % BNM);
                    else
                        limbs[i] = temp % BNM;
                    carry = temp / BNM;
                }
            }
        }
        return *this;
    }

    bool operator<(const bn &x) {
        if ( limbs.size() < x.limbs.size() )
            return true;
        if ( limbs.size() > x.limbs.size() )
            return false;
        for(I n = limbs.size()-1; n>=0; --n) 
            if ( limbs[n] != x.limbs[n] )
                return limbs[n] < x.limbs[n];
        return false;
    }
    
    bool operator<(const LI &x) {
        if ( x < BNM )
            return limbs.size()==1 && limbs[0]<x;
        return operator<(bn(x));
    }
    
    void out() {
        I n = limbs.size();
        printf("%lld", limbs[n-1]);
        FOR(i, n-1) {
            printf("%04lld", limbs[n-2-i]);
        }
    }
};

#define PII_ovlap(x, y) ((x).p1 <= (y).p2 && (y).p1 <= (x).p2)
#define PII_ovlap2(pi, a, b) ((pi).p1 <= (b) && (pi).p2 >= (a))

int bitnum[] = {
0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8    
};

template <class T> 
T gcd(T a, T b) {
    T c = a % b;
    while ( c ) { a = b; b = c; c = a % b; }
    return b;
}

/// END OF BOILERPLATE ;)

int main() {
    
    return 0;
}
