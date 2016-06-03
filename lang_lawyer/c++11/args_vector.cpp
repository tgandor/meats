#include <vector>
#include <iostream>
#include <string>
#include <algorithm>

// example: g++ -std=c++11 -DOUTPUT=/tmp/args.txt args_vector.cpp
// will save the args when called by something (like other program...)

#ifdef OUTPUT
#  include <fstream>
#  define STRINGIZE(x) #x
#  define STRING(x) STRINGIZE(x)
#endif


int main(int argc, char **argv)
{
#ifdef OUTPUT
    std::ofstream cout(STRING(OUTPUT));
    std::cout << "Redirecting to: " << STRING(OUTPUT) << std::endl;
#else
    using std::cout;
#endif

    using std::endl;

    std::vector<std::string> args(argv, argv+argc);
    if (std::find(args.begin(), args.end(), "--help") != args.end())
    {
        cout << args[0] << " - print number of arguments, then arguments on separate lines." << endl;
        cout << "Usage: " << args[0] << " [args...]" << endl;
        return 0;
    }

    cout << args.size() << endl;

    // compile with -std=c++0x
    for (const std::string &arg : args)
    {
        cout << arg << endl;
    }

    return 0;
}
