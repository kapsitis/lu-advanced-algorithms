from myaes_gfbyte import *

class State: 
    # Initialize with 'bytes' object containing exactly 16 bytes
    def __init__(self, theBytes):
        # print('in KeySchWord init type list = {}'.format(type(bList[0])))
        assert isinstance(theBytes, bytes)
        self.matrix = []
        for col in range(4):  
            columnList = []
            for row in range(4):  
                # print('type of theBytes is {}; its [0]th member is {}'.format(theBytes, theBytes[0]))
                columnList.append(GfByte(theBytes[4*col + row]))
            self.matrix.append(columnList)

    def __str__(self):
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        result = []
        for col in range(4):
            for row in range(4):
                result.append(hex[self.matrix[col][row].b//16])
                result.append(hex[self.matrix[col][row].b%16])
        return "".join(result)

    def __repr__(self):
        return self.__str__()


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

    def ShiftRows(self): 
        temp = []
        for col in 
