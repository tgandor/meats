#include <iostream>
#include <boost/system/error_code.hpp>

int main() {
	boost::system::error_code ec;
	if ( ec != boost::system::errc::success )
		std::cout << "Error default." << std::endl;
	else
		std::cout << "Success default." << std::endl;
	return 0;
}

