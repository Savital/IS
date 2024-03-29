import sys
from base64 import b64encode, b64decode

class base_conv(object):
    def __init__(self):
        self.chars = 'abcdefghijklmnopqrstuvwxyz'
        self.base = len(self.chars)
        self.splitter = "!"
        self.debug = False

    @staticmethod
    def base_alpha_encode(chars, base, binary):
        encoded = ''
        while int(binary) > 0:
            binary, remainder = divmod(binary, base)
            encoded = chars[remainder] + encoded
        return encoded

    @staticmethod
    def base_alpha_decode(chars, base, charset):
        i = 1
        res = 0
        for char in charset:
            res += chars.index(char) * i
            i *= base
        return chr(res)

    def to_base(self, string):
        res = ''
        for char in string:
            res += self.base_alpha_encode(self.chars, self.base, ord(char)) + self.splitter
        return res

    def from_base(self, enc):
        res = ''
        char_list = enc.split(self.splitter)
        char_list.pop()
        for word in char_list:
            res += self.base_alpha_decode(self.chars, self.base, word[::-1])
        return res


class Enigma(object):
    rotorI =    'ekmflgdqvzntowyhxuspaibrcj'
    rotorII =   'ajdksiruxblhwtmcqgznpyfvoe'
    rotorIII =  'bdfhjlcprtxvznyeiwgakmusqo'
    rotorIV =   'esovpzjayquirhxlnftgkdcmwb'
    rotorV =    'vzbrgityupsdnhlxawmjqofeck'
    rotorVI =   'jpgvoumfyqbenhzrdkasxlictw'
    rotorVII =  'nzjhgrcxmyswboufaivlpekqdt'
    rotorVIII = 'fkqhtlxocbjspdzramewniuygv'

    reflectorA =    'ejmzalyxvbwfcrquontspikhgd'
    reflectorB =    'yruhqsldpxngokmiebfzcwvjat'
    reflectorC =    'fvpjiaoyedrzxwgctkuqsbnmhl'

    def __init__(self):
        self.rotor = []
        self.chars = 'abcdefghijklmnopqrstuvwxyz'
        self.rotor.append(self.rotorI)
        self.rotor.append(self.rotorII)
        self.rotor.append(self.rotorIII)
        self.reflector = self.reflectorB

        self.rotor_index = [0, 0, 0]
        self.decrypt_index = [0, 0, 0]

    @staticmethod
    def rotate_index(rotor_index):
        rotor_index[2] += 1

        if rotor_index[2] == 26:
            rotor_index[2] = 0
            rotor_index[1] += 1

            if rotor_index[1] == 26:
                rotor_index[1] = 0
                rotor_index[0] += 1

                if rotor_index[0] == 26:
                    rotor_index[0] = 0

    def crypt(self, char, splitter, rotor_index):
        if char == splitter:
            return splitter

        self.rotate_index(rotor_index)
        input, output = [], []

        input.append((self.chars.index(char) + rotor_index[2]) % len(self.chars))
        output.append(self.rotor[0][input[-1]])

        input.append((self.chars.index(output[-1]) + rotor_index[1] - rotor_index[2]) % len(self.chars))
        output.append(self.rotor[1][input[-1]])

        input.append((self.chars.index(output[-1]) + rotor_index[0] - rotor_index[1]) % len(self.chars))
        output.append(self.rotor[2][input[-1]])

        input.append((self.chars.index(output[-1]) - rotor_index[0]) % len(self.chars))
        output.append(self.reflector[input[-1]])

        input.append((self.chars.index(output[-1]) + rotor_index[0]) % len(self.chars))
        current_char = self.chars[input[-1]]
        output.append(self.rotor[2].index(current_char))

        input.append((output[-1] + rotor_index[1] - rotor_index[0]) % len(self.chars))
        current_char = self.chars[input[-1]]
        output.append(self.rotor[1].index(current_char))

        input.append((output[-1] + rotor_index[2] - rotor_index[1]) % len(self.chars))
        current_chat = self.chars[input[-1]]
        output.append(self.rotor[0].index(current_chat))

        input.append((output[-1] - rotor_index[2]) % len(self.chars))
        current_char = self.chars[input[-1]]
        output.append(self.chars.index(current_char))

        return self.chars[output[-1]]

    def crypt_string(self, string, splitter):
        result = ""
        for char in string:
            result += self.crypt(char, splitter, self.rotor_index)
        return result

    def decrypt_string(self, string, splitter):
        result = ""
        for char in string:
            result += self.crypt(char, splitter, self.decrypt_index)
        return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        str = "Frankly, my dear, i don't give a damn"
        print("Source : ", str)
        basis = base_conv()
        enigma = Enigma()
        enc = basis.to_base(str)
        print("Encoded string: ", enc, "\nLength: ", len(enc))
        enigmed = enigma.crypt_string(enc, basis.splitter)
        print("Crypted string: ", enigmed)
        de_enigmed = enigma.decrypt_string(enigmed, basis.splitter)
        print("Decrypted string: ", de_enigmed)
        decode = basis.from_base(de_enigmed)
        print("Decoded: ", decode)
    else:
        filename = sys.argv[1]
        with open(filename, 'rb') as input_file:
            data = input_file.read()
            basis = base_conv()
            enigma = Enigma()
            str = b64encode(data)
            b26 = basis.to_base(str.decode("utf-8"))
            encrypt = enigma.crypt_string(b26, basis.splitter)

            with open(filename + ".encrypted", 'w') as encrypt_file:
                encrypt_file.write(encrypt)
                encrypt_file.close()
            decrypt = enigma.decrypt_string(encrypt, basis.splitter)

            with open(filename + ".decrypted", 'w') as decrypt_file:
                decrypt_file.write(decrypt)
                decrypt_file.close()

            tmp = basis.from_base(decrypt)
            restored = b64decode(tmp)

            with open(filename + ".restored", 'wb') as restore_file:
                restore_file.write(restored)
                restore_file.close()
