
// begin: BIGNUM

#ifndef PB
#  define PB push_back
#endif

#ifndef I
#  define I int
#  define LI long long
#endif 

#ifndef FRN
#  define FRN(ii, ll, uu) for(I ii = (ll); ii < uu; ++ii)
#  define FOR(ii, nn) FRN(ii, 0, nn)
#endif

#include<stdio.h>
#include<vector>
using std::vector;

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
	return *this;
    }

    bn& mul(const bn& x) 
    {
        bn result(0);
	bn pattern(*this);
	for (int i=0; i < x.limbs.size(); ++i) {
            bn row(pattern);
	    row.mul(x.limbs[i]);
	    result += row;
	    pattern.mul(BNM);
	}
	limbs.swap(result.limbs);
	return *this;
    }
    
    bn& add(long long x) {
        *this += bn(x);
	return *this;
    }

    bn& pow(int k)
    {
	bn result(1), multiplier(*this);
	while(k) {
		if (k & 1) result.mul(multiplier);
		multiplier.mul(multiplier);
		k >>= 1;
	}
	limbs.swap(result.limbs);
	return *this;
    }
    
    const bn& operator+=(const bn &x) {
        LI carry = 0;
	vector<LI> result;
	int i = 0;
	while (i < limbs.size() || i < x.limbs.size() || carry)
	{
		if ( i < limbs.size() )
			carry += limbs[i];
		if ( i < x.limbs.size() )
			carry += x.limbs[i];
		result.PB(carry % BNM);
		carry /= BNM;
		++i;
	}
	limbs.swap(result);
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
    
    bn& out(const char *after = 0) {
        I n = limbs.size();
        printf("%lld", limbs[n-1]);
        FOR(i, n-1) {
            printf("%04lld", limbs[n-2-i]);
        }
	if ( after )
		printf("%s", after);
	return *this;
    }
};

// end: BIGNUM

