import doctest
def encrypt_with_mul(text, key):
    # First character of the text is xored directly with the key and stored on first_ecnrypted
    # After that, key is multipled by 2 and xored with the next character, then modulos 256
    result = ''
    first = ord(text[0])
    first_encrypted = (first ^ key)
    result = result + chr(first_encrypted)
    key = key * 2
    # We skip the first character
    for ch in text[1:]:
        ch_numeric = ord(ch)
        encrypted = ch_numeric ^ (key % 256)
        key = key * 2
        result = result + chr(encrypted)
    return result


def encrypt_with_mul2(text, key, mode):
    # There is no need to do nothing special to reverse the algorithm, it is working correctly when decrypting
    # an encrypted message. We left the mode parameter just for testing purposes. We check now if key is 1 or 0 to use
    # the last raw character as key.
    result = ''
    first = ord(text[0])
    first_encrypted = (first ^ key)
    result = result + chr(first_encrypted)
    key = key * 2
    # We skip the first character
    for i in range(1, len(text)):
        ch_numeric = ord(text[i])
        new_key = key % 256
        # if 1 or 0 we get last byte character, else key calculated modulus 256
        if new_key == 0 | new_key == 1:
            new_key = text[i - 1]
        encrypted = ch_numeric ^ new_key
        key = key * 2
        result = result + chr(encrypted)
    return result


def swap_every_second_bit(number):
    # swapping every second bit. First we check if the format is on 0bxxxxx, if so we transform it to the decimal
    # number and proceed an apply a transformation with binary function
    check = str(number)[0:1]
    if check == '0b':
        number = int(str(number), 2)
    bits = str(Binary(number))
    bits_arr = list(bits[1:])
    arr = [0, 2, 4, 6]
    for a in arr:
        aux = bits_arr[a + 1]
        bits_arr[a + 1] = bits_arr[a]
        bits_arr[a] = aux
    return int("".join(bits_arr), 2)


def Binary(n):
    binary = ""
    i = 0
    while n > 0 and i <= 8:
        s1 = str(int(n % 2))
        binary = binary + s1
        n /= 2
        i = i + 1
        d = binary[::-1]
    return d


from collections import Counter


def break_scheme2(text):
    all_freq = {}
    arr = list(text)
    z = Counter(arr)
    print(z)
    ch = z.most_common()[0][0]
    #key = ord(ch) ^ ord('e')
    #print(key)
    result = ''
    for key in z.keys():
        for a in text:
            result = result + chr(ord(a) ^ ord(key))
        print(result,'\n')
        result = ''

    return result


if __name__ == '__main__':
    #doctest._test()
    print(encrypt_with_mul('Hello', 227))
    print(encrypt_with_mul(encrypt_with_mul('Hello', 123), 123))
    print(encrypt_with_mul(encrypt_with_mul('Cryptography', 10), 10))

    print(encrypt_with_mul2('Hello', 34, 'encrypt'))
    print(encrypt_with_mul2('Hello2', 131, 'encrypt'))
    print(encrypt_with_mul2(encrypt_with_mul2('Hello', 123, 'encrypt'), 123, 'decrypt'))
    print(encrypt_with_mul2(encrypt_with_mul2('Cryptography', 10, 'encrypt'), 10, 'decrypt'))

    print(swap_every_second_bit(1))
    print(swap_every_second_bit(2))
    print(swap_every_second_bit(4))
    print(swap_every_second_bit(16))
    print(bin(swap_every_second_bit(0b1010)))
    print(bin(swap_every_second_bit(0b01010110)))

    print(break_scheme2('&ú+Ñ$óªd°N!|õù¬ä¼ª¡N/uù¸¡R©uù³òÝ'))
