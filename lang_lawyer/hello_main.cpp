#include <iostream>
#include <string>

using namespace std;

int main()
{
	string s((const char *)&main);
	cout << s << endl;
	return 0;
}

