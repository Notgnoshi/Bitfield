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
        return hash(self.value)

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value.__eq__(other)
        elif isinstance(other, Bitfield):
            return self.value.__eq__(other.value)
        return False

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__(self.value.__add__(other))
        elif isinstance(other, Bitfield):
            return self.__class__(self.value.__add__(other.value))
        else:
            raise TypeError(f'Bitfield unsupported operand type(s) for +: Bitfield and {type(other)}')

    def __radd__(self, other):
        return self.__add__(other)

    # def __sub__(self, other):
    #     return self.value.__sub__(other)
    #
    # def __mul__(self, other):
    #     return self.value.__mul__(other)
    #
    # def __matmul__(self, other):
    #     return self.value.__matmul__(other)
    #
    # def __truediv__(self, other):
    #     return self.value.__truediv__(other)
    #
    # def __floordiv__(self, other):
    #     return self.value.__floordiv__(other)
    #
    # def __mod__(self, other):
    #     return self.value.__mod__(other)
    #
    # def __divmod__(self, other):
    #     return self.value.__divmod__(other)
    #
    # def __pow__(self, other, modulo=None):
    #     return self.value.__pow__(other, modulo)
    #
    # def __lshift__(self, other):
    #     return self.value.__lshift__(other)
    #
    # def __rshift__(self, other):
    #     return self.value.__rshift__(other)
    #
    # def __and__(self, other):
    #     return self.value.__and__(other)
    #
    # def __xor__(self, other):
    #     return self.value.__xor__(other)
    #
    # def __or__(self, other):
    #     return self.value.__or__(other)

    # def __radd__(self, other):
    #     return self.value.__radd__(other)
    #
    # def __rsub__(self, other):
    #     return self.value.__rsub__(other)
    #
    # def __rmul__(self, other):
    #     return self.value.__rmul__(other)
    #
    # def __rmatmul__(self, other):
    #     return self.value.__rmatmul__(other)
    #
    # def __rtruediv__(self, other):
    #     return self.value.__rtruediv__(other)
    #
    # def __rfloordiv__(self, other):
    #     return self.value.__rfloordiv__(other)
    #
    # def __rmod__(self, other):
    #     return self.value.__rmod__(other)
    #
    # def __rdivmod__(self, other):
    #     return self.value.__rdivmod__(other)
    #
    # def __rlshift__(self, other):
    #     return self.value.__rlshift__(other)
    #
    # def __rrshift__(self, other):
    #     return self.value.__rrshift__(other)
    #
    # def __rand__(self, other):
    #     return self.value.__rand__(other)
    #
    # def __rxor__(self, other):
    #     return self.value.__rxor__(other)
    #
    # def __ror__(self, other):
    #     return self.value.__ror__(other)
    #
    # def __iadd__(self, other):
    #     return self.value.__iadd__(other)
    #
    # def __isub__(self, other):
    #     return self.value.__isub__(other)
    #
    # def __imul__(self, other):
    #     return self.value.__imul__(other)
    #
    # def __imatmul__(self, other):
    #     return self.value.__imatmul__(other)
    #
    # def __itruediv__(self, other):
    #     return self.value.__itruediv__(other)
    #
    # def __ifloordiv__(self, other):
    #     return self.value.__ifloordiv__(other)
    #
    # def __imod__(self, other):
    #     return self.value.__imod__(other)
    #
    # def __ipow__(self, other, modulo=None):
    #     return self.value.__ipow__(other, modulo)
    #
    # def __ilshift__(self, other):
    #     return self.value.__ilshift__(other)
    #
    # def __irshift__(self, other):
    #     return self.value.__irshift__(other)
    #
    # def __iand__(self, other):
    #     return self.value.__iand__(other)
    #
    # def __ixor__(self, other):
    #     return self.value.__ixor__(other)
    #
    # def __ior__(self, other):
    #     return self.value.__ior__(other)
