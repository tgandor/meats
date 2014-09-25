#include <iostream>
#include <string>
#include <boost/regex.hpp>

using namespace std;

int main()
{
	string search, replace, topic;
	cout << "Enter search: ";
	getline(cin, search);
	cout << "Enter replace: ";
	getline(cin, replace);
	cout << "Enter topic: ";
	getline(cin, topic);
	cout << "Substituted: " << boost::regex_replace(topic, boost::regex(search), replace) << endl;
	return 0;
}
