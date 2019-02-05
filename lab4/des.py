#-*- coding: utf8 -*-
import sys, getopt

#Начальная матрица перестановок для данных
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

#Начальная матрица перестановок для ключа
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

#матрица перестановок для ключа со сдвигом
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

#Матрица для дополнения данных до 48 бит для выполнения xor с ключом
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

#SBOX
S_BOX = [
         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

#перестановка после каждой замены SBox 
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

#Окончательная перестановка данных
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

#Матрица сдвига ключей на каждом раунде
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def string_to_bit_array(text):
    array = list()
    for char in text:
        binval = binvalue(char, 8)
        array.extend([int(x) for x in list(binval)])
    return array

def bit_array_to_string(array):
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in bytes]) for bytes in  nsplit(array,8)]])   
    return res

def binvalue(val, bitsize):
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise Exception("binary value larger than the expected size")
    while len(binval) < bitsize:
        binval = "0"+binval
    return binval

def nsplit(s, n):
    return [s[k:k+n] for k in range(0, len(s), n)]

def getTextFromFile(path):
    return Path(path).read_bytes()

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        return f.read()


def writeToFile(path, text):
    try:
        with open(path, "wb") as file_handler:
            file_handler.write(text)
            return True
    except IOError:
        print("Some error")
        return False

def writeToBinaryFile(path, text):
    try:
        with open(path, "wb") as file_handler:
            file_handler.write(text)
            return True
    except IOError:
        print("Some error")
        return False

ENCRYPT=1
DECRYPT=0

class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()
        
    def run(self, key, text, action=ENCRYPT):
        if len(key) < 8:
            raise Exception("Key Should be 8 bytes long")
        elif len(key) > 8:
            key = key[:8]
        
        self.password = key
        self.text = text
        
        if action==ENCRYPT:
            self.addPadding()
        
        self.generatekeys() # Генерируем все ключи
        text_blocks = nsplit(self.text, 8) #Разюиваем данные в блоки по 8 байтов
        result = list()
        for block in text_blocks:
            block = string_to_bit_array(block) #Convert the block in bit array
            block = self.permut(block,PI) # Применяем начальную перестановку
            l, r = nsplit(block, 32) #l(LEFT), r(RIGHT)
            tmp = None
            for i in range(16):
                r_e = self.expand(r, E) #Дополняем правый блок до размера ключа Ki(48 бит)
                if action == ENCRYPT:
                    tmp = self.xor(self.keys[i], r_e) #При шифровании используем ключи в прямом порядке
                else:
                    tmp = self.xor(self.keys[15-i], r_e) #При дешифровании используем ключи в обратном порядке
                tmp = self.substitute(tmp) # Применяем S-box-ы
                tmp = self.permut(tmp, P) # Еще одна перестановка
                tmp = self.xor(l, tmp)
                l = r
                r = tmp
            result += self.permut(r+l, PI_1) #Последняя перестановка
        final_res = bit_array_to_string(result)
        if action==DECRYPT:
            return self.removePadding(final_res)
        else:
            return final_res
    
    def substitute(self, r_e):#Замена байтов с помощью S-box
        subblocks = nsplit(r_e, 6) #Разбиваем 48-битный блок на 8 6-битных
        result = list()
        for i in range(len(subblocks)):
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2) #первый и последний бит дают строку
            column = int(''.join([str(x) for x in block[1:][:-1]]),2) #4 бита посередине - столбец
            val = S_BOX[i][row][column]
            bin = binvalue(val, 4)
            result += [int(x) for x in bin]
        return result
        
    def permut(self, block, table): #Перемещать данный блок с использованием данной таблицы
        return [block[x-1] for x in table]
    
    def expand(self, block, table): # Делает то же самое что и перестановка
        return [block[x-1] for x in table]
    
    def xor(self, t1, t2):
        return [x^y for x,y in zip(t1,t2)]
    
    def generatekeys(self):
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.permut(key, CP_1) # Применяем начальную перестановку 64 => 56
        l, r = nsplit(key, 28) #Разбиваем на 2 части по 28 бит
        for i in range(16):
            l, r = self.shift(l, r, SHIFT[i]) #Применяем сдвиги
            tmp = l + r #Merge them
            self.keys.append(self.permut(tmp, CP_2)) #Применяем перестановку

    def shift(self, g, d, n):
        return g[n:] + g[:n], d[n:] + d[:n]
    
    def addPadding(self): #Добавление дополнения к данным с использованием спецификации PKCS5.
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)
    
    def removePadding(self, data):#Удаление дополнения
        pad_len = ord(data[-1])
        return data[:-pad_len]
    
    def encrypt(self, key, text):
        return self.run(key, text, ENCRYPT)
    
    def decrypt(self, key, text):
        return self.run(key, text, DECRYPT)
    
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
            if action not in ("e", "d"):
                raise Exception("Action argument must be e or d")
            
    print("Input file is ", inputfile)
    print("Output file is ", outputfile)
    print("Sekret_key ", secret_key)
    print("action ", action)
    return inputfile, outputfile, secret_key, action

# Example to run for encoding: python3 des.py -i input.txt.zip -o cipher.zip -s secret_k -a e
# Example to run for decoding: python3 des.py -o decipher.zip -i cipher.zip -s secret_k -a d
if __name__ == '__main__':
    inputfile, outputfile, secret_key, action = main(sys.argv[1:])
    some_str = bytes_from_file(inputfile)
    decode_str = some_str.decode("latin-1")
    d = des()
    result = None
    if action == "e":
        result = d.encrypt(secret_key, decode_str)
    else:
        result = d.decrypt(secret_key, decode_str)
    encode_result = result.encode("latin-1")
    writeToBinaryFile(outputfile, encode_result)

