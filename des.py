# -*- coding：utf-8 -*-

import base64
from Crypto.Cipher import DES


def encrypt(key, text):
    encrypter = DES.new(key.encode(), DES.MODE_ECB)
    length = 8
    count = len(text)
    if count < length:
        add = (length - count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = encrypter.encrypt(text.encode())
    return base64.b64encode(ciphertext)


def decrypt(key, text):
    decrypter = DES.new(key.encode(), DES.MODE_ECB)
    return decrypter.decrypt(text).decode()
