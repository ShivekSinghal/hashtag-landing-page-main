
from Crypto.Cipher import AES
from hashlib import md5
import hashlib
import binascii

def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length]) * length
    return data

def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText.encode('utf-8'))
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode('utf-8'))
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText)
    return binascii.hexlify(encryptedText).decode('utf-8')

def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode('utf-8'))
    cipherText = binascii.unhexlify(cipherText)
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    decryptedText = dec_cipher.decrypt(cipherText)
    return decryptedText.rstrip(b'\x00').decode('utf-8')
