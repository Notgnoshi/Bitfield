from bitfield import Bitfield


def chunk_file(file_obj, bitfield_size):
    """
        Chunk a binary file into Bitfields of the given size.
    """
    # TODO: read the file in chunks
    data = file_obj.read()
    data = Bitfield(int.from_bytes(data, 'little'))
    while data:
        chunk = data[:bitfield_size]
        chunk.width = bitfield_size
        yield chunk
        data >>= bitfield_size
