#include <iostream>

// -std=c++11
// for && (and decltype, but decltype(std::endl) doesn't work)

struct NullStream // : public std::basic_ostream<_CharT, _Traits>
{
    NullStream();
    template <typename T>
    explicit NullStream(const T& arg);
};

/*
 * equialent to the next one
template <typename T>
NullStream &NullStream::operator<<(T&& arg)
{
    return *this;
}

*/

template <typename T>
NullStream operator<<(NullStream ns, T&& arg)
{
    return ns;
}

/*
 * VS2015 - illegal argument to decltype
NullStream operator<<(NullStream ns, const decltype(std::endl)& arg)
{
    return ns;
}
*/

NullStream::NullStream()
{}

template <typename T>
NullStream::NullStream(const T &arg)
{}

class LoggedConcrete
{
    struct LoggerStream
    {
        LoggerStream(LoggedConcrete* parent);
        template <typename T>
        std::ostream& operator<<(T&& arg);
    private:
        LoggedConcrete* parent_;
        int msgNum;
    };

#ifndef NDEBUG
    typedef LoggerStream DBG;
#else
    typedef NullStream DBG;
#endif

    int value1, value2;
public:
    LoggedConcrete();
    void speak();
};

int main()
{
    LoggedConcrete lc;
    lc.speak();
    return 0;
}


LoggedConcrete::LoggedConcrete() : value1(42), value2(24)
{}

void LoggedConcrete::speak()
{
    DBG(this) << "My value2 is: " << value1 << '\n';
    // <<  std::endl; - template argument deduction/substitution failed
}


LoggedConcrete::LoggerStream::LoggerStream(LoggedConcrete *parent) : parent_(parent), msgNum(0)
{}

template <typename T>
std::ostream& LoggedConcrete::LoggerStream::operator<<(T&& arg)
{
    ++msgNum;
    return std::cout << msgNum << ": LoggedConcrete with value1=" << parent_->value1
                     << " says: " << std::forward(arg);
}
