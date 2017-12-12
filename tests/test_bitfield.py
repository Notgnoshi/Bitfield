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
