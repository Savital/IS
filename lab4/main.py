import sys
import rsa

if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    print(inputfile)
    print(outputfile)
    # p = int(input("Enter a prime number (17, 19, 23, etc): "))
    # q = int(input("Enter another prime number (Not one you entered above): "))
    p, q = rsa.generate_primes(1000, 10000)
    print('p = ', p, ' q = ', q)
    print('n = p*q =', p*q)
    print("Generating public/private keys. Please, wait.")
    public, private = rsa.generate_keypair(p, q)
    print("Your public key is ", public ," and your private key is ", private)

    rsa.encrypt_and_write(inputfile=inputfile, outputfile=outputfile, key=public)
    rsa.decrypt_and_write(inputfile=outputfile, outputfile='decrypt_' + inputfile, key=private)
