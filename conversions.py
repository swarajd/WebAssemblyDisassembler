def leb128_to_int(num, signed=False):
    """ 
        Parameters:
        num      byte string encoded in LEB 128 signed
        signed   boolean, true if decoding signed integers, false otherwise

        Return value
        integer variable represented the encoded byte string

        Example:
        >>> leb128_to_int(b'\xe4\x00', true)
        100

        Source: https://github.com/bright-tools/varints
    """
    return_value = None
    if (isinstance(num, (str, bytes))):
        index = 0
        while index < len(num):
            partial = num[index:]
            value = None
            bytes_used = 0
            cont = True

            while cont:
                val = partial[bytes_used]
                if((val & 0x80) == 0):
                    cont = False
                val = val & 0x7F

                if value is None:
                    value = 0

                value = value | (val << (7 * bytes_used))

                bytes_used = bytes_used + 1

            if signed and val & 0x40:
                value |= (-1 << (7 * bytes_used))

            index = index + bytes_used
            if return_value is None:
                return_value = value
            else:
                if isinstance(return_value, int):
                    return_value = [return_value]
                return_value.append(value)
    return return_value

