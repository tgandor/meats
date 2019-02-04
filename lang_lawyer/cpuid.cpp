#include <iostream>

int main()
{
  int a, b;

  for (a = 0; a < 5; a++)
  {
    __asm ( "mov %1, %%eax; "            // a into eax
          "cpuid;"
          "mov %%eax, %0;"             // eax into b
          :"=r"(b)                     // output
          :"r"(a)                      // input
          :"%eax","%ebx","%ecx","%edx" // clobbered register
         );
    std::cout << "The code " << a << " gives " << b << std::endl;
  }

  return 0;
}
