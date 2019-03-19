# -*- coding: utf-8 -*-
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import os

def generateHash(fname="./a.py"):
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

def checkSignature(signature, pubKey, fname="./a.py"):
    h = generateHash(fname=fname)
    try:
        pkcs1_15.new(pubKey).verify(h, signature)
    except:
        return False
    return True

if __name__ == '__main__':
    fname1 ="./a.py"
    fname2 = "./b.py"
    # Генерируете новый ключ (или берете ранее сгенерированный)
    key = generateKey()
    # Получаете хеш файла
    h = generateHash(fname=fname1)
    # послучаем сигнатуру применением шифрования к хешу
    signature = getSignature(key=key, hashValue=h)
    pubkey = getPubkey(key)

    if checkSignature(signature, pubkey, fname=fname1):
        print('all ok')
    else:
        print('wrong')
