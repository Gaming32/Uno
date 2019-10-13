import struct, numbers

NO_STATE        = 0b000000
IN_CALL         = 0b000001
IN_RETURN       = 0b000010
IN_CALL_START   = 0b000100
IN_ARG_START    = 0b001000
IN_LENGTH_IDENT = 0b010000
IN_VALUE        = 0b100000

NULL_TYPE   = 0b00000
INT_TYPE    = 0b00001
STRING_TYPE = 0b00010
BINARY_TYPE = 0b00100
FLOAT_TYPE  = 0b01000
TUPLE_TYPE  = 0b10000

INCOMPLETE_DATA = 0b00
CALL_DATA       = 0b01
RETURN_DATA     = 0b10

def _tuple2data(seq):
    data = objects2data('tuple_func', *seq)
    return data
def _data2tuple(data):
    return tuple(data2objects(data)['args'])

class DataToObjects:
    def __init__(self, string):
        self.reset(string)
    def reset(self, string):
        self.string = string
        self.state = NO_STATE
        self.type = NO_STATE
        self.data_type = NO_STATE
        self.cur = 0x00
        self.i = 0
        self.length = 0
        self.data = {}
    def tokenize(self):
        while self.i < len(self.string):
            if (not self.state & IN_CALL and not self.state & IN_RETURN) and self.string[self.i] == 0x00:
                self.state |= IN_CALL
                self.state |= IN_CALL_START
                self.state |= IN_VALUE
                self.state |= IN_LENGTH_IDENT
                self.type = STRING_TYPE
                self.length = 0
                self.i += 1
            elif (not self.state & IN_RETURN and not self.state & IN_CALL) and self.string[self.i] == 0x02:
                self.state |= IN_RETURN
                self.i += 1
                self.type = self.string[self.i]
                self.state |= IN_LENGTH_IDENT
                self.i += 1
            elif self.state & IN_CALL and self.string[self.i] == 0xff:
                self.state ^= IN_CALL
                self.data_type = CALL_DATA
                self.i += 1
            elif self.state & IN_RETURN and self.string[self.i] == 0xff:
                self.state ^= IN_RETURN
                self.data_type = RETURN_DATA
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
                    elif self.type == BINARY_TYPE:
                        self.data[self.cur] = value
                    elif self.type == INT_TYPE:
                        self.data[self.cur] = int.from_bytes(value, 'big')
                    elif self.type == FLOAT_TYPE:
                        self.data[self.cur] = struct.unpack('>f', value)[0]
                    elif self.type == TUPLE_TYPE:
                        self.data[self.cur] = _data2tuple(value)
                    elif self.type == NULL_TYPE:
                        self.data[self.cur] = None
                    self.i += self.data[0xff]
                    self.length = 0
                    self.type = NO_STATE
                    self.state ^= IN_VALUE
                    self.cur += 1
        return self.data, self.data_type
def data2objects(data):
    value, type = DataToObjects(data).tokenize()
    value.pop(0xff)
    if type == CALL_DATA:
        name = value.pop(0x00)
        res = list(value.values())
        return_ = False
    elif type == RETURN_DATA:
        name = None
        res = value.pop(0x00)
        return_ = True
    return {'name': name, 'args': res, 'return': return_}

def _object2data(obj):
    data = b''
    if isinstance(obj, numbers.Number):
        if int(obj) == obj:
            obj = int(obj)
    if isinstance(obj, str):
        data += bytes((STRING_TYPE,))
        data += len(obj).to_bytes(2, 'big')
        data += obj.encode()
    elif isinstance(obj, bytes):
        data += bytes((BINARY_TYPE,))
        data += len(obj).to_bytes(2, 'big')
        data += obj
    elif isinstance(obj, int):
        data += bytes((INT_TYPE,))
        leng = obj.bit_length() // 8 + 1
        data += leng.to_bytes(2, 'big')
        data += obj.to_bytes(leng, 'big')
    elif isinstance(obj, numbers.Number):
        data += bytes((FLOAT_TYPE,))
        data += b'\x00\x04'
        data += struct.pack('>f', obj)
    elif isinstance(obj, (tuple, list)):
        data += bytes((TUPLE_TYPE,))
        info = _tuple2data(obj)
        data += len(info).to_bytes(2, 'big')
        data += info
    elif obj is None:
        data += bytes((NULL_TYPE,))
        data += b'\x00\x01\x00'
    return data
def objects2data(name, *args):
    data = b''
    data += b'\x00'
    data += len(name).to_bytes(2, 'big')
    data += name.encode()
    for arg in args:
        data += b'\x01'
        data += _object2data(arg)
    data += b'\xff'
    return data
def return2data(return_val):
    data = b''
    data += b'\x02'
    data += _object2data(return_val)
    data += b'\xff'
    return data

if __name__ == '__main__':
    orig = objects2data('Hello!', 5, 'World!', 5.5, None, ['123', 789, 3.141592653, ('abc', 'def')], b'\x00\xff\x80')
    val = data2objects(orig)
    print(val)
    # orig = return2data("'Hello!', 5, 'World!', 5.5")
    # val = data2objects(orig)
    # print(val)