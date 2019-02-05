import pyprimes
import random
import sys
import hashlib

CONTENT_LENGTH_BYTE = 32
CONTENT_LENGTH_BIT = 8 * CONTENT_LENGTH_BYTE

KEY_LENGTH_BIT = CONTENT_LENGTH_BIT + 1
KEY_LENGTH_BYTE = CONTENT_LENGTH_BYTE + 1

PUB_KEY_FILE = 'key.pub'
PRIVATE_KEY_FILE = 'key'


def are_relatively_prime(a, b):
    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def get_prime_in_range(start, stop):
    prime = random.randint(start, stop)
    while not pyprimes.isprime(prime):
        prime = random.randint(start, stop)
    return prime


def get_primes_and_n():
    n_min = 1 << (KEY_LENGTH_BIT - 1)
    n_max = (1 << KEY_LENGTH_BIT) - 1

    prime_min = 1 << (KEY_LENGTH_BIT // 2 - 1)
    prime_max = 1 << (KEY_LENGTH_BIT // 2 + 1)
    while True:
        p, q = get_prime_in_range(prime_min, prime_max), get_prime_in_range(prime_min, prime_max)
        if n_min <= p * q <= n_max:
            return p, q, p * q


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modular_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def generate_keys():
    p, q, n = get_primes_and_n()

    stop = (p - 1) * (q - 1)
    e = 3
    for e in range(3, stop, 2):
        if are_relatively_prime(e, stop):
            break

    d = modular_inverse(e, stop)
    return (n, e), (n, d)


def encode_or_decode(val, key):
    return pow(val, key[1], key[0])


def write_keys():
    pub, private = generate_keys()
    with open(PUB_KEY_FILE, 'w') as f:
        f.write(str(pub[0]))
        f.write('\t')
        f.write(str(pub[1]))
    with open(PRIVATE_KEY_FILE, 'w') as f:
        f.write(str(private[0]))
        f.write('\t')
        f.write(str(private[1]))


def read_keys():
    with open(PUB_KEY_FILE, 'r') as f:
        pub = [int(el) for el in f.read().split('\t')]
    with open(PRIVATE_KEY_FILE, 'r') as f:
        private = [int(el) for el in f.read().split('\t')]
    return pub, private


def encode_file(filename, out_filename, key):
    with open(filename, 'rb') as f_in, open(out_filename, 'wb') as f_out:
        block = f_in.read(CONTENT_LENGTH_BYTE)
        while block != b'':
            value = int.from_bytes(block, byteorder='little')
            enc = encode_or_decode(value, key)
            enc_block = enc.to_bytes(KEY_LENGTH_BYTE, byteorder='little')
            f_out.write(enc_block)
            block = f_in.read(CONTENT_LENGTH_BYTE)


def decode_file(filename, out_filename, key):
    with open(filename, 'rb') as f_in, open(out_filename, 'wb') as f_out:
        block = f_in.read(KEY_LENGTH_BYTE)
        while block != b'':
            value = int.from_bytes(block, byteorder='little')
            dec = encode_or_decode(value, key)
            dec_block = dec.to_bytes(CONTENT_LENGTH_BYTE, byteorder='little')
            f_out.write(dec_block)
            block = f_in.read(KEY_LENGTH_BYTE)


def sign_file(filename, out_filename, key):
    m = hashlib.sha3_256()
    with open(filename, 'rb') as f_in:
        data = f_in.read()
    m.update(data)
    h = m.digest()
    val = int.from_bytes(h, byteorder='little')
    signature = encode_or_decode(val, key)

    with open(out_filename, 'wb') as f_out:
        f_out.write(signature.to_bytes(KEY_LENGTH_BYTE, byteorder='little'))


def validate_file(filename, signature, key):
    m = hashlib.sha3_256()
    with open(filename, 'rb') as f_in:
        data = f_in.read()
        m.update(data)
    h = m.digest()
    with open(signature, 'rb') as f_in:
        prev_h = f_in.read()

    val = int.from_bytes(prev_h, byteorder='little')
    dec = encode_or_decode(val, key)

    if dec.to_bytes(CONTENT_LENGTH_BYTE, byteorder='little') == h:
        print('SUCCESS')
    else:
        print('FAILURE')


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'keys':
            write_keys()

    elif len(sys.argv) > 3:
        pub, private = read_keys()

        filename = sys.argv[2]
        out_filename = sys.argv[3]
        if sys.argv[1] == 'encode':
            encode_file(filename, out_filename, pub)
        elif sys.argv[1] == 'decode':
            decode_file(filename, out_filename, private)

        elif sys.argv[1] == 'sign':
            sign_file(filename, out_filename, pub)
        elif sys.argv[1] == 'validate':
            validate_file(filename, out_filename, private)

    else:
        print(
            'USAGE:\n\tkeys - generate public and private keys'
            '\n\tencode - encode with public key'
            '\n\tdecode - decode with private key'
        )


if __name__ == '__main__':
    main()
