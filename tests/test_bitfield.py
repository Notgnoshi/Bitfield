import unittest
from bitfield import Bitfield as B

a = B(0b0011)
b = B(0b1100)
c = 0b0011
d = 0b1100


class BitfieldOperatorsTest(unittest.TestCase):
    def test_neg(self):
        self.assertEqual(-a, -c)
        self.assertNotEqual(a, -a)

    def test_pos(self):
        self.assertEqual(+a, a)
        self.assertNotEqual(+a, -a)

    def test_abs(self):
        self.assertEqual(abs(-a), a)
        self.assertEqual(abs(a), a)

    def test_invert(self):
        self.assertEqual(~a, ~c)
        self.assertEqual(~b, ~d)

    def test_equality(self):
        # Bitfield and ints
        self.assertEqual(a, c)
        self.assertNotEqual(a, d)
        # Bitfield and Bools
        self.assertEqual(B(0b1), True)
        self.assertNotEqual(B(0b0), True)
        # Bitfield and Bitfield
        self.assertEqual(a, B(0b0011))
        self.assertNotEqual(a, b)
        # Bitfield and some non-number type
        self.assertNotEqual(a, [0, 0, 1, 1])

    def test_add(self):
        # Add two of the same type
        self.assertEqual(a + b, c + d)
        # Add Bitfield to int
        self.assertEqual(a + d, c + d)
        self.assertEqual(d + a, c + d)
        # Above operations should return Bitfields
        self.assertTrue(isinstance(a + b, B))
        self.assertTrue(isinstance(a + d, B))
        self.assertTrue(isinstance(d + a, B))
        self.assertRaises(TypeError, a.__add__, None)
        self.assertRaises(TypeError, a.__radd__, None)

    def test_sub(self):
        # Two Bitfields
        self.assertEqual(a - b, c - d)
        # Bitfield and int
        self.assertEqual(a - d, c - d)
        self.assertEqual(d - a, d - c)
        # Above operations should return Bitfields
        self.assertTrue(isinstance(a - b, B))
        self.assertTrue(isinstance(a - d, B))
        self.assertTrue(isinstance(d - a, B))
        self.assertRaises(TypeError, a.__sub__, None)
        self.assertRaises(TypeError, a.__rsub__, None)

    def test_mul(self):
        self.assertEqual(a * b, c * d)
        self.assertEqual(a * d, c * d)
        self.assertEqual(d * a, d * c)
        self.assertTrue(isinstance(a * b, B))
        self.assertTrue(isinstance(a * d, B))
        self.assertTrue(isinstance(d * a, B))
        self.assertRaises(TypeError, a.__mul__, None)
        self.assertRaises(TypeError, a.__rmul__, None)

    def test_div(self):
        self.assertEqual(a / b, c / d)
        self.assertEqual(a / d, c / d)
        self.assertEqual(d / a, d / c)
        self.assertTrue(isinstance(a / b, float))
        self.assertTrue(isinstance(a / d, float))
        self.assertTrue(isinstance(d / a, float))
        self.assertRaises(TypeError, a.__truediv__, None)
        self.assertRaises(TypeError, a.__rtruediv__, None)

        self.assertEqual(a // b, c // d)
        self.assertEqual(a // d, c // d)
        self.assertEqual(d // a, d // c)
        self.assertTrue(isinstance(a // b, B))
        self.assertTrue(isinstance(a // d, B))
        self.assertTrue(isinstance(d // a, B))
        self.assertRaises(TypeError, a.__floordiv__, None)
        self.assertRaises(TypeError, a.__rfloordiv__, None)

    def test_mod(self):
        self.assertEqual(a % b, c % d)
        self.assertEqual(a % d, c % d)
        self.assertEqual(d % a, d % c)
        self.assertTrue(isinstance(a % b, B))
        self.assertTrue(isinstance(a % d, B))
        self.assertTrue(isinstance(d % a, B))
        self.assertRaises(TypeError, a.__mod__, None)
        self.assertRaises(TypeError, a.__rmod__, None)

    def test_pow(self):
        self.assertEqual(a ** b, c ** d)
        self.assertEqual(a ** d, c ** d)
        self.assertEqual(d ** a, d ** c)
        self.assertTrue(isinstance(a ** b, B))
        self.assertTrue(isinstance(a ** d, B))
        self.assertTrue(isinstance(d ** a, B))
        self.assertRaises(TypeError, a.__pow__, None)
        self.assertRaises(TypeError, a.__rpow__, None)

        p = 13
        self.assertEqual(pow(a, b, p), pow(c, d, p))
        self.assertEqual(pow(a, d, p), pow(c, d, p))
        self.assertEqual(a.__rpow__(d, p), pow(d, c, p))
        self.assertTrue(isinstance(pow(a, b, p), B))
        self.assertTrue(isinstance(pow(a, d, p), B))
        self.assertRaises(TypeError, a.__pow__, None)
        self.assertRaises(TypeError, a.__rpow__, None)

    @unittest.expectedFailure
    def test_int_bit_pow(self):
        p = 13
        # It does not appear as if using pow(int, Bitfield, int) will call __rpow__
        self.assertEqual(pow(d, a, p), pow(d, c, p))
        self.assertTrue(isinstance(pow(d, a, p), B))

    def test_shifts(self):
        self.assertEqual(a << 2, c << 2)
        self.assertEqual(a >> 2, c >> 2)
        self.assertEqual(b << a, d << c)
        self.assertEqual(b >> a, d >> c)
        self.assertTrue(isinstance(a << 2, B))
        self.assertTrue(isinstance(a << b, B))
        self.assertTrue(isinstance(a >> 2, B))
        self.assertTrue(isinstance(a >> b, B))

    def test_and(self):
        self.assertEqual(a & b, 0b0000)
        self.assertEqual(a & a, 0b0011)
        self.assertEqual(a & ~a, 0b0000)
        self.assertEqual(a & 0b0011, 0b0011)
        self.assertEqual(a & 0b1100, 0b0000)
        self.assertEqual(a & ~0b0011, 0b0000)
        self.assertEqual(0b0011 & a, 0b0011)
        self.assertEqual(0b1100 & a, 0b0000)
        self.assertEqual(~0b0011 & a, 0b0000)
        self.assertTrue(isinstance(a & 2, B))
        self.assertTrue(isinstance(a & b, B))
        self.assertTrue(isinstance(2 & a, B))

    def test_xor(self):
        self.assertEqual(a ^ b, 0b1111)
        self.assertEqual(a ^ a, 0b0000)
        self.assertEqual(a ^ ~a, -0b0001)
        self.assertEqual(a ^ 0b0011, 0b0000)
        self.assertEqual(a ^ 0b1100, 0b1111)
        self.assertEqual(a ^ ~0b0011, -0b0001)
        self.assertEqual(0b0011 ^ a, 0b0000)
        self.assertEqual(0b1100 ^ a, 0b1111)
        self.assertEqual(~0b0011 ^ a, -0b0001)
        self.assertTrue(isinstance(a ^ 0b0011, B))
        self.assertTrue(isinstance(a ^ b, B))
        self.assertTrue(isinstance(0b0011 ^ a, B))

    def test_or(self):
        self.assertEqual(a | b, 0b1111)
        self.assertEqual(a | a, 0b0011)
        self.assertEqual(a | ~a, -0b0001)
        self.assertEqual(a | 0b0011, 0b0011)
        self.assertEqual(a | 0b1100, 0b1111)
        self.assertEqual(a | ~0b0011, -0b0001)
        self.assertEqual(0b0011 | a, 0b0011)
        self.assertEqual(0b1100 | a, 0b1111)
        self.assertEqual(~0b0011 | a, -0b0001)
        self.assertTrue(isinstance(a | 0b0011, B))
        self.assertTrue(isinstance(a | b, B))
        self.assertTrue(isinstance(0b0011 | a, B))

    def test_iadd(self):
        a1 = B(0b0001)
        a2 = B(0b1000)

        a1 += 1
        self.assertEqual(a1, 0b0010)
        a1 += a2
        self.assertEqual(a1, 0b1010)

    def test_isub(self):
        a1 = B(0b0001)
        a2 = B(0b1000)

        a1 -= 1
        self.assertEqual(a1, 0b0000)
        a2 -= 0b0001
        self.assertEqual(a2, 0b0111)

    def test_imul(self):
        a1 = B(0b0001)
        a2 = B(0b1000)

        a1 *= 0b0010
        self.assertEqual(a1, 0b0010)
        a2 *= a1
        self.assertEqual(a2, 0b10000)

    @unittest.expectedFailure
    def test_itruediv(self):
        # It does not make sense for an integer bitfield to allow for implementing /=
        a1 = B(0b0001)
        a2 = B(0b1000)
        a1 /= a2
        self.assertTrue(isinstance(a1, B))

    def test_ifloordiv(self):
        a1 = B(0b0001)
        a2 = B(0b1000)

        a2 //= a1
        self.assertEqual(a2, 0b1000)
        a2 //= 2
        self.assertEqual(a2, 0b0100)

    def test_imod(self):
        a1 = B(8)
        a2 = B(7)

        a1 %= a2
        self.assertEqual(a1, 1)

    def test_ipow(self):
        a1 = B(0b1000)
        a2 = B(0b0010)

        a1 **= a2
        self.assertEqual(a1, 0b1000000)

    def test_ishift(self):
        a1 = B(0b1010)
        a2 = B(0b0101)

        a2 <<= 1
        self.assertEqual(a2, a1)
        a2 >>= 1
        self.assertEqual(a2, 0b0101)
        a1 <<= a2
        self.assertEqual(a1, 0b101000000)

    def test_iand(self):
        a1 = B(0b1010)
        a2 = B(0b0101)

        a1 &= a2
        self.assertEqual(a1, 0b0000)
        a2 &= 0b0100
        self.assertEqual(a2, 0b0100)

    def test_ixor(self):
        a1 = B(0b1010)
        a2 = B(0b0101)

        a1 ^= a2
        self.assertEqual(a1, 0b1111)
        a2 ^= 0b0110
        self.assertEqual(a2, 0b0011)

    def test_ior(self):
        a1 = B(0b1010)
        a2 = B(0b0101)

        a1 |= a2
        self.assertEqual(a1, 0b1111)
        a2 |= 0b0110
        self.assertEqual(a2, 0b0111)


class BitfieldSlicingTest(unittest.TestCase):
    def test_len(self):
        # Bitfields are *not* fixed width.
        self.assertEqual(len(a), 2)
        self.assertEqual(len(b), 4)
        self.assertEqual(len(a << 65), 67)

    def test_getitem(self):
        bits = B(0b1111)

        # Basic bit indexing:
        self.assertEqual(bits[0], 0b0001)
        # Bitfield indexing does *not* produce bits[1] --> 0b0010
        self.assertEqual(bits[1], 0b0001)
        self.assertEqual(bits[-4], 0b1)
        self.assertRaises(IndexError, bits.__getitem__, 4)
        self.assertRaises(IndexError, bits.__getitem__, -5)

        bits = B(0b11110101)
        self.assertEqual(bits[1], 0b0)
        self.assertEqual(bits[7], 0b1)

        # Providing __len__, __getitem__, and raising appropriate IndexError's make Bitfields
        # iterable. Iterates over the bits LSBF.
        self.assertSequenceEqual(bits, [1, 0, 1, 0, 1, 1, 1, 1])

        self.assertTrue(isinstance(bits[0:2], B))

        bits = B(0b101011)

        self.assertEqual(bits[:], bits)
        # Reverse endianness
        self.assertEqual(bits[::-1], 0b110101)
        # Test slicing subtleties
        self.assertEqual(bits[:2], 0b11)
        self.assertEqual(bits[:-1], 0b01011)
        self.assertEqual(bits[0:2], bits[:2])
        self.assertEqual(bits[2:], 0b1010)
        self.assertEqual(bits[2:-1], 0b010)
        # The most significant bit will *always* be 0b1, even in the case bits = B(0b01)
        self.assertEqual(B(0b01)[-1], 0b1)
        self.assertEqual(bits[-1:], 0b1)
        # 6 is not a valid index, but the endpoint is exclusive
        self.assertEqual(bits[2:6], 0b1010)
        self.assertRaises(IndexError, bits.__getitem__, slice(2, 7))
        self.assertEqual(bits[-3:], 0b101)
        self.assertEqual(bits[-4:-2], 0b10)
        self.assertEqual(B(0b10101)[::2], 0b111)
        self.assertEqual(B(0b101010)[1::2], 0b111)
        self.assertEqual(B(0b1100010001)[-2::-2], 0b10101)

    def test_setitem(self):
        bits = B(0b1111)
        bits[:] = 0b1010
        self.assertEqual(bits, 0b1010)
        self.assertTrue(isinstance(bits, B))

        bits[0:2] = 0b00
        self.assertEqual(bits, 0b1000)

        bits[:-1] = 0b111
        self.assertEqual(bits, 0b1111)

    def test_delitem(self):
        bits = B(0b101010101)
        l = len(bits)
        del bits[0]
        self.assertEqual(bits, 0b10101010)
        self.assertEqual(len(bits), l - 1)
        l = len(bits)
        del bits[-1]
        self.assertEqual(bits, 0b101010)
        # We actually just removed two bits because the MSB will always be 1.
        self.assertEqual(len(bits), l - 2)
        l = len(bits)
        del bits[0::2]
        self.assertEqual(bits, 0b111)
        self.assertEqual(len(bits), l - 3)
        del bits[:]
        self.assertEqual(bits, 0b0)
        self.assertEqual(len(bits), 0)
        self.assertEqual(0b0.bit_length(), 0)
        self.assertEqual(0b1.bit_length(), 1)


class BitfieldFixedWidthTest(unittest.TestCase):
    def test_length(self):
        n = 0x891237AB17231FED1273619231
        self.assertGreaterEqual(n.bit_length(), 64)
        q = B(n)
        self.assertEqual(len(q), n.bit_length())
        self.assertEqual(q, n)
        q = B(n, 64)
        self.assertEqual(len(q), 64)
        mask = (0b1 << 64) - 0b1
        # Grab the lowest 64 bits.
        m = n & mask
        self.assertEqual(q, m)

        v = 0b110011001010
        q = B(v, width=4)
        self.assertEqual(0b1010, q)
        self.assertSequenceEqual(q, [0, 1, 0, 1])
        q.width = 8
        self.assertEqual(0b11001010, q)
        q.value = 0b11110000
        self.assertEqual(len(q), 8)
        self.assertEqual(0b11110000, q)
        q.value = v
        q.width = None
        self.assertEqual(len(q), v.bit_length())
        self.assertSequenceEqual(q, [0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1])
