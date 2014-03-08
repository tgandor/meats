#include <iostream>

using namespace std;

template <class T, bool b>
void info()
{
	cout << "The value is: " << b << endl;
}

int main()
{
	const int x = 3;
	info<int, x < 4>();
	return 0;
}
