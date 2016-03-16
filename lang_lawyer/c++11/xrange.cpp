struct Xrange
{
    struct Pseudoiter
    {
        Pseudoiter(int val) : val_(val) {}
        bool operator!=(const Pseudoiter& rhs) { return val_ != rhs.val_; }
        Pseudoiter operator++() { ++val_; return *this; }
        int operator*() { return val_; }
    private:
        int val_;
    };

    Xrange(int count = 0);
    Xrange(int begin, int end);
    Pseudoiter begin() { return begin_; }
    Pseudoiter end() { return end_; }
private:
    Pseudoiter begin_;
    Pseudoiter end_;
};

Xrange::Xrange(int count) :
    begin_(0), end_(count)
{}

Xrange::Xrange(int begin, int end) :
    begin_(begin), end_(end)
{}

#include <iostream>

using namespace std;

int main() {
    for (int i : Xrange(10))
    {
        cout << i << endl;
    }
    return 0;
}
