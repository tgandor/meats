#include <iostream>
#include "boost/program_options.hpp"

// compile with -lboost_program_options

namespace po = boost::program_options;

int main()
{
	po::variables_map vm;
	po::options_description desc;
	desc.add_options()
		("help", "Print help messages")
		("add", po::value<int>()->default_value(10), ("additional options"));

	try
	{
		po::store(po::parse_config_file<char>("boostopts.conf", desc), vm);
	}
	catch (const std::exception&)
	{
		int argc = 1;
		const char *argv[2] = {"dummy", 0};
		po::store(po::parse_command_line(argc, argv, desc), vm);
	}

	if ( vm.count("help")  )
	{
		std::cout << desc << std::endl;
		return 0;
	}
	else
	{
		std::cout << "Help option not specified..." << std::endl;
	}

	std::cout << "In the end 'add' is: " << vm["add"].as<int>() << std::endl;
	return 0;
}
