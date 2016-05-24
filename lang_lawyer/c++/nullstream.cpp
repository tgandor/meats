#include <iostream>
#include <iomanip>

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
NullStream operator<<(NullStream ns, T&& /* arg */)
{
    return ns;
}

typedef std::basic_ostream<char, std::char_traits<char>> ostream_char;
NullStream operator<<(NullStream ns, ostream_char& (* /* arg */)(ostream_char&))
{
    return ns;
}

// (below) seems not necessary, ostream&(*)(ostream) overload is enough.
// However, when only this available - setw() and boolalpha work,
// and endl doesn't

//NullStream operator<<(NullStream ns, std::ios_base& (* /* arg */)(std::ios_base&))
//{
//    return ns;
//}

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
    DBG(this) << "My value2 is: " << value1 << std::endl;
}


LoggedConcrete::LoggerStream::LoggerStream(LoggedConcrete *parent) : parent_(parent), msgNum(0)
{}

template <typename T>
std::ostream& LoggedConcrete::LoggerStream::operator<<(T&& arg)
{
    ++msgNum;
    return std::cout << std::boolalpha << true << " " // manipulators
                     <<  std::setw(4) << msgNum // manipulators continued
                     << ": LoggedConcrete with value1=" << parent_->value1
                     << " says: "
                     << std::forward<T>(arg); // forward arg, no copying
}
