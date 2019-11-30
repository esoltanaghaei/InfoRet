class VariableByteCompressor:

    @staticmethod
    def compress_to_binary_file(dictionary, file='var_index.txt'):
        f = open(file, "wb")
        # positional indexing {t_id: {doc_id: [pos]}}
        sorted_dictionary = sorted(dictionary)
        f.write(int(len(sorted_dictionary)).to_bytes(4, 'little') + b'\n')
        for t_id in sorted(dictionary):
            posting_dict = dictionary[t_id]
            doc_id_list = sorted(posting_dict)
            variable_byte = VariableByteCompressor.__compress_posting_list(doc_id_list)
            VariableByteCompressor.__write_variable_byte(f, variable_byte)
            for doc_id in doc_id_list:
                variable_byte = VariableByteCompressor.__compress_posting_list(posting_dict[doc_id])
                VariableByteCompressor.__write_variable_byte(f, variable_byte)

    @staticmethod
    def __write_variable_byte(f, variable_byte):
        for i in range(0, len(variable_byte), 8):
            f.write(int(variable_byte[i:i + 8], 2)
                    .to_bytes(1, 'little'))
        f.write(b'\n')

    @staticmethod
    def __compress_posting_list(posting_list):
        vbcode = ''
        if not len(posting_list):
            return vbcode
        vbcode += VariableByteCompressor.__convert_int_to_vbcode(posting_list[0])
        for i in range(1, len(posting_list)):
            vbcode += VariableByteCompressor \
                .__convert_int_to_vbcode(posting_list[i] - posting_list[i - 1])
        return vbcode

    @staticmethod
    def __convert_int_to_vbcode(num):
        binary_str = format(num, 'b')
        end_ptr = len(binary_str)
        vbcode = ''
        continuation_bit = '1'
        while end_ptr > 0:
            start_ptr = max(0, end_ptr - 7)
            vbcode = VariableByteCompressor \
                         .__fill_vb_8bits(binary_str[start_ptr:end_ptr], continuation_bit) \
                     + vbcode
            continuation_bit = '0'
            end_ptr = start_ptr
        return vbcode

    @staticmethod
    def __fill_vb_8bits(binary_str, continuation_bit):
        if len(binary_str) > 7:
            raise Exception('wrong input argument!')
        return str(continuation_bit) + '0' * (7 - len(binary_str)) + binary_str


class VariableByteDecompressor:

    @staticmethod
    def decompress_from_binary_file(file='var_index.txt'):
        f = open(file, "rb")
        dictionary = {}
        tid_num = int(format(int.from_bytes(f.readline().strip(b'\n'), 'little')))
        for i in range(tid_num):
            tid_dict = {}
            doc_list = VariableByteDecompressor.read_posting_list(f)
            for doc_id in doc_list:
                posting_list = VariableByteDecompressor.read_posting_list(f)
                tid_dict[doc_id] = posting_list
            dictionary[i] = tid_dict
        return dictionary

    @staticmethod
    def read_posting_list(f):
        line = f.readline().strip(b'\n')
        variable_byte = ''
        for byte in line:
            variable_byte += format(byte, '08b')
        return VariableByteDecompressor.__decompress_posting_list(variable_byte)

    @staticmethod
    def __decompress_posting_list(vbcode):
        vbcode = [vbcode[i:i + 8] for i in range(0, len(vbcode), 8)]
        postings_list = []
        int_vbcode_list = []
        start_iterator = 0
        while start_iterator < len(vbcode):
            end_iterator = start_iterator + 1
            while vbcode[end_iterator - 1][0] == '0':
                end_iterator += 1
            int_vbcode_list.append(VariableByteDecompressor.
                                   __convert_vbcode_to_int(vbcode[start_iterator:end_iterator]))
            start_iterator = end_iterator
        prev_num = 0
        for gap in int_vbcode_list:
            next_num = prev_num + gap
            postings_list.append(next_num)
            prev_num = next_num
        return postings_list

    @staticmethod
    def __convert_vbcode_to_int(vbcode):
        for i in range(len(vbcode)):
            vbcode[i] = vbcode[i][1:]
        binary_str = ''.join(vbcode)
        return int(binary_str, 2)

# dic = {0:
#            {1: [824, 829, 215607],
#             2: [824, 829, 215607]},
#        1:
#            {1: [824, 829, 215607],
#             2: [824, 829, 215607]},
#        }
# VariableByteCompressor().compress_to_binary_file(dic)
# print(VariableByteDecompressor.decompress_from_binary_file())
#
# f = open("test_1", "wb")
# for i in range(2):
#     bits = "1011000010110000"
#     VariableByteCompressor.__wr
#     VariableByteCompressor.__write_variable_byte(f, bits)
#     # f.writelines()
# # for i in range(1000*1000):
# #     f.write(i)
# #     f.write('\n')
# f = open("test_1", "rb")
# l = f.readline()
# print(l)
# g = l.strip(b'\n')
# print(g.split(b' '))
# for i in g:
#     print("{0:b}".format(i))
#     print(i.to_bytes(1, 'little'))
    # print(format(int.from_bytes(i, 'little'), 'b'))

# print(format(int.from_bytes(g[0], 'little'), 'b'))
# print(format(int.from_bytes(l, 'little'), 'b'))
#
#
# f = open("test_2", "w")
# for i in range(1000):
#     bits = "10111111111111111011110"
#     f.write(bits)