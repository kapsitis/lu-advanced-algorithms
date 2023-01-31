from myaes_gfbyte import *

class KeySchWord: 
    # Initialize with a list of 4 bytes
    def __init__(self, bList):
        # print('in KeySchWord init type list = {}'.format(type(bList[0])))
        assert isinstance(bList[0], int) or isinstance(bList[0], GfByte)

        if isinstance(bList[0], int):
            self.bList = [GfByte(bb) for bb in bList]
        else: 
            self.bList = bList

    # Output a hex string representation of the key - convert all 4 bytes. 
    def __str__(self):
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        result = []
        for byte in self.bList:
            result.append(hex[byte.b//16])
            result.append(hex[byte.b%16])
        return "".join(result)


    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return KeySchWord([self.bList[0] + other.bList[0], self.bList[1] + other.bList[1], self.bList[2] + other.bList[2], self.bList[3] + other.bList[3]])

    # Multiply by a number from left side
    def __rmul__(self, other):
        assert isinstance(other, int) or isinstance(other, GfByte)
        if isinstance(other, int):
            other = GfByte(other)
        return KeySchWord([other*self.bList[i] for i in range(4)])


    def RotWord(self):
        return KeySchWord([self.bList[1], self.bList[2], self.bList[3], self.bList[0]])

    def SubWord(self):
        return KeySchWord([self.bList[0].sbox(), self.bList[1].sbox(), self.bList[2].sbox(), self.bList[3].sbox()])


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            result = True
            for i in range(4):
                result = result and (self.bList[i].b == other.bList[i].b)
            return result
        else:
            return False

    def __hash__(self):
        result = 0
        for i in range(4):
            result = result ^ self.bList[i].__hash__()
        return result

    def __ne__(self, other):
        return not self.__eq__(other)



class KeyScheduler: 

    # Initialize with a list of N byte sequences, 4 bytes each. 
    def __init__(self, listOfBytes, numBits):
        self.numBits = numBits

        # TODO: Rewrite this as self.WList =  [KeySchWord([uu[0], uu[1], uu[2], uu[3]]) for uu in listOfBytes]
        self.WList =  []
        for uu in listOfBytes:
            self.WList.append(KeySchWord([uu[0], uu[1], uu[2], uu[3]]))
        self.rc = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        self.rcon = [KeySchWord([x, 0x00, 0x00, 0x00]) for x in self.rc]



    # R as the number of round keys needed: 11 round keys for AES-128, 13 keys for AES-192, and 15 keys for AES-256
    def getWords(self):
        result = []        
        if self.numBits == 128:
            R = 11
            N = 4
        elif self.numBits == 192: 
            R = 13
            N = 6
        else:
            N = 15
            N = 8
        for i in range(4*R):
            if i < 4: 
                W_i = self.WList[i]
                result.append(W_i)
            elif i >= 4 and i % N == 0:
                W1 = result[-1].RotWord()
                W2 = W1.SubWord()
                W3 = result[i-N] + W2
                W_i = W3 + self.rcon[i//N]
                result.append(W_i)
            elif i >= 4 and N > 6 and i % N == 0:
                # impossible for 128-bit AES
                W_i = result[i-N] + result[-1].SubWord()
                result.append(W_i)
            else:
                W_i = result[i-N] + result[-1]
                result.append(W_i)
        return result
        

    # Returns round key as a sequence of 4 bytes
    def getRoundKey(self, round):
        all_words = self.getWords()
        slice = all_words[4*round: 4*round + 4]
        # round_key = 0x1000000*slice[0] + 0x10000*slice[1] + 0x100*slice[2] + slice[3]
        # return round_key.to_bytes(16, 'big', signed = False)
        round_key_hex = '{}{}{}{}'.format(slice[0], slice[1], slice[2], slice[3])
        round_key_int = int(round_key_hex, 16)
        return round_key_int.to_bytes(16, 'big', signed = False)


    