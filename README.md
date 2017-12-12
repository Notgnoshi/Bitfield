# Bitfield
A Python bitfield class for easier bit manipulation of integers


## TODO:
* Pass in an optional bitfield width?
    - If width is set, should the width be fixed until increased manually?
* Allow out of range indices in `__getitem__` (return `0b0`) and `__setitem__` (extend the number)
* Sign extension?
* Test more extensively with negative numbers
* Add classes/functions for working with `bytes` and `bytearray`s
