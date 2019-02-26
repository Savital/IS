# -*- coding: utf-8 -*-
#from Crypto.Hash import SHA256
#from Crypto.PublicKey import RSA
#from Crypto.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import os

def generateHash(fname="./des_ex.py"):
    h = SHA256.new()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h

def generateKey():
    return RSA.generate(1024, os.urandom)

def getSignature(key, hashValue):
    return pkcs1_15.new(key).sign(h)

def getPubkey(key):
    return key.publickey()

def checkSignature(signature, pubKey, fname="./des_ex.py"):
    h = generateHash(fname=fname)
    try:
        pkcs1_15.new(pubKey).verify(h, signature)
    except:
        return False
    return True

if __name__ == '__main__':
    fname1 ="./des_ex.py"
    fname2 = "./d.py"
    # Генерируете новый ключ (или берете ранее сгенерированный)
    key = generateKey()
    # Получаете хэш файла
    h = generateHash(fname=fname1)
    # послучаем сигнатуру применением шифрования к хэшу
    signature = getSignature(key=key, hashValue=h)
    pubkey = getPubkey(key)

    if checkSignature(signature, pubkey, fname=fname1):
        print('all ok')
    else:
        print('not all ok')
