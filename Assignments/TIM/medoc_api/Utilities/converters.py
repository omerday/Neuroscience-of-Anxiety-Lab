def to_u_int_16_ex(array, start_index) -> int:
    if len(array) <= start_index:
        raise IndexError(f'Index out of range {start_index}')
    b = array[start_index]
    copy = list(array[0:start_index])
    copy.append(array[start_index + 1])
    copy.append(b)
    if len(array[start_index + 2:]) != 0:
        copy.append(array[start_index + 2:])

    r = copy[start_index:start_index + 2]
    # if(start_index % 2 == 0 ):
    #     return int.from_bytes(r, byteorder='little')
    # else:
    return int.from_bytes(r, byteorder='little')


def to_int_16(array, start_index):
    if len(array) <= start_index:
        raise IndexError(f'Index out of range {start_index}')

    b = array[start_index]
    copy = list(array[0:start_index])
    copy.append(array[start_index + 1])
    copy.append(b)
    if len(array[start_index + 2:]) != 0:
        copy.append(array[start_index + 2:])

    r = copy[start_index:start_index + 2]
    # if(start_index % 2 == 0 ):
    #     return int.from_bytes(r, byteorder='little')
    # else:
    return int.from_bytes(r, byteorder='little', signed=True)


def to_uint_16(array, start_index):
    if len(array) <= start_index:
        raise IndexError(f'Index out of range {start_index}')

    b = array[start_index]
    copy = list(array[0:start_index])
    copy.append(array[start_index + 1])
    copy.append(b)
    if len(array[start_index + 2:]) != 0:
        copy.append(array[start_index + 2:])

    r = copy[start_index:start_index + 2]
    # if(start_index % 2 == 0 ):
    #     return int.from_bytes(r, byteorder='little')
    # else:
    return int.from_bytes(r, byteorder='little', signed=False)


def to_uint_32(array, start_index):
    if len(array) < start_index + 4:
        raise IndexError(f'Index out of range {start_index}')

    copy = list(array[0:start_index])  # 1 part of list
    reversed = array[start_index: start_index + 4]
    copy.extend(reversed[::-1])
    trail = array[start_index + 4:]
    copy.extend(trail)
    # if len(array[start_index + 2:]) != 0:
    #     copy.append(array[start_index+2:])

    r = copy[start_index:start_index + 4]
    # if(start_index % 2 == 0 ):
    #     return int.from_bytes(r, byteorder='little')
    # else:
    return int.from_bytes(r, byteorder='little', signed=False)


def to_string(array, start_index):
    # if len(array) < start_index + 4:
    #     raise IndexError(f'Index out of range {start_index}')
    length = array[start_index]
    if length > 0:
        a = bytes(array[start_index + 1:start_index + 1 + length])
        return str(a, 'utf-8')
    else:
        return ''


# need test
def get_bytes16(short, border='little'):
    n = short
    return n.to_bytes(2, byteorder=border)


# need test
def get_bytes32(integer):
    n = integer
    return n.to_bytes(4, byteorder='little')


# need test
def set_bit(v, index, x) -> int:
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
    v &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask  # If x was True, set the bit indicated by the mask.
    return v


# need test
def get_bit(v, index) -> bool:
    """Get bit"""
    if v & (1 << index):
        return True
    return False


def read_UInt32(bytes):
    """
        read to var uint32 from bytes array
        :param bytes: array of bytes from which converting
        :return:
    """
