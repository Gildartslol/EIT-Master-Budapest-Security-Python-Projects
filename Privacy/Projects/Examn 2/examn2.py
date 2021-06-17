import sys
import random
import hashlib
import libnum
import numpy as np


def randomPoint(a, b):
    y = random.randint(-100, 100)
    # Get roots of:  f(x) = x^3 + ax + b - y^2
    roots = np.roots([1, 0, a, b - y ** 2])
    # 3 roots are returned, but ignore potential complex roots
    # At least one will be real
    roots = [val.real for val in roots if val.imag == 0]
    # Choose a random root among those real root(s)
    x = random.choice(roots)
    return [x, y]


password = "abcdef"

G = randomPoint(2, 2)
H = randomPoint(2, 2)

print('Number G is', G)
print('Number H is', H)

print("Password:\t", password)
x = int(hashlib.md5(password.encode()).hexdigest()[:8], 16)
print('hash is', x)
xG = x * np.array(G)
xH = x * np.array(H)

print('xG', xG,)
print('xH', xH,)

v = random.randint(10000, 20000)
vG = v * np.array(G)
vH = v * np.array(H)

print('vG', vG)
print('vH', vH)

concat = xG + xH + vG + vH
print(concat)
suma = concat[0] + concat[1]
# concat = str(xG[0]) + str(xG[1]) + str(xH[0]) + str(xH[1]) + str(vG[0]) + str(vG[1]) + str(vH[0]) + str(vH[1])
print('Sum', str(suma))
concat = str(suma)
h = hashlib.md5()
h.update(concat.encode("utf-8"))
challenge = int(h.hexdigest(), 16)
print('The challenge is', challenge)

response = (v - challenge * x)
print('Peggy Response part is', response)

print('Victor proves')
rG = response * np.array(G)
rH = response * np.array(H)
vGProve = rG + (challenge * np.array(xG))
vHProve = rH + (challenge * np.array(xH))

print('VGProve is', vGProve)
print('VHProve is', vHProve)
