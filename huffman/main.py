import heapq
import os
import sys
import ast
import bitstring

PADDING = 'padding'


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    result = bytes(b[::-1])
    if len(result) == 0:
        return b'\x00'
    return result


class HeapNode:
    def __init__(self, occurrences, symbol=None, left=None, right=None):
        self.occurrences = occurrences
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.occurrences < other.occurrences

    def build_codes_from_tree(self, current_code, dictionary):
        if self.symbol is not None:
            dictionary[self.symbol] = current_code
        else:
            self.left.build_codes_from_tree(current_code + b'0', dictionary)
            self.right.build_codes_from_tree(current_code + b'1', dictionary)

    def symbol_for_bits(self, bit_array):
        if self.symbol is not None:
            return self.symbol, bit_array
        if len(bit_array) == 0:
            return None, None
        if bit_array[0] is False:
            return self.left.symbol_for_bits(bit_array[1:])
        return self.right.symbol_for_bits(bit_array[1:])


class HuffmanCoder:
    def __init__(self):
        self.heap = []
        self.dict = {}
        self.root = None
        self.codes = {}
        self.padding = 0

    def read_dict(self, dict_filename):
        with open(dict_filename, 'r') as f:
            self.dict = ast.literal_eval(f.read())


    def write_dict(self, dict_filename):
        with open(dict_filename, 'w') as f:
            f.write(str(self.dict))

    def build_dict(self, data_filename):
        with open(data_filename, 'rb') as f:
            byte = f.read(1)
            while byte != b'':
                if byte not in self.dict:
                    self.dict[byte] = 1
                else:
                    self.dict[byte] += 1
                byte = f.read(1)

        size = os.path.getsize(data_filename)

    def build_heap(self):
        for symbol, probability in self.dict.items():
            self.heap.append(HeapNode(probability, symbol))
        heapq.heapify(self.heap)

    def build_tree(self):
        while len(self.heap) != 1:
            node1, node2 = heapq.heappop(self.heap), heapq.heappop(self.heap)
            internal_node = HeapNode(node1.occurrences + node2.occurrences, None, node1, node2)
            heapq.heappush(self.heap, internal_node)
        self.root = heapq.heappop(self.heap)

    def build_codes(self):
        self.root.build_codes_from_tree(b'', self.codes)

    def build_codes_for_file(self, data_filename, dict_filename):
        self.build_dict(data_filename)
        self.write_dict(dict_filename)
        self.build_heap()
        self.build_tree()
        self.build_codes()

    def build_codes_from_dict_file(self, dict_filename):
        self.read_dict(dict_filename)
        self.build_heap()
        self.build_tree()
        self.build_codes()

        with open(PADDING, 'r') as f:
            self.padding = int(f.read())

    def read_block_for_encoding(self, file):
        block = b''
        byte = file.read(1)
        while byte != b'':
            block += self.codes[byte]
            if len(block) % 8 == 0:
                return block, False
            byte = file.read(1)
        return block, True

    def make_padding(self, block):
        self.padding = 8 - len(block) % 8
        block += b'0' * self.padding
        with open(PADDING, 'w') as f:
            f.write(str(self.padding))
        return block

    def encode(self, data_filename, dict_filename, output_filename):
        self.build_codes_for_file(data_filename, dict_filename)
        with open(data_filename, 'rb') as f, open(output_filename, 'wb') as f_out:
            block, eof = self.read_block_for_encoding(f)
            while eof is False:
                byte_str = bitstring_to_bytes(block)
                f_out.write(byte_str)
                block, eof = self.read_block_for_encoding(f)
            if len(block) != 0:
                block = self.make_padding(block)
                byte_str = bitstring_to_bytes(block)
                f_out.write(byte_str)
            else:
                self.padding = 0
                with open(PADDING, 'w') as f:
                    f.write(str(self.padding))

        print('File ', data_filename, ' was successfully encoded in ', output_filename)

    def decode(self, data_filename, dict_filename, output_filename):
        self.build_codes_from_dict_file(dict_filename)
        with open(output_filename, 'wb') as f_out:
            bits = bitstring.Bits(filename=data_filename)
            while bits is not None and len(bits) > self.padding:
                code, bits = self.root.symbol_for_bits(bits)
                if code is not None:
                    f_out.write(code)
        print('File ', data_filename, ' was successfully decoded in ', output_filename)


if __name__ == '__main__':
    if len(sys.argv) > 4:
        data_filename = sys.argv[2]
        dict_filename = sys.argv[3]
        output_filename = sys.argv[4]
        if sys.argv[1] == 'compress':
            HuffmanCoder().encode(data_filename, dict_filename, output_filename)
        elif sys.argv[1] == 'decompress':
            HuffmanCoder().decode(data_filename, dict_filename, output_filename)
