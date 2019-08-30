// compile (link) with: -lgtest

// why do we need bits_iter class template and bits function template?
// https://stackoverflow.com/questions/984394/why-not-infer-template-parameter-from-constructor

template <class T>
class bits_iter
{
    T value;
public:
    bits_iter(T init_value) : value(init_value) {}
    bool operator*() { return value & 1 == 1; }
    bits_iter<T> begin() { return *this; }
    bits_iter<T> end() { return bits_iter<T>(T()); }
    void operator++() { value >>= 1; }
    bool operator!=(const bits_iter<T>& other) { return value != other.value; }
};

template <class T>
bits_iter<T> bits(T value)
{
    return bits_iter<T>(value);
}

// well, so this is out of date, and the bits_iter could be renamed to bits,
// but then it would require mandatory C++17 support.

template <class Base, class Factor>
Base multiply(Base base, Factor factor)
{
    Base result = Base();
    for (auto bit : bits(factor))
    {
        if (bit)
        {
            result += base;
        }

        base += base;
    }

    return result;
}

template <class Base, class Exponent>
Base power(Base base, Exponent exponent)
{
    Base result = Base(1);
    for (auto bit : bits(exponent))
    {
        if (bit)
        {
            result *= base;
        }

        base *= base;
    }

    return result;
}

class Bignum
{
    // void operator*=(const Bignum& other);
};


#include <gtest/gtest.h>

// region: power tests
TEST(PowerTest, something_to_zero_power)
{
    GTEST_ASSERT_EQ(1, power(2, 0));
}

TEST(PowerTest, something_to_first)
{
    GTEST_ASSERT_EQ(12, power(12, 1));
}

TEST(PowerTest, arbitrary)
{
    GTEST_ASSERT_EQ(5764801, power(7, 8));
}

TEST(PowerTest, floating_point)
{
    GTEST_ASSERT_EQ(6.25, power(2.5, 2));
}
// endregion: power tests

TEST(MultiplyTest, arbitrary)
{
    GTEST_ASSERT_EQ(56, multiply(7, 8));
}

TEST(MultiplyTest, float_by_int)
{
    GTEST_ASSERT_EQ(15.0f, multiply(7.5f, 2));
}

#include <string>

TEST(MultiplyTest, string_by_int)
{
    GTEST_ASSERT_EQ(std::string("aaaaa"), multiply(std::string("a"), 5));
}

TEST(BitsTest, test_iteration)
{
    int v = 234;
    auto iterator = bits(v);
    for (auto bit : iterator)
    {
        GTEST_ASSERT_EQ(bit, v & 1 == 1);
        v >>= 1;
    }
}

TEST(BitsTest, test_number_of_bits)
{
    int num_bits = 0;
    for (auto bit : bits(8))
    {
        ++num_bits;
    }
    GTEST_ASSERT_EQ(num_bits, 4);
}

int main(int argc, char *argv[])
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}