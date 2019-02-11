import sys

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

    def crypt(self, char, rotor_index):
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

    def crypt_string(self, string):
        result = ""
        for char in string:
            result += self.crypt(char, self.rotor_index)
        return result

    def decrypt_string(self, string):
        result = ""
        for char in string:
            result += self.crypt(char, self.decrypt_index)
        return result


if __name__ == '__main__':
    str = "franklymydearidontgiveadamn"
    print("Source : ", str)
    enigma = Enigma()
    enigmed = enigma.crypt_string(str)
    print("Crypted string: ", enigmed)
    decoded = enigma.decrypt_string(enigmed)
    print("Decrypted string: ", decoded)