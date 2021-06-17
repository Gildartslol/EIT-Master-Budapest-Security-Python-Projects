def encrypt_by_add_mod(text, key):
    result = ''
    for ch in text:
        number = ord(ch)
        encrypted = (number + key) % 256
        result = result + chr(encrypted)
    return result


def encrypt_xor_with_changing_key_by_prev_cipher(text, key, mode):
    result = ''
    for ch in text:
        encrypted = ord(ch) ^ key
        if mode == 'encrypt':
            key = encrypted
        else:
            key = ord(ch)
        result = result + chr(encrypted)
    return result


if __name__ == '__main__':
    print(encrypt_by_add_mod('Hello', 123))
    print(encrypt_by_add_mod(encrypt_by_add_mod('Hello', 123), 133))
    print(encrypt_by_add_mod(encrypt_by_add_mod('Cryptography', 10), 246))
    print(encrypt_xor_with_changing_key_by_prev_cipher('Hello', 123, 'encrypt'))
    print(encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello', 123, 'encrypt'),
                                                 123, 'decrypt'))
    print(encrypt_xor_with_changing_key_by_prev_cipher(
        encrypt_xor_with_changing_key_by_prev_cipher('Cryptography', 10, 'encrypt'), 10, 'decrypt'))
