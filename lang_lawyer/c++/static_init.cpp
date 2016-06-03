#include <iostream>

using namespace std;

const int SIZE = 100;

int is_prime(int n)
{
	static bool sieve[SIZE];
	struct InitStruct
	{
		InitStruct()
		{
			cout << "Initializing the sieve..." << endl;
			for (int i=2; i*i < SIZE; ++i)
				if (!sieve[i])
				{
					for (int j=i*i; j<SIZE; j += i)
						sieve[j] = true;
				}
		}
	};
	static InitStruct initializer;
	if (n >= 0 && n < SIZE)
		return !sieve[n];
	cout << "Error: outside range." << endl;
	return false;
}

int main()
{
	cout << "Before first call" << endl;
	cout << is_prime(5) << endl;
	cout << is_prime(16) << endl;
	cout << is_prime(101) << endl;
	return 0;
}
