#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int naive_is_prime(int n)
{
	if (n < 2)
		return 0;
	int d;
	for (d=2; d*d <= n; ++d)
	{
		if (n % d == 0)
			return 0;
	}
	// printf("%d - prime\n", n);
	return 1;
}

int main()
{
	// printf("Num threads: %d\n", omp_get_num_threads()); // == 1 in sequential
	// int counts[16] = {0};
	int *counts;
	int limit;
	puts("Count primes up to?");
	scanf("%d", &limit);
#pragma omp parallel shared(counts)
	{
		int N = omp_get_num_threads();
		int id = omp_get_thread_num();
		int i;
#pragma omp master
		{
		counts = (int*) calloc(N, sizeof(int));
		}
#pragma omp barrier
#pragma omp for
		for (i=0; i<limit; ++i)
		{
			if (naive_is_prime(i))
				++counts[id];
		}
#pragma omp master
		{
			printf("Num threads: %d\n", omp_get_num_threads());
			int total = 0;
			for (i=0; i<N; ++i)
			{
				printf("%d: %d\n", i, counts[i]);
				total += counts[i];
			}
			printf("Total: %d\n", total);
		}
	}
	return 0;
}

