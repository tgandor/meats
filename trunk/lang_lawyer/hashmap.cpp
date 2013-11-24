#include <iostream>
#include <tr1/unordered_map>

using namespace std;

int main()
{
	string w;
	tr1::unordered_map<string, int> stats;
	while (cin >> w)
	{
		cout << w << ": " << ++stats[w] << endl;
	}
	return 0;
}
