#include <iostream>
#include <iterator>
#include <sstream>
#include <algorithm>
#include <vector>

using namespace std;

int left(const vector<int>& v)
{
	int cnt = 1;
	int maxi = v[0];
	for (int i = 1; i<v.size(); ++i)
	{
		if (v[i] > maxi)
		{
			++cnt;
			maxi = v[i];
		}
	}
	return cnt;
}

int right(const vector<int>& v)
{
	int cnt = 1;
	int maxi = v[v.size()-1];
	for (int i = v.size()-2; i>=0; --i)
	{
		if (v[i] > maxi)
		{
			++cnt;
			maxi = v[i];
		}
	}
	return cnt;
}

int main(int argc, char **argv)
{
	int n;
	if (argc > 1)
	{
		istringstream nstr(argv[1]);
		nstr >> n;
	}
	else
	{
		cout << "How many pyramids: ";
		cin >> n;
	}
	if (n < 2 || n > 8)
	{
		cerr << argv[0] << ": Bad value for n: " << n << endl;
		return 1;
	}
	vector<int> pyramids(n);
	for (int i=1; i <= n; ++i)
		pyramids[i-1] = i;
	do
	{
		cout << left(pyramids) << " --- ";
		copy(pyramids.begin(), pyramids.end(), ostream_iterator<int>(cout, " "));
		cout << "--- " << right(pyramids) << endl;
	} while (next_permutation(pyramids.begin(), pyramids.end()));
	return 0;
}


