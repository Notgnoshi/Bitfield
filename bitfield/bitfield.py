class Bitfield(object):
    """
        A Bitfield class to provide easier bit manipulations.

        Example:
        TODO
    """

    def __init__(self, value):
        self.value = value

    @staticmethod
    def mask(key, length):
        """
            Generate the mask corresponding to the given slice or index and the bitfield length.
            Example:
            >>> bin(Bitfield.mask(slice(0, 2), 4))
            '0b11'
            >>> bin(Bitfield.mask(slice(0, 4), 4))
            '0b1111'
            >>> bin(Bitfield.mask(slice(None, 4), 4))
            '0b1111'
            >>> bin(Bitfield.mask(slice(2), 4))
            '0b11'
            >>> bin(Bitfield.mask(slice(0, -1), 4))
            '0b111'
            >>> bin(Bitfield.mask(slice(0, -2), 4))
            '0b11'
            >>> bin(Bitfield.mask(slice(1, 2), 4))
            '0b10'
            >>> bin(Bitfield.mask(slice(-4, -2), 4))
            '0b11'
        """
        if isinstance(key, int):
            if key < 0:
                key *= -1
                key = length - key

            if key >= length or key < 0:
                raise IndexError('Bitfield index out of range')

            mask = 0b1 << key
        elif isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError('Bitfield slice steps not implemented')
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else length
            # If any of the indices are negative, convert them to their positive counterparts.
            if start < 0:
                start *= -1
                start = length - start

            if stop < 0:
                stop *= -1
                stop = length - stop

            if stop > length:
                raise IndexError('Bitfield index out of range')

            num_bits = stop - start
            mask = ((1 << num_bits) - 1) << start
        return mask

    def __len__(self):
        return self.value.bit_length()

    def __getitem__(self, key):
        """
            Return the bit(s) at the given key(s). Shifts the bits down until *only* the requested
            bits are returned.
            Example:
            >>> b = Bitfield(0b1111)
            >>> bin(b[:])
            '0b1111'
            >>> bin(b[0])
            '0b1'
            >>> bin(b[1])
            '0b1'
            >>> bin(b[2])
            '0b1'
            >>> bin(b[3])
            '0b1'
            >>> bin(b[-1])
            '0b1'
            >>> bin(b[-2])
            '0b1'
            >>> bin(b[-3])
            '0b1'
            >>> bin(b[-4])
            '0b1'
            >>> b[4]
            Traceback (most recent call last):
              ...
            IndexError: Bitfield index out of range
            >>> b[-5]
            Traceback (most recent call last):
              ...
            IndexError: Bitfield index out of range
            >>> bin(b[:2])
            '0b11'
            >>> bin(b[2:])
            '0b11'
            >>> bin(b[:-1])
            '0b111'
            >>> bin(b[-1:])
            '0b1'
            >>> bin(b[0:2])
            '0b11'
            >>> bin(b[::-1])
            '0b1111'
            >>> b = Bitfield(0b1100)
            >>> bin(b[::-1])
            '0b11'
        """
        length = len(self)
        # Special case [::-1] for reversing endianness
        if key == slice(None, None, -1):
            return int(f'{self.value:0{length}b}'[::-1], 2)
        mask = self.mask(key, length)
        temp = self.value & mask

        if mask == 0:
            return 0

        # Shift temp and the mask down as long as the mask has a lowest 0
        while mask & 0b01 == 0b00:
            mask >>= 1
            temp >>= 1

        return temp

    def __setitem__(self, key, value):
        """
            Sets the bit(s) at the given key to the provided value. The provided value will be
            shifted left automatically.
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
        mask = self.mask(key, length)
        # Zero out the chosen values
        temp = self.value & ~mask

        if mask == 0:
            return 0

        # Shift value left and the mask right as long as the mask has a lowest 0
        while mask & 0b01 == 0b00:
            mask >>= 1
            value <<= 1

        # Fuck. ints are immutable, so this line has no effect if subclassing from int
        self.value = temp | value

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

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value.__eq__(other)
        elif isinstance(other, Bitfield):
            return self.value.__eq__(other.value)
        return False

    # Begin awful boilerplate code to make Bitfields act just like integers. Subclassing isn't an
    # option because ints are immutable, and that throws out the whole point of using __getitem__
    # and __setitem__.

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
