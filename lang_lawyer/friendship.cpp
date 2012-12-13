#include <iostream>

using namespace std;

class B {
  int x;
  friend class A;
protected:
  int y;
};

class D : public B {};

class A {
  void touchB(B b) { cout << b.x << endl << b.y << endl; }
  void touchD(D b) { cout << b.x << endl << b.y << endl; }
};

class C : public A {
  // void touchB(B b) { cout << b.x << endl << b.y << endl; }
  // void touchD(D b) { cout << b.x << endl << b.y << endl; }
};

int main() {
  return 0;
}
