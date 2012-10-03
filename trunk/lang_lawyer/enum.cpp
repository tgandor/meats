#include <iostream>

using namespace std;

enum vals { A, B=0xFFFFFFFFFFL, C };
enum vals2 { D, E, F };

int main()
{
	vals x;
	vals2 y;
	cout << sizeof(x) << endl;
	cout << sizeof(y) << endl;
	return 0;
}

