import base64
import binascii
import math
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
    return bin(int(hexData, scale))[2:]


def bin2hex(binData):
    """return the hex form of an bin string.
        >>> [bin2hex('1111')]
        ['f']
        >>> [bin2hex('11111111')]
        ['ff']
        >>> [bin2hex('1')]
        ['1']
        """
    if binData == '0' or binData == '1' or len(binData) % 4 != 0:
        return binData
    num_of_bits = len(binData) / 4
    scale = 2  # equals to hexadecimal
    return hex(int(binData, scale))[2:]


def fillupbyte(byte):
    """return the hex form of an bin string.
        >>> fillupbyte('011')
        '00000011'
        >>> fillupbyte('1')
        '00000001'
        >>> fillupbyte('10111')
        '00010111'
        >>> fillupbyte('11100111')
        '11100111'
        >>> fillupbyte('111001111')
        '0000000111001111'
        """

    if len(byte) % 8 == 0:
        return byte
    else:
        if len(byte) < 8:
            padding = 8 - len(byte)
        else:
            padding = len(byte) % 8
            padding = 8 - padding
        for x in range(padding):
            byte = '0' + byte

        return byte


def paddingMultiSix(byte):
    rounded = roundup(len(byte))
    return byte.ljust(rounded, '0')


def roundup(x):
    return int(math.ceil(x / 6)) * 6


def binary2base64NoLibrary(str):
    str_base64 = ''
    for i in range(0, len(str), 6):
        arr = str[i:i + 6].encode('utf-8')
    hex_string = binascii.a2b_hex(str.rstrip('\n'))
    return binascii.b2a_base64(hex_string)


def int2base64(byte):
    """return the hex form of an bin string.
        >>> int2base64(0x61)
        b'YQ=='
        >>> int2base64(0x78)
        b'eA=='
        """
    return base64.b64encode(bytes([byte]), altchars=None)


def bin2base64(bits):
    value = ''
    if len(bits) % 6 != 0:
        raise Exception('Not a multiple of 6 group of bits')
    groups = [bits[i:i + 6] for i in range(0, len(bits), 6)]
    for group in groups:
        decimal = int(group, 2)
        value = value + translation(decimal)
    return value + '=='


def hex_to_64(string):
    hex_string = binascii.a2b_hex(string)
    return binascii.b2a_base64(hex_string)


translate_dict = {
    'A': 0, 'Q': 16, 'g': 32, 'w': 48,
    'B': 1, 'R': 17, 'h': 33, 'x': 49,
    'C': 2, 'S': 18, 'i': 34, 'y': 50,
    'D': 3, 'T': 19, 'j': 35, 'z': 51,
    'E': 4, 'U': 20, 'k': 36, '0': 52,
    'F': 5, 'V': 21, 'l': 37, '1': 53,
    'G': 6, 'W': 22, 'm': 38, '2': 54,
    'H': 7, 'X': 23, 'n': 39, '3': 55,
    'I': 8, 'Y': 24, 'o': 40, '4': 56,
    'J': 9, 'Z': 25, 'p': 41, '5': 57,
    'K': 10, 'a': 26, 'q': 42, '6': 58,
    'L': 11, 'b': 27, 'r': 43, '7': 59,
    'M': 12, 'c': 28, 's': 44, '8': 60,
    'N': 13, 'd': 29, 't': 45, '9': 61,
    'O': 14, 'e': 30, 'u': 46, '+': 62,
    'P': 15, 'f': 31, 'v': 47, '/': 63
}


def hex2base64(hexString):
    bin_data = hex2bin(hexString)
    fill_data = fillupbyte(bin_data)
    padding_data = paddingMultiSix(fill_data)
    result = bin2base64(padding_data)
    return result


def translation(search):
    for key, value in translate_dict.items():
        if value == search:
            return key


if __name__ == "__main__":
    doctest.testmod()
    # print(binary2base64NoLibrary('a'))
    # print(hex_to_64('507974686f6e'))
    # print(bin2hex('010100000111100101110100011010000110111101101110'));
    example = hex2base64('3D')
    print(example)
