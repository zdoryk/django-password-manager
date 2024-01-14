# utils.py
import base64
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from keyring import get_password


def get_encryption_key():
    return get_password('pm_v1', 'sk')


def encrypt(raw, key):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))


def decrypt(enc, key):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    decrypted_data = cipher.decrypt(enc)
    return decrypted_data.decode('utf-8')
