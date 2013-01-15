#include <stdio.h>

main(int argc, char *argv[])
{
	if (argc != 3)
	{
		printf("Usage: %s <file1> <file2>\n", argv[0]);
		return 1;
	}
	FILE *f1 = fopen(argv[1], "rb");
	FILE *f2 = fopen(argv[2], "rb");
	int c1, c2;
	int total = 0;
	for (;;)
	{
		c1 = fgetc(f1);
		c2 = fgetc(f2);
		if (c1 != c2)
		{
			printf("Files differ at byte %d: %d vs %d\n", total, c1, c2);
			break;
		}
		++total;
		if (c1 == EOF)
		{
			puts("Files same.");
			break;
		}
	}
	fclose(f1);
	fclose(f2);
	return 0;
}
