# https://gist.github.com/JonCooperWorks/5314103
import sys, getopt
import random
from array import array
import sympy


'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def bezout(a, b):
    '''An implementation of extended Euclidean algorithm.
    Returns integer x, y and gcd(a, b) for Bezout equation:
        ax + by = gcd(a, b).
    '''
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return (x, y, a)
    
'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse2(a, b):
    x = 0
    lx = 1
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
    if lx < 0:
        lx += ob
    print('lx = ', lx)
    return lx



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

    #Choose an integer e such that e and phi(n) are coprime
    e = sympy.randprime(3, phi)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = sympy.randprime(3, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char),key,n) for char in plaintext]
    #Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)

def main(argv):
    inputfile = ''
    outputfile = ''
    secret_key = ''
    action = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:a:",["ifile=","ofile=","secret_key=","action="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -s <secretkey> -a <action(e-encrypt or d-decrypt)>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -s <secretkey> -a <action(e-encrypt or d-decrypt)>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--sekretckey"):
            secret_key = arg
        elif opt in ("-a", "--action"):
            action = arg
            
    # print("Input file is ", inputfile)
    # print("Output file is ", outputfile)
    # print("Sekret_key ", secret_key)
    # print("action ", action)
    return inputfile, outputfile


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

if __name__ == '__main__':
    inputfile, outputfile = main(sys.argv[1:])
    print(inputfile)
    print(outputfile)
    # p = int(input("Enter a prime number (17, 19, 23, etc): "))
    # q = int(input("Enter another prime number (Not one you entered above): "))
    p, q = generate_primes(1000, 10000)
    print('p = ', p, ' q = ', q)
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public ," and your private key is ", private)

    encrypt_and_write(inputfile=inputfile, outputfile=outputfile, key=public)
    decrypt_and_write(inputfile=outputfile, outputfile='decrypt_' + inputfile, key=private)
