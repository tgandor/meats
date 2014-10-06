#include <stdio.h>
#include <cpuid.h>

int main()
{
	unsigned int i, idmax, eax, ebx, ecx, edx;
	idmax =__get_cpuid_max(0, 0);
	printf("Max cpuid level (basic): %u\n", idmax);
	for (i=0; i <= idmax; ++i)
	{
		__get_cpuid(i, &eax, &ebx, &ecx, &edx);
		printf("%u: eax=%08x ebx=%08x ecx=%08x edx=%08x\n", i, eax, ebx, ecx, edx);
	}
	return 0;
}
