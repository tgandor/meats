#include <stdio.h>
#include <dlfcn.h>

int main(int argc, char **argv)
{
	if (argc < 2)
	{
		printf("Usage: %s <dynamic_library.so> [symbol_to_find]\n", argv[0]);
		return 1;
	}
	void *hLib = dlopen(argv[1], RTLD_NOW);
	if (!hLib)
	{
		puts(dlerror());
		return 1;
	}
	printf("Library loaded, at address: %p\n", hLib);
	int status = 0;
	if (argc > 2)
	{
		(void)dlerror();
		void *symbol = dlsym(hLib, argv[2]);
		if (!symbol)
		{
			char *error = dlerror();
			if (dlerror)
			{
				printf("Error retrieving symbol %s: %s\n", argv[2], error);
				status = 1;
			}
			else
			{
				puts("Symbol found, but NULL address returned.");
			}
		}
		else
		{
			printf("Symbol is found, under address: %p\n", symbol);
		}
	}
	int res = dlclose(hLib);
	if (res)
	{
		printf("Error closing: %s\n", dlerror());
		return 1;
	}
	return status;
}
