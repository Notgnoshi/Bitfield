# Bitfield
A Python bitfield class for easier bit manipulation of integers

This Python class is motivated by a previous need of mine to iterate over the bits of a bitfield. My original solution was to build a bitstream generator that consumed `bytes` and produced bits. However, in order to accumulate bits into a bitfield for manipulation, it was easiest to use `itertools.islice` and convert to a `tuple`. This was quite inefficient.

`Bitfield` is a partial solution. While it still does not provide any kind of interface to consume the bits of a bitstream, it allows bitwise manipulations extremely easily.

# Examples:
* A `Bitfield` is an `int`, along with all of the operations that can be performed on an `int`:
    ```python
    >>> from bitfield import Bitfield
    >>> bits = Bitfield(0b1010)
    >>> bin(bits)
    '0b1010'
    >>> bin(bits + 1)
    '0b1110'
    >>> bin(bits << 2)
    '0b101000'
    >>> bin(bits >> 2)
    '0b10'
    ```

    Unfortunately, `int`s are immutable, so any subclass of an `int` must also be immutable. Subclassing an `int` would provide the above functionality for free, without all of the nasty duplicated code I have, but would destroy one of the bigger reasons this class exists in the first place: mutability using `__setitem__`.
* A `Bitfield` also has a `__len__` and a `__getitem__`, and is thus an iterable. This is the main difference between a `Bitfield` and an `int`.
    ```python
    >>> from bitfield import Bitfield
    >>> bits = Bitfield(0b1010)
    >>> len(bits)
    4
    >>> list(bits)  # Equivalent to: [bit for bit in bits]
    [0, 1, 0, 1]
    >>> bits[0]  # Indexed least significant bit first
    0
    >>> bits[1]
    1
    >>> bin(bits[::-1])  # Note: bin(0b0101) will give '0b101'
    '0b101'
    >>> bin(bits[::2])  # Note: 0b00 == 0b0
    '0b0'
    >>> bin(bits[1::2])
    '0b11'
    ```
* Unlike `int`s, `Bitfield`s are mutable, and define a `__setitem__`:
    ```python
    >>> from bitfield import Bitfield
    >>> bits = Bitfield(0b1010)
    >>> bits[0] = 1
    >>> bin(bits)
    '0b1011'
    >>> bits[::2] = 0b10  # Toggles bits 0 and 2
    >>> bin(bits)
    '0b1110'
    ```
* Has an optional width:
    ```python
    >>> from bitfield import Bitfield
    >>> bits = Bitfield(0b0101, width=4)
    >>> 0b0101.bit_length()
    3
    >>> len(bits)
    4
    >>> list(bits)
    [1, 0, 1, 0]
    >>> list(Bitfield(0b0101))
    [1, 0, 1]
    ```
* Implements `__delitem__`:
    ```python
    >>> from bitfield import Bitfield
    >>> bits = Bitfield(0b1001)
    >>> del bits[1:3]
    >>> bin(bits)
    '0b11'
    ```

# TODO:
* Test more extensively with negative numbers -- especially negative fixed width numbers.
* Add classes/functions for working with `bytes` and `bytearray`s
    - Read in successive `Bitfield`s from a file, constructed from `bytes` objects. I'm thinking a generator that takes in an arbitrary sized `bytes` or `bytearray` object and yields `Bitfield`s of a certain size until the `bytes` object is exhausted.
    - `int`s have `to_bytes` and `from_bytes` methods
* Construct a Bitfield from an iterable?
    - Or should the focus be less on streams as on manipulations?
* Add Bit manipulation functions from [`crypto`](https://github.com/Notgnoshi/cryptography) library?
