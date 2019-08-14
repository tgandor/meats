// compile (link) with: -lgtest

template <class Base, class Factor>
Base multiply(Base base, Factor factor)
{
    Base result = Base();
    for (;;)
    {
        if (factor & 1)
        {
            result += base;
        }

        factor >>= 1;
        if (!factor)
            break;

        base += base;
    }

    return result;
}

template <class Base, class Exponent>
Base power(Base base, Exponent exponent)
{
    Base result = Base(1);
    for (;;)
    {
        if (exponent & 1)
        {
            result *= base;
        }

        exponent >>= 1;
        if (!exponent)
            break;

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

int main(int argc, char *argv[])
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}