#include <iostream>
#include <sstream>
#include <chrono>
#include <thread>
#include <locale>
#include <cmath>

// -std=c++11

#ifdef CNT
int g_calls;
#endif

int fib(int n)
{
#ifdef CNT
	++g_calls;
#endif
	if (n < 2)
	{
		return n;
	}
	return fib(n-1) + fib(n-2);
}

struct Numpunct: public std::numpunct<char>
{
protected:
	virtual char do_thousands_sep() const { return ','; }
	virtual std::string do_grouping() const { return "\003"; }
};

int main(int argc, char **argv)
{
	using namespace std::chrono;
	double percent = 50;
	if (argc > 1)
	{
		std::istringstream(argv[1]) >> percent;
	}

	if (percent < 1)
		percent = 1.0;
	else if (percent > 100)
		percent = 100;

	for (;;)
	{
		high_resolution_clock::time_point start = high_resolution_clock::now();
		int fib_n = fib(10 + rand() % 20);
		high_resolution_clock::time_point end = high_resolution_clock::now();
		duration<double> elapsed = duration_cast<duration<double>>(end - start);
		std::this_thread::sleep_for(elapsed * (100 / percent - 1));
	}

	return 0;
}
