import doctest


def hex2bin(hexData):
    """return the binary form of an hex string.
        >>> [hex2bin('f')]
        ['1111']
        >>> [hex2bin('ff')]
        ['11111111']
        >>> [hex2bin('1')]
        ['1']
        """
    if hexData == '0' or hexData == '1':
        return hexData
    num_of_bits = len(hexData) * 4
    scale = 16  # equals to hexadecimal
    # we can zfill the rest here
    # return bin(int(hexData, scale))[2:].zfill(num_of_bits)
    return bin(int(hexData, scale))[2:].zfill(num_of_bits)


def bin2hex(binData):
    """return the hex form of an bin string.
        >>> [bin2hex('1111')]
        ['f']
        >>> [bin2hex('11111111')]
        ['ff']
        >>> [bin2hex('1')]
        ['1']
        """
    if binData == '0' or binData == '1':
        return binData
    num_of_bits = len(binData) / 4
    scale = 2  # equals to hexadecimal
    return hex(int(binData, scale))[2:]


def hex2string(hex_data):
    """return from hext to string
        >>> hex2string('61')
        'a'
        >>> hex2string('776f726c64')
        'world'
        >>> hex2string('68656c6c6f')
        'hello'
           """
    value = ''
    groups = [hex_data[i:i + 2] for i in range(0, len(hex_data), 2)]
    for group in groups:
        decimal = int(group, 16)
        value = value + chr(decimal)
    return value


def string2hex(string_data):
    """Create a function that converts aa string, containing the hexadecimal representation of a text, to the original text string. Inverse of the hex2string function.
        >>> string2hex('a')
        '61'
        >>> string2hex('hello')
        '68656c6c6f'
        >>> string2hex('world')
        '776f726c64'
        >>> string2hex('foo')
        '666f6f'
               """
    value = ''
    for a in string_data:
        decimal = ord(a)
        value = value + hex(decimal)[2:]
    return value


def hex_xor(first, second):
    """Create a function that xor bitwise two string that contains a number hexadecimal representations.
        >>> hex_xor('aabbf11','12345678')
        '189fe969'
        >>> hex_xor('12cc','12cc')
        '0000'
        >>> hex_xor('1234','2345')
        '3171'
        >>> hex_xor('111','248')
        '359'
        >>> hex_xor('8888888','1234567')
        '9abcdef'
               """
    first_bin = hex2bin(first)
    second_bin = hex2bin(second)
    len_first = len(first_bin)
    len_second = len(second_bin)

    if len_first > len_second:
        second_bin = second_bin.rjust(len_first, '0')
    if len_second > len_first:
        first_bin = first_bin.rjust(len_second, '0')

    xor_number = ''
    for a in range(0, len(first_bin)):
        xor_character = int(first_bin[a], 2) ^ int(second_bin[a], 2)
        xor_number = xor_number + str(xor_character)

    return hex(int(xor_number, 2))[2:]


def decryption(hex_text, key):
    decrypted_text = ''
    groups = [hex_text[i:i + 2] for i in range(0, len(hex_text), 2)]
    for group in groups:
        decrypted_text = decrypted_text + hex_xor(group, key)
    return decrypted_text


if __name__ == "__main__":
    doctest.testmod()
    for i in range(0, 256):
        text = decryption('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480', hex(i)[2:])
        print('KEY : ', hex(i)[2:], 'TEXT : ', hex2string(text))
