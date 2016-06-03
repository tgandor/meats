#include <vector>
#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

int main(int argc, char **argv)
{
    vector<string> args(argv, argv+argc);
    if (find(args.begin(), args.end(), "--help") != args.end())
    {
        cout << args[0] << " - print number of arguments, then arguments on separate lines." << endl;
        cout << "Usage: " << args[0] << " [args...]" << endl;
        return 0;
    }

    cout << args.size() << endl;

    // compile with -std=c++0x
    for (const string &arg : args)
    {
        cout << arg << endl;
    }
    return 0;
}
