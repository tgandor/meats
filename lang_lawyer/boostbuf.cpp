#include <iostream>
#include <boost/asio.hpp>

int main() 
{
	boost::asio::streambuf strb;
	std::cout << strb.max_size() << std::endl;
	return 0;
}

