#include <iostream>
#include <string>
#include <functional>

int main()
{
	std::cout << "Input string:" << std::endl;
	std::string to_hash;
	std::cin >> to_hash;
	std::cout << "Hash = " << std::hash<std::string>()(to_hash) << std::endl;
	return 0;
}

