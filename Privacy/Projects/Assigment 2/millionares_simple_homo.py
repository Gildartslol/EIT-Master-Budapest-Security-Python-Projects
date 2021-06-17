def make_zero_encoding(x, padding=0):
    x = bin(x)[2:].zfill(padding)  # Pad the binary integer
    x = x[::-1]  # Reverse the binary integer so the order stays as per the formula specified in the paper
    encoding = set()  # Initialize an empty set
    for i in range(len(x)):
        if x[i] == '0':
            element = '1' + x[i + 1:]
            element = element[::-1]
            if int(element, 2) == 1:
                encoding.add('1')
            else:
                encoding.add(element)
            if x[i + 1:] == '0' * len(x[i + 1:]):
                break
    return encoding  # Return the set


# Method to get the one encoding of the integer specified with a padding
# params int x, int padding
def make_one_encoding(x, padding=0):
    x = bin(x)[2:].zfill(padding)  # Pad the binary integer
    x = x[::-1]  # Reverse the binary integer so the order stays as per the formula specified in the paper
    encoding = set()  # Initialize an empty set
    for i in range(len(x)):
        if x[i] == '1':
            element = x[i:]
            element = element[::-1]
            if int(element, 2) == 1:
                encoding.add('1')
            else:
                encoding.add(element)
            if x[i + 1:] == '0' * len(x[i + 1:]):
                break
    return encoding  # Return the set


import random
import sys


def cipher(number, p, q):
    ciphertext = ''
    binary = bin(number)
    for i in binary[2:]:
        c = p * q + 2 * r + m
        ciphertext = ciphertext + str(c)
    return ciphertext


def decipher(ciphertext):
    d = (ciphertext % p) % 2


if __name__ == "__main__":
    # Lets suppose alice is 4millions and bob 2 millions
    alice = 4000000
    bob = 2000000

    p = 1001
    m = 1
    q = random.randint(3, 10)
    r = random.randint(3, 10)

    cipherTextAlice = cipher(alice, p, q)
    cipherTextBob = cipher(bob, p, q)
    print(bin(int(cipherTextAlice)))
    print(bin(int(cipherTextBob)))

    zero_encoding_y = make_zero_encoding(int(cipherTextBob))
    one_encoding_x = make_one_encoding(int(cipherTextAlice))
    print(len(zero_encoding_y.intersection(one_encoding_x)))  # if no elements intersected then x > y
