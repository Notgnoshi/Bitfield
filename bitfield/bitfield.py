class Bitfield(object):
    """
        A Bitfield class to provide easier bit manipulations.

        Example:
        >>> b = Bitfield(0b11001010)
        >>> assert 0b1010 == b[:4]
        >>> assert 0b1100 == b[4:]
        >>> assert 0b01010011 == b[::-1]
        >>> b[1::2] = 0b1111
        >>> assert 0b11101010
        >>> b[1::2] = 0b1000
        >>> assert 0b11000000 == b
    """

    def __init__(self, value, width=None):
        """
            Constructs a Bitfield from an integer and an optional Bitfield width.

            If the Bitfield width is not given, the width will be determined by the index of the
            most significant 1 bit.

            Example:
            >>> b = Bitfield(0b0011, width=4)
            >>> len(b)
            4
            >>> list(b)  # equivalent to [bit for bit in b]
            [1, 1, 0, 0]
            >>> c = Bitfield(0b0011)
            >>> len(c)
            2
            >>> list(c)
            [1, 1]
        """
        self.width = width
        self.value = value

    @property
    def value(self):
        if self.__fixed_width_flag:
            # When ANDing a small number, say 0b100 with a larger number, say 0b1100, Python
            # will bring in zeros in the smaller number to bring the two to the same width. Thus we
            # would get 0b100 & 0b1100 --> 0b0100 & 0b1100 --> 0b0100 --> 0b100
            mask = (0b1 << self.width) - 1
            return self.__value & mask
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__fixed_width_flag = width is not None
        self.__width = width

    def __len__(self):
        if self.__fixed_width_flag:
            return self.width
        return self.value.bit_length()

    def __getitem__(self, key):
        """
            Return the bit(s) at the given key(s). Shifts the bits down until *only* the requested
            bits are returned.
            Example:
            >>> b = Bitfield(0b1111)
            >>> bin(b[:])
            '0b1111'
            >>> bin(b[::2])
            '0b11'
            >>> b = Bitfield(0b11001100)
            >>> bin(b[1::3])
            '0b100'
            >>> bin(b[::-1])
            '0b110011'
        """
        length = len(self)
        if isinstance(key, int):
            if key >= length or key < -length:
                raise IndexError('Bitfield index out of range')

            if key < 0:
                key *= -1
                key = length - key
            mask = 1 << key

            return self.__class__((self.value & mask) >> key)
        elif isinstance(key, slice):
            if key.stop is not None and key.stop > length:
                raise IndexError('Bitfield index out of range')

            # Leverage existing Python data structures that support full slicing in order to avoid
            # implementing all of the different combinations and subtleties.

            # Map (0, 1, 2, ...) to the desired indices indicated by the slice.
            old_indices = tuple(range(length))[key]
            val = 0b0
            for new_index, old_index in zip(range(length), old_indices):
                # Get the sliced indexth bit of self.value
                b = self.value & (1 << old_index)
                # Move the bit down to the LSB
                b >>= old_index
                # Move the bit up to the MSB of the view
                b <<= new_index
                val |= b

            return self.__class__(val)
        else:
            raise TypeError(f'unsupported index type: {type(key)}')

    def __setitem__(self, key, value):
        """
            Sets the bit(s) at the given key to the provided value. The provided value will be
            shifted left automatically. Thus to set the middle two bits of 0b1001 all that is
            needed is the following:

            >>> b = Bitfield(0b1001)
            >>> b[1:3] = 0b11
            >>> bin(b)
            '0b1111'

            Rather than the following (wrong) example:

            >>> b = Bitfield(0b1001)
            >>> b[1:3] = 0b110
            >>> bin(b)
            '0b1101'

            This method is provided to eliminate the need for masking:

            >>> b = Bitfield(0b1001)
            >>> mask = 0b0110
            >>> b = b & ~mask  # Clear the middle two bits
            >>> new_middle_values = 0b11
            >>> new_middle_values <<= 1
            >>> b |= new_middle_values  # Set both the middle bits to 1
            >>> bin(b)
            '0b1111'

            Example:
            >>> b = Bitfield(0b1010)
            >>> b[2] = 1
            >>> bin(b)
            '0b1110'
            >>> b[:] = 0
            >>> bin(b)
            '0b0'
        """
        length = len(self)
        if isinstance(key, int):
            if key >= length or key < -length:
                raise IndexError('Bitfield index out of range')

            if key < 0:
                key *= -1
                key = length - key
            mask = 1 << key

            # Clear the bit of interest:
            self.value &= ~mask
            value <<= key
            self.value |= value
            return
        elif isinstance(key, slice):
            if key.stop is not None and key.stop > length:
                raise IndexError('Bitfield index out of range')

            # Leverage existing Python data structures that support full slicing in order to avoid
            # implementing all of the different combinations and subtleties.

            # Map (0, 1, 2, ...) to the desired indices indicated by the slice.
            indices = tuple(range(length))[key]
            expanded = 0b0
            mask = 0b0
            # Not the same as using enumerate, because length could be less than len(indices)
            for val_index, new_index in zip(range(length), indices):
                # Generate a mask of the bits of interest
                mask |= (1 << new_index)

                # Get the ith bit of value
                b = value & (1 << val_index)
                # Move bit down to the LSB
                b >>= val_index
                # Move bit to its new location
                b <<= new_index
                expanded |= b

            # Clear out the bits of interest
            self.value &= ~mask
            self.value |= expanded
        else:
            raise TypeError(f'unsupported index type: {type(key)}')

    def __delitem__(self, key):
        """
            Deletes the given keyth values from the bitfield. Does not clear them, it removes them.

            Example:
            >>> b = Bitfield(0b1001)
            >>> del b[0]
            >>> bin(b)
            '0b100'
            >>> b = Bitfield(0b1011101)
            >>> del b[3]
            >>> bin(b)
            '0b101101'
            >>> del b[2:4]
            >>> bin(b)
            '0b1001'
            >>> del b[1:3]
            >>> bin(b)
            '0b11'
        """
        length = len(self)
        if isinstance(key, int):
            if key >= length or key < -length:
                raise IndexError('Bitfield index out of range')

            if key < 0:
                key *= -1
                key = length - key

            right, left = self[:key], self[key + 1:]
            left <<= key
            self.value = int(left) | int(right)
        elif isinstance(key, slice):
            indices = list(range(length))
            del indices[key]
            val = 0b0
            for new_index, old_index in zip(range(length), indices):
                # Get the sliced indexth bit of self.value
                b = self.value & (1 << old_index)
                # Move the bit down to the LSB
                b >>= old_index
                # Move the bit up to the MSB of the view
                b <<= new_index
                val |= b
            self.value = val
        else:
            raise TypeError(f'unsupported index type: {type(key)}')

    def __reversed__(self):
        """
            Reverses the endianness.
            Example:
            >>> bin(reversed(Bitfield(0b1010)))
            '0b101'
        """
        return self[::-1]

    def __repr__(self):
        return self.value.__repr__()

    """
    Use the underlying integer's magic methods so that Bitfields can be treated exactly like
    integers. Unfortunately, these *do* have to be explicitly listed out like this.
    """

    def __hash__(self):
        """
            Makes Bitfields hashable by hashing their underlying value.

            Example:
            >>> b = Bitfield(0b1010)
            >>> hash(b)
            10
        """
        return hash(self.value)

    def __int__(self):
        """
            Allows for converting Bitfields to integers

            Example:
            >>> b = Bitfield(0b1010)
            >>> type(int(b))
            <class 'int'>
            >>> int(b) == 0b1010
            True
        """
        return self.value

    def __index__(self):
        """
            Allows Python to treat Bitfields as integers, allowing for the use of bin(), hex(),
            and oct() on Bitfields

            Example:
            >>> b = Bitfield(0b1010)
            >>> bin(b)
            '0b1010'
        """
        return self.__int__()

    def __neg__(self):
        return self.__class__(self.value.__neg__())

    def __pos__(self):
        return self.__class__(self.value.__pos__())

    def __abs__(self):
        return self.__class__(self.value.__abs__())

    def __invert__(self):
        return self.__class__(self.value.__invert__())

    """
    Begin awful boilerplate code to make Bitfields act just like integers. Subclassing isn't an
    option because ints are immutable, and that throws out the whole point of using __getitem__
    and __setitem__.
    """

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__add__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__add__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for +: Bitfield and {type(other)}')

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__sub__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__sub__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for -: Bitfield and {type(other)}')

    def __rsub__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__rsub__(other))
        else:
            raise TypeError(f'unsupported operand type(s) for -: {type(other)} and Bitfield')

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__mul__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__mul__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for *: Bitfield and {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return self.value.__truediv__(other)
        elif isinstance(other, Bitfield):
            return self.value.__truediv__(other.value)
        else:
            raise TypeError(f'unsupported operand type(s) for /: Bitfield and {type(other)}')

    def __rtruediv__(self, other):
        if isinstance(other, int):
            return self.value.__rtruediv__(other)
        else:
            raise TypeError(f'unsupported operand type(s) for /: {type(other)} and Bitfield')

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__floordiv__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__floordiv__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for //: Bitfield and {type(other)}')

    def __rfloordiv__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__rfloordiv__(other))
        else:
            raise TypeError(f'unsupported operand type(s) for //: {type(other)} and Bitfield')

    def __mod__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__mod__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__mod__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for %: Bitfield and {type(other)}')

    def __rmod__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__rmod__(other))
        else:
            raise TypeError(f'unsupported operand type(s) for %: {type(other)} and Bitfield')

    def __pow__(self, other, modulus=None):
        if isinstance(other, int):
            return self.__class__(self.value.__pow__(other, modulus))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__pow__(other.value, modulus))
        else:
            raise TypeError(f'unsupported operand type(s) for **: Bitfield and {type(other)}')

    def __rpow__(self, other, modulus=None):
        if isinstance(other, int):
            return self.__class__(self.value.__rpow__(other, modulus))
        else:
            raise TypeError(f'unsupported operand type(s) for **: {type(other)} and Bitfield')

    def __lshift__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__lshift__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__lshift__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for <<: Bitfield and {type(other)}')

    def __rlshift__(self, other):
        return self.__lshift__(other)

    def __rshift__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__rshift__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__rshift__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for >>: Bitfield and {type(other)}')

    def __rrshift__(self, other):
        return self.__rshift__(other)

    def __and__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__and__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__and__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for &: Bitfield and {type(other)}')

    def __rand__(self, other):
        return self.__and__(other)

    def __xor__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__xor__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__xor__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for ^: Bitfield and {type(other)}')

    def __rxor__(self, other):
        return self.__xor__(other)

    def __or__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__or__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__or__(other.value))
        else:
            raise TypeError(f'unsupported operand type(s) for |: Bitfield and {type(other)}')

    def __ror__(self, other):
        return self.__or__(other)

    def __iadd__(self, other):
        if isinstance(other, int):
            self.value += other
            return self
        elif isinstance(other, Bitfield):
            self.value += other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for +=: Bitfield and {type(other)}')

    def __isub__(self, other):
        if isinstance(other, int):
            self.value -= other
            return self
        elif isinstance(other, Bitfield):
            self.value -= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for -=: Bitfield and {type(other)}')

    def __imul__(self, other):
        if isinstance(other, int):
            self.value *= other
            return self
        elif isinstance(other, Bitfield):
            self.value *= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for *=: Bitfield and {type(other)}')

    def __ifloordiv__(self, other):
        if isinstance(other, int):
            self.value //= other
            return self
        elif isinstance(other, Bitfield):
            self.value //= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for //=: Bitfield and {type(other)}')

    def __imod__(self, other):
        if isinstance(other, int):
            self.value %= other
            return self
        elif isinstance(other, Bitfield):
            self.value %= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for %=: Bitfield and {type(other)}')

    def __ipow__(self, other, modulus=None):
        if isinstance(other, int):
            self.value = pow(self.value, other, modulus)
            return self
        elif isinstance(other, Bitfield):
            self.value = pow(self.value, other.value, modulus)
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for **=: Bitfield and {type(other)}')

    def __ilshift__(self, other):
        if isinstance(other, int):
            self.value <<= other
            return self
        elif isinstance(other, Bitfield):
            self.value <<= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for <<=: Bitfield and {type(other)}')

    def __irshift__(self, other):
        if isinstance(other, int):
            self.value >>= other
            return self
        elif isinstance(other, Bitfield):
            self.value >>= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for >>=: Bitfield and {type(other)}')

    def __iand__(self, other):
        if isinstance(other, int):
            self.value &= other
            return self
        elif isinstance(other, Bitfield):
            self.value &= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for &=: Bitfield and {type(other)}')

    def __ixor__(self, other):
        if isinstance(other, int):
            self.value ^= other
            return self
        elif isinstance(other, Bitfield):
            self.value ^= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for ^=: Bitfield and {type(other)}')

    def __ior__(self, other):
        if isinstance(other, int):
            self.value |= other
            return self
        elif isinstance(other, Bitfield):
            self.value |= other.value
            return self
        else:
            raise TypeError(f'unsupported operand type(s) for |=: Bitfield and {type(other)}')

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value.__eq__(other)
        elif isinstance(other, Bitfield):
            return self.value.__eq__(other.value)
        return False

    def __ne__(self, other):
        if isinstance(other, int):
            return self.value.__ne__(other)
        elif isinstance(other, Bitfield):
            return self.value.__ne__(other.value)
        return True

    def __le__(self, other):
        if isinstance(other, int):
            return self.value.__le__(other)
        elif isinstance(other, Bitfield):
            return self.value.__le__(other.value)
        return False

    def __ge__(self, other):
        if isinstance(other, int):
            return self.value.__ge__(other)
        elif isinstance(other, Bitfield):
            return self.value.__ge__(other.value)
        return False

    def __gt__(self, other):
        if isinstance(other, int):
            return self.value.__gt__(other)
        elif isinstance(other, Bitfield):
            return self.value.__gt__(other.value)
        return False

    def __lt__(self, other):
        if isinstance(other, int):
            return self.value.__lt__(other)
        elif isinstance(other, Bitfield):
            return self.value.__lt__(other.value)
        return False
