#include <iostream>

// -std=c++11 [-DNDEBUG]

template <typename _Elem, typename _Traits> struct NullStream // : public std::basic_ostream<_CharT, _Traits>
{
    NullStream()
    {
    }
    template <typename T>
    explicit NullStream(const T& arg);
};

template <typename _Elem, typename _Traits, typename T>
NullStream<_Elem, _Traits> operator<<(NullStream<_Elem, _Traits> ns, T&& arg)
{
    // std::cout << __FUNCTION__ << ':' << __LINE__ << std::endl;
    return ns;
}

// MSVC, Clang 3.6 and GCC 4.8 needs this templated overload:
// also, this seems standard-compliant, but GCC 6 does fine without
template <typename _Elem, typename _Traits>
NullStream<_Elem, _Traits> operator<<(
        NullStream<_Elem, _Traits> ns,
        std::basic_ostream<_Elem, _Traits>& (*)(std::basic_ostream<_Elem, _Traits>&))
{
    // std::cout << __FUNCTION__ << ':' << __LINE__ << std::endl;
    return ns;
}

template <typename _Elem, typename _Traits> template <typename T>
NullStream<_Elem, _Traits>::NullStream(const T &arg)
{
}

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
    typedef NullStream<char, std::char_traits<char>> DBG;
#endif

    int value1, value2;
    public:
    LoggedConcrete();
    void speak();
};

int main()
{
    std::cout << std::endl;
    LoggedConcrete lc;
    lc.speak();
    return 0;
}


LoggedConcrete::LoggedConcrete() : value1(42), value2(24)
{
}

void LoggedConcrete::speak()
{
    DBG(this) << "My value2 is: " << value1 << std::endl;
}


LoggedConcrete::LoggerStream::LoggerStream(LoggedConcrete *parent) : parent_(parent), msgNum(0)
{
}

template <typename T>
std::ostream& LoggedConcrete::LoggerStream::operator<<(T&& arg)
{
    ++msgNum;
    return std::cout << msgNum << ": LoggedConcrete with value1=" << parent_->value1 << " says: " << arg;
}
