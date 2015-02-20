#include <stdio.h>
#include <linux/input.h>

int main(int argc, char **argv)
{
	char buf1[KEY_CNT / 8], buf2[KEY_CNT / 8];

	if (argc < 2)
	{
		printf("Usage: %s /dev/input/eventX (keyboard virtual file).\n", argv[0]);
		return 1;
	}

	FILE *kbd = fopen(argv[1], "r");
	if (!kbd)
	{
		printf("%s: error: Could not open keyboard file: %s.\n", argv[0], argv[1]);
		return 1;
	}

	puts("Reading keyboard...");
	fread(buf1, KEY_CNT / 8, 1, kbd);
	puts("Processing result:");

	int i, j;
	for (i=0; i < 8; ++i)
	{
		printf("%2d: ", i*8);
		for (j=0; j<8; ++j)
			putchar ('0' + ((buf1[i] >> j) & 1));
		putchar('\n');
	}
	puts("------------");

	fclose(kbd);

	return 0;
}
