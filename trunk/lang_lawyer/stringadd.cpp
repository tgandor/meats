#include <iostream>
#include <string>
#include <sstream>

using namespace std;

string& operator+=(string &s, int n) {
    s += ((ostringstream&)(ostringstream() << n)).str();
    return s;
}

int main() {
  string x("abc");
  x += 4;
  cout << x << endl;
  return 0;
}
