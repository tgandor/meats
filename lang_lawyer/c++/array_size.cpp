#include <iostream>

using namespace std;

template <int N>
void array_info(char (&c)[N]) {
    cout << "Array is " << N << " elements long." << endl;
}

int main() {
  char a[4], b[10];
  array_info(a);
  array_info(b);
  return 0;
}
