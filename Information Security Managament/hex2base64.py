from builtins import print
from base64 import b64encode


def hex2base64(str):
    hex_str = bytearray.fromhex(str).decode()
    data = bytes(hex_str, 'utf-8')
    return b64encode(data)


if __name__ == '__main__':
    base64_string = hex2base64(
        '68 6f 6c 61 0d 0a')
    print(base64_string)
