import struct

NO_STATE        = 0b00000
IN_CALL         = 0b00001
IN_CALL_START   = 0b00010
IN_ARG_START    = 0b00100
IN_LENGTH_IDENT = 0b01000
IN_VALUE        = 0b10000

INT_TYPE    = 0b00
STRING_TYPE = 0b01
FLOAT_TYPE  = 0b10

class DataToObjects:
    def __init__(self, string):
        self.reset(string)
    def reset(self, string):
        self.string = string
        self.state = NO_STATE
        self.type = NO_STATE
        self.cur = 0x00
        self.i = 0
        self.length = 0
        self.data = {}
    def tokenize(self):
        while self.i < len(self.string):
            if not self.state & IN_CALL and self.string[self.i] == 0x00:
                self.state |= IN_CALL
                self.state |= IN_CALL_START
                self.state |= IN_VALUE
                self.state |= IN_LENGTH_IDENT
                self.type = STRING_TYPE
                self.length = 0
                self.i += 1
            elif self.state & IN_CALL and self.string[self.i] == 0xff:
                self.state ^= IN_CALL
                self.i += 1
            elif self.state & IN_CALL and not self.state & IN_VALUE and self.string[self.i] == 0x01:
                self.state |= IN_ARG_START
                self.state |= IN_VALUE
            elif self.state & IN_CALL and self.state & IN_ARG_START:
                self.i += 1
                self.type = self.string[self.i]
                self.state ^= IN_ARG_START
                self.state |= IN_LENGTH_IDENT
                self.i += 1
            elif self.state & IN_LENGTH_IDENT:
                if self.length == 0:
                    self.data[self.cur] = bytes((self.string[self.i],))
                    self.length += 1
                    self.i += 1
                elif self.length == 1:
                    self.data[self.cur] += bytes((self.string[self.i],))
                    self.length += 1
                    self.i += 1
                else:
                    self.data[0xff] = int.from_bytes(self.data[self.cur], 'big')
                    self.state ^= IN_LENGTH_IDENT
                    value = self.string[self.i:self.i + self.data[0xff]]
                    if self.type == STRING_TYPE:
                        self.data[self.cur] = value.decode()
                        if self.state & IN_CALL_START:
                            self.state ^= IN_CALL_START
                    elif self.type == INT_TYPE:
                        self.data[self.cur] = int.from_bytes(value, 'big')
                    elif self.type == FLOAT_TYPE:
                        self.data[self.cur] = struct.unpack('>f', value)[0]
                    self.i += self.data[0xff]
                    self.length = 0
                    self.type = NO_STATE
                    self.state ^= IN_VALUE
                    self.cur += 1
        return self.data
def data2objects(data):
    value = DataToObjects(data).tokenize()
    value.pop(0xff)
    name = value.pop(0x00)
    res = []
    for obj in value.values():
        res.append(obj)
    return {'name': name, 'args': res}

def objects2data(name, *args):
    data = b''
    data += b'\x00'
    data += len(name).to_bytes(2, 'big')
    data += name.encode()
    for arg in args:
        data += '\x01'
        if isinstance(arg, str):
            data += len(arg).to_bytes(2, 'big')
            data += arg.encode()
        elif isinstance(arg, int):
            leng = arg.bit_length() // 8 + 1
            data += leng.to_bytes(2, 'big')
            data += arg.to_bytes(leng, 'big')
    data += '\xff'
    return data

if __name__ == '__main__':
    val = data2objects(b'\x00\x00\x06Hello!\x01\x00\x00\x01\x05\x01\x01\x00\x06World!\x01\x02\x00\x04\x40\xb0\x00\x00\xff')
    print(val)