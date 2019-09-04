// compile (link) with: -lgtest

#include <gtest/gtest.h>

// why do we need bits_iter class template and bits function template?
// https://stackoverflow.com/questions/984394/why-not-infer-template-parameter-from-constructor

// https://stackoverflow.com/a/1724039/1338797
// wow, thanks SO!
// I almost went through the pain of fully specifying iterator_traits
// myself. But sometimes it's enough to inherit...
template <class T>
class bits_iter : public std::iterator<std::input_iterator_tag, bool>
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

#include <vector>

std::vector<int> segment(int value, int modulus)
{
    std::vector<int> result;

    do {
        result.push_back(value % modulus);
        value /= modulus;
    } while (value);

    return result;
}

class Bignum
{
    std::vector<int> bin_segments;
    std::vector<int> dec_segments;
public:
    static const int BIN_MOD = 1 << 10;
    static const int DEC_MOD = 1000;

    Bignum(int value = 0) :
        bin_segments(segment(value, BIN_MOD)),
        dec_segments(segment(value, DEC_MOD))
    {}

    Bignum(const Bignum& other) = default;

    Bignum operator+(const Bignum& other);

    bool operator==(const Bignum& other) const
    {
        return dec_segments == other.dec_segments && bin_segments == other.bin_segments;
    }

    const std::vector<int>& chunks() const { return dec_segments; }

    const std::vector<int>& bin_chunks() const { return bin_segments; }
};

std::string dec(const Bignum& num)
{
    std::string result;
    for(int i = 0; i < num.chunks().size() - 1; ++i)
    {
        int val = num.chunks()[i];

        for (int f = Bignum::DEC_MOD / 10; f > 0; f /= 10)
        {
            result += ('0' + val % 10);
            val /= 10;
        }
    }

    int val = num.chunks().back();
    while (val > 0)
    {
        result += ('0' + val % 10);
        val /= 10;
    }

    std::reverse(result.begin(), result.end());
    return result;
}

std::vector<int> sum_vectors(const std::vector<int>& a, const std::vector<int>& b, int modulus)
{
    std::vector<int> result;
    auto ai = a.begin();
    auto bi = b.begin();
    int carry = 0;
    do {
        if (ai != a.end())
        {
            carry += *ai++;
        }

        if (bi != b.end())
        {
            carry += *bi++;
        }

        result.push_back(carry % modulus);
        carry /= modulus;
    } while (carry || ai != a.end() || bi != b.end());

    return result;
}

Bignum Bignum::operator+(const Bignum& other)
{
    Bignum result;
    result.bin_segments = sum_vectors(this->bin_segments, other.bin_segments, BIN_MOD);
    result.dec_segments = sum_vectors(this->dec_segments, other.dec_segments, DEC_MOD);
    return result;
}

template <>
class bits_iter<Bignum> : public std::iterator<std::input_iterator_tag, bool>
{
    bool done;
    Bignum value;
    int chunk_index;
    int flag_mask;
    int last_chunk;
public:
    bits_iter() : done(true), value() {}
    bits_iter(Bignum init_value) :
        done(false), value(init_value),
        chunk_index(0), flag_mask(1),
        last_chunk(value.bin_chunks().back())
    {}
    bool operator*() {
        if (chunk_index < value.bin_chunks().size() - 1)
        {
            return (value.bin_chunks()[chunk_index] & flag_mask) != 0;
        }

        return (last_chunk & 1) == 1;
    }
    bits_iter<Bignum> begin() { return *this; }
    bits_iter<Bignum> end() { return bits_iter<Bignum>(); }
    void operator++() {
        if (chunk_index < value.bin_chunks().size() - 1)
        {
            flag_mask <<= 1;
            if (flag_mask == Bignum::BIN_MOD)
            {
                flag_mask = 1;
                ++chunk_index;
            }
            return;
        }

        last_chunk >>= 1;
        if (last_chunk == 0)
        {
            done = true;
        }
    }
    bool operator!=(const bits_iter<Bignum>& other) { return done != other.done; }
};

template <class T>
std::string bin(const T& value)
{
    std::string result;
    for (auto bit : bits(value))
    {
        result.push_back(bit ? '1' : '0');
    }

    std::reverse(result.begin(), result.end());
    return result;
}

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

TEST(BitsTest, bin_to_string)
{
    GTEST_ASSERT_EQ("1010", bin(10));
}

TEST(Bignum, addition)
{
    GTEST_ASSERT_EQ(Bignum(5511) + Bignum(5522), Bignum(11033));
}

TEST(Bignum, dec)
{
    GTEST_ASSERT_EQ("11033", dec(Bignum(11033)));
    GTEST_ASSERT_EQ("987654321", dec(Bignum(987654321)));
}

TEST(BignumBitsIter, compare_with_int_bits_length)
{
    const int VALUE = 12345678;
    auto int_bits = bits(VALUE);
    auto bignum_bits = bits(Bignum(VALUE));
    auto len_int = std::distance(int_bits.begin(), int_bits.end());
    auto len_bignum = std::distance(bignum_bits.begin(), bignum_bits.end());
    GTEST_ASSERT_EQ(len_int, len_bignum);
}

TEST(BignumBitsIter, compare_with_string_value)
{
    const int VALUE = 12345678;
    GTEST_ASSERT_EQ("101111000110000101001110", bin(Bignum(VALUE)));
}

TEST(BignumBitsIter, compare_with_int_bits_values)
{
    const int VALUE = 12345678;
    auto int_bits = bits(VALUE);
    auto bignum_bits = bits(Bignum(VALUE));
    GTEST_ASSERT_EQ(true, std::equal(int_bits.begin(), int_bits.end(), bignum_bits.begin()));
}

int main(int argc, char *argv[])
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
