#include <iostream>
#include <string>

int main()
{
	std::wstring wide( L"Wide" );
	std::string str( wide.begin(), wide.end() );
	std::cout << str << std::endl;
	return 0;
}
