import sys, getopt
import random
from array import array
import sympy

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(a, b):
    mult_inv = 3

    while (a * mult_inv) % b != 1:
        mult_inv += 1

    return mult_inv

def generate_keypair(p, q):
    if not (sympy.isprime(p) and sympy.isprime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q

    phi = (p-1) * (q-1)

    e = sympy.randprime(3, phi)

    g = gcd(e, phi)
    while g != 1:
        e = sympy.randprime(3, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        return f.read()

def writeToBinaryFile(path, text):
    try:
        with open(path, "wb") as file_handler:
            file_handler.write(text)
            return True
    except IOError:
        print("Some error")
        return False

def encrypt_and_write(inputfile, outputfile, key):
    some_str = bytes_from_file(inputfile)
    decode_str = some_str.decode("latin-1")
    encrypted_msg = encrypt(key, decode_str)
    encrypted_msg_str = ','.join([str(x) for x in encrypted_msg])
    encode_result = encrypted_msg_str.encode('latin-1')
    writeToBinaryFile(outputfile, encode_result)

def decrypt_and_write(inputfile, outputfile, key):
    some_str = bytes_from_file(inputfile)
    decode_str = some_str.decode("latin-1").split(',')
    decode_str = [int(x) for x in decode_str]
    encrypted_msg = decrypt(key, decode_str)
    encode_result = encrypted_msg.encode('latin-1')
    writeToBinaryFile(outputfile, encode_result)

def generate_primes(a, b):
    prime1 = prime2 = 0
    while prime1 == prime2:
        prime1 = sympy.randprime(a, b)
        prime2 = sympy.randprime(a, b)

    if prime2 < prime1:
        return prime2, prime1

    return prime1, prime2