import doctest
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_aes_ecb(data, key, iv):
    cipher = AES.new(key, AES.MODE_ECB, iv)
    return b64encode(cipher.encrypt(pad(data.encode('utf-8'),
                                        AES.block_size)))


def decrypt_aes_ecb(bytes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(bytes)
    return decrypted


def xor_byte_arrays(arr1, arr2):
    """return a bit permutation in the order given.
       >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([2,3,4,5]))
       bytearray(b'\\x03\\x01\\x07\\x01')
       >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([]))
       bytearray(b'\\x01\\x02\\x03\\x04')
       >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([1,2]))
       bytearray(b'\\x01\\x02\\x02\\x06')
       >>> xor_byte_arrays(bytes([1,2,4,8,16,32,64,128]),bytes([1,1,1,1,1,1,1,1]))
       bytearray(b'\\x00\\x03\\x05\\t\\x11!A\\x81')
        """
    if len(arr2) > len(arr1):
        arr1 = arr1.rjust(len(arr2), bytes([0]))
    elif len(arr1) > len(arr2):
        arr2 = arr2.rjust(len(arr1), bytes([0]))

    result = bytearray(len(arr1))
    for b in range(0, len(arr1)):
        result[b] = arr1[b] ^ arr2[b]
    return result


def decrypt_aes_cbc_with_ecb(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.decrypt(pad(data.encode('utf-8'),
                                   AES.block_size))


def encrypt_aes_cbc_with_ecb(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data.encode('utf-8'),
                                   AES.block_size))


if __name__ == '__main__':
    doctest.testmod()

    key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    print(decrypt_aes_ecb(bytes([215, 221, 59, 138, 96, 94, 155, 69, 52, 90, 212, 108, 49, 65, 138, 179]), key))
    print(decrypt_aes_ecb(bytes([147, 140, 44, 177, 97, 209, 42, 239, 152, 124, 241, 175, 202, 164, 183, 18]), key))

    key2 = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    # print(decrypt_aes_cbc_with_ecb(bytes([255, 18, 67, 115, 172, 117, 242, 233, 246, 69, 81, 156, 52, 154, 123, 171]),
    # key2, iv))
    # print(decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64]),
    #  key2, iv))

    key3 = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    iv3 = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    print(encrypt_aes_cbc_with_ecb(b'hello world 1234', key3, iv3))
    print(encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography'), key3, iv3))
