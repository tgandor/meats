#include <iostream>

// see also: http://en.wikipedia.org/wiki/Return_value_optimization

struct C {
  C() { std::cout << "Default constructor.\n"; }
  C(const C&) { std::cout << "A copy was made.\n"; }
};

C f() {
  return C();
}

int main() {
  std::cout << "Hello World!\n";
  C obj = f();
}
