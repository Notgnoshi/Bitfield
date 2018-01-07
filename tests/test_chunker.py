import unittest
from bitfield import Bitfield, chunk_file


class ChunkerTest(unittest.TestCase):
    def setUp(self):
        # Path relative to runtests.py
        self.filename = 'tests/assets/rand.dat'
        self.bytes = []
        with open('tests/assets/rand.hexdump', 'r') as hexdump:
            for line in hexdump:
                tokens = line.strip().split()
                # strip off the first and last token
                tokens = tokens[1:-1]
                for byte in tokens:
                    self.bytes.append(int(byte, base=16))

    def test_byte_divisible_1(self):
        with open(self.filename, 'rb') as f:
            chunker = chunk_file(f, 8)
            for read, actual in zip(chunker, self.bytes):
                self.assertEqual(read, actual)

    def test_byte_divisible_2(self):
        nibbles = []
        for byte in self.bytes:
            bits = Bitfield(byte, width=8)
            left, right = bits[:4], bits[4:]
            left.width, right.width = 4, 4
            nibbles.append(left)
            nibbles.append(right)

        with open(self.filename, 'rb') as f:
            chunker = chunk_file(f, 4)
            for read, actual in zip(chunker, nibbles):
                self.assertEqual(read, actual)

    def test_byte_indivisible_1(self):
        chunks = [0b100111, 0b10111, 0b11111, 0b1001, 0b11100]
        with open(self.filename, 'rb') as f:
            chunker = chunk_file(f, 6)
            for read, actual in zip(chunker, chunks):
                self.assertEqual(read, actual)

    def test_byte_indivisible_2(self):
        chunks = [0b111, 0b100, 0b111, 0b010, 0b111, 0b011, 0b001, 0b001, 0b100, 0b011]
        with open(self.filename, 'rb') as f:
            chunker = chunk_file(f, 3)
            for read, actual in zip(chunker, chunks):
                self.assertEqual(read, actual)

    def test_byte_indivisible_3(self):
        chunks = [0b111100111, 0b011111010, 0b100001001]
        with open(self.filename, 'rb') as f:
            chunker = chunk_file(f, 9)
            for read, actual in zip(chunker, chunks):
                self.assertEqual(read, actual)
