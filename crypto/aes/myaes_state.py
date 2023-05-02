from myaes_gfbyte import *

import copy

class State:

    MIXCOLUMNS_INT = int("02010103030201010103020101010302", 16)
    MIXCOLUMNS_BYTES = b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02'
    INV_MIXCOLUMNS_INT = int("0e090d0b0b0e090d0d0b0e09090d0b0e", 16)
    INV_MIXCOLUMNS_BYTES = b'\x0e\t\r\x0b\x0b\x0e\t\r\r\x0b\x0e\t\t\r\x0b\x0e'

    # Initialize with 'bytes' object containing exactly 16 bytes
    def __init__(self, theBytes):
        # print('in KeySchWord init type list = {}'.format(type(bList[0])))
        assert isinstance(theBytes, bytes)
        self.matrix = []
        for col in range(4):  
            column = []
            for row in range(4):  
                # print('type of theBytes is {}; its [0]th member is {}'.format(theBytes, theBytes[0]))
                column.append(GfByte(theBytes[4*col + row]))
                
            self.matrix.append(column)

        # self.mixColMatrix = []
        # rotatingColumn = [2,1,1,3]
        # for col in range(4): 
        #     mixColColumn = []
        #     for row in range(4):
        #         mixColColumn.append(GfByte(rotatingColumn[(row + col)%4]))
        #     self.mixColMatrix.append(mixColColumn)


    def __str__(self):
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        result = []
        for col in range(4):
            for row in range(4):
                result.append(hex[self.matrix[col][row].b//16])
                result.append(hex[self.matrix[col][row].b%16])
        return "".join(result)


    def __repr__(self):
        return self.__str__()


    def pretty_print(self):
        lines = []
        for row in range(4):
            line = []
            for col in range(4):
                line.append('{}'.format(self.matrix[col][row]))
            lines.append(' '.join(line))
        return '\n'.join(lines)

    def getBytes(self):
        result_hex = self.__str__()
        result_int = int(result_hex, 16)
        return result_int.to_bytes(16, 'big', signed=False)

    def addRoundKey(self, keyBytes):
        for col in range(4):
            for row in range(4):
                keyByte = GfByte(keyBytes[4*col + row])
                self.matrix[col][row] = self.matrix[col][row] + keyByte


    def SubBytes(self):
        for col in range(4):
            for row in range(4):
                self.matrix[col][row] = self.matrix[col][row].sbox()

    def InvSubBytes(self):
        for col in range(4):
            for row in range(4):
                self.matrix[col][row] = self.matrix[col][row].inv_sbox()

    def ShiftRows(self): 
        temp = []
        for col in range(4): 
            temp.append(copy.copy(self.matrix[col]))
        for col in range(4): 
            for row in range(4):
                self.matrix[col][row] = temp[(col+row)%4][row]

    def InvShiftRows(self): 
        temp = []
        for col in range(4): 
            temp.append(copy.copy(self.matrix[col]))
        for col in range(4): 
            for row in range(4):
                self.matrix[col][row] = temp[(col-row)%4][row]


    def MixColumns(self, mixColMatrix): 
        temp = []
        for col in range(4): 
            temp.append(copy.copy(self.matrix[col]))
        for col in range(4): 
            for row in range(4):
                self.matrix[col][row] = GfByte(0)
                for t in range(4):
                    # if col == 0 and row == 0:
                    #     print('({}) Adding to {} the product {}*{}'.format(t, self.matrix[col][row], mixColMatrix.matrix[t][row], temp[col][t]))
                    self.matrix[col][row] = self.matrix[col][row] + mixColMatrix.matrix[t][row] * temp[col][t]

