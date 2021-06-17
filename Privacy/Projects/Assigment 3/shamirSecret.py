from binascii import hexlify, unhexlify
from Crypto.Protocol.SecretSharing import Shamir

key_str = "im a hacker"
key_str_bytes = bytearray(key_str.encode())
key_str_bytes = key_str_bytes.ljust(16, bytes('0', 'utf-8'))
print('ORIGINAL KEY ', key_str)
shares = Shamir.split(3, 8, key_str_bytes)
for idx, share in shares:
    print("Index #%d: %s" % (idx, hexlify(share)))

shares_recovered = []
num_samples = 2

for idx, share in shares[0:num_samples]:
    shares_recovered.append((idx, share))

key_recovered = Shamir.combine(shares_recovered)
str_recovered = ''
for i in key_recovered:
    str_recovered = str_recovered + chr(i)

print('RECONSTRUCTED ', str_recovered)
