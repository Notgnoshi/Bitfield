import unittest
from bitfield import Bitfield as B


class BitfieldTest(unittest.TestCase):
    def test_equality(self):
        a = B(0b0011)
        b = B(0b1100)
        c = 0b0011
        d = 0b1100

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
        a = B(0b0011)
        b = B(0b1100)
        c = 0b0011
        d = 0b1100

        # Add two of the same type
        self.assertEqual(a + b, c + d)
        # Add Bitfield to int
        self.assertEqual(a + d, c + d)
        self.assertEqual(d + a, c + d)
        # Above operations should return Bitfields
        self.assertTrue(isinstance(a + b, B))
        self.assertTrue(isinstance(a + d, B))
        self.assertTrue(isinstance(d + a, B))
