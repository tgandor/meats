#include <xmmintrin.h>
#include <stdio.h>

typedef union view_m128
{
	__m128 vec;
	int32_t ints[4];
	float floats[4];
} view_m128;

void printv_(__m128 m)
{
	view_m128 view;
	view.vec = m;
	/*
	printf("Ints: %d %d %d %d\n", view.ints[0], view.ints[1],
			view.ints[2], view.ints[3]);
			*/
	printf("%f %f %f %f\n", view.floats[0], view.floats[1],
			view.floats[2], view.floats[3]);
	// etc.
}

#define printv(x) { printf("%s = ", #x); printv_(x); }

int main()
{
	__m128 m = _mm_set_ps(-4, -3, -2, -1);
	__m128 one = _mm_set1_ps(1.0f);

	printv(_mm_and_ps(m, _mm_setzero_ps())); // Always a zero vector
	printv(_mm_or_ps(m, _mm_set1_ps(-0.0f))); // Negate all (nop, all negative)
	printv(_mm_add_ps(m, _mm_setzero_ps())); // Add 0 (nop; x+0=x)
	printv(_mm_sub_ps(m, _mm_setzero_ps())); // Substruct 0 (nop; x-0=x)
	printv(_mm_mul_ps(m, one)); // Multiply by one (nop)
	printv(_mm_div_ps(m, one)); // Division by one (nop)

	return 0;
}
