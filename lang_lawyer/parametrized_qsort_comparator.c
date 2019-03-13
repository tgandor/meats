#include <stdio.h>
#include <stdlib.h>

/*
Source:
https://stackoverflow.com/questions/11284624/sort-an-array-of-arrays-by-different-indexes-in-c
https://stackoverflow.com/a/11285488/1338797
*/

/* this place needed some better casting */
int my_comparator(const void* a, const void* b, int n)
{
    double da = (*(double**)a)[n];
    double db = (*(double**)b)[n];
    printf("Comparing %lf to %lf (by field %d)\n", da, db, n);
    return (da > db) ? 1 : ((da < db) ? -1 : 0);
}

void my_qsort(void* base, size_t num, size_t size,
    int (*comparator)(const void *, const void *, int), int field)
{
    /* Internal comparator */
    int my_qsort_comparator(const void* a, const void* b)
    {
        return comparator(a, b, field);
    }

    /* Invoke the base qsort function */
    qsort(base, num, size, my_qsort_comparator);
}



int main()
{
    double a0[] = { 1.0, 4.0 };
    double a1[] = { 2.0, 3.0 };
    double *a[] = { &a0[0], &a1[0] };

    printf("Sort by? (0/1) ");
    int field;
    scanf("%d", &field);
    if (field != 1) field = 0;
    printf("Sorting by field %d:\n", field);
    my_qsort(a, 2, sizeof(double *), my_comparator, field);
    printf("%.0lf %.0lf\n", a[0][0], a[0][1]);
    printf("%.0lf %.0lf\n", a[1][0], a[1][1]);
    return 0;
}
