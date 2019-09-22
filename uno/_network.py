from ._mods import *
from ._card import *

class Network:
    def __init__(self):
        self.sock1 = socket.socket()
        # self.sock2 = socket.socket()
        self._ended = False
    def send_receive(self, cmd):
        self.send(cmd)
        return self.receive()
    def send(self, cmd):
        print('sent', b'\x00' + cmd.encode())
        self.sock1.send(b'\x00' + cmd.encode())
    def set_value(self, *value):
        print(b'\x02'+pickle.dumps(value))
        self.sock1.send(b'\x02'+pickle.dumps(value))
    def receive(self):
        testdata = self.sock1.recv(1)
        while not len(testdata):
            testdata = self.sock1.recv(1)
            time.sleep(1)
        datafinal = self.sock1.recv(2048)
        data = bytes(datafinal)
        print('received', testdata + data)
        if testdata == b'\x01':
            return pickle.loads(data)
    def poll_event(self):
        testdata = self.sock1.recv(1)
        while not len(testdata):
            # print(testdata)
            testdata = self.sock1.recv(1)
            time.sleep(1)
        datafinal = self.sock1.recv(2048)
        data = bytes(datafinal)
        print('poll received', testdata + data)
        if testdata == b'\x00':
            print('poll sent', b'\x01' + pickle.dumps(eval('self.'+data.decode())))
            self.sock1.send(b'\x01' + pickle.dumps(eval('self.'+data.decode())))
        elif testdata == b'\x02':
            data = pickle.loads(data)
            setattr(self, data[0], data[1])
    def poll_events(self, n=math.inf):
        self._ended = False
        i = 0
        while i < n:
            # print(i)
            self.poll_event()
            if self._ended: break
            i += 1
    def poll_events_forever(self):
        _thread.start_new_thread(self.poll_events, ())
class NetworkWrapper(Network):
    def __init__(self, host, player):
        super().__init__()
        self.sock1.connect((host, 4000))
        # self.sock2.connect((host, 4001))
        self.player = player
        # self.other = NetworkPlayer.from_socket(self.sock2)
    @staticmethod
    def from_socket(sock, player):
        self = NetworkWrapper.__new__(NetworkPlayer)
        self.sock1 = sock
        self.player = player
        return self
    def play(self, current_card, game:type(None)):
        class TempGame:
            def display_message(self_, *vals):
                value = self.send_receive('_display_messge(%s)' %
                ','.join(repr(x) for x in vals))
        self.player.play(current_card, TempGame())
class NetworkPlayer(Network):
    # def __init__(self, player_this_side):
    def __init__(self):
        Network.__init__(self)
        self.sock1.bind(('', 4000))
        # self.sock2.bind(('', 4001))
        self.sock1.listen(0)
        self.sock1, addr1 = self.sock1.accept()
        self._game = None
        # self.sock2.listen(0)
        # while True:
        #     sock2, addr2 = self.sock2.accept()
        #     if addr2[0] == addr1[0]: break
        # self.sock2 = sock2
        # self.other = NetworkWrapper.from_socket(self.sock2, player_this_side)
    @staticmethod
    def from_socket(sock):
        self = NetworkPlayer.__new__(NetworkPlayer)
        self.sock1 = sock
        return self
    def __getattr__(self, attr):
        attr = 'player.' + attr
        value = self.send_receive(attr)
        if callable(value):
            def do_call(*args, **kwargs):
                nonlocal attr
                arglist = []
                for arg in args:
                    if isinstance(arg, Card):
                        arglist.append(get_card_name(arg))
                    else:
                        arglist.append(repr(arg))
                argstr = ','.join(arglist)
                kwarglist = []
                for arg in kwargs.items():
                    kwarglist.append('='.join(arg))
                kwargstr = ','.join(kwarglist)
                comma = ',' * bool(argstr and kwargstr)
                return self.send_receive('%s(%s%s%s)' % (attr, argstr, comma, kwargstr))
            return do_call
        else: return value
    def end(self):
        self._ended = True
    def play(self, current_card, game):
        self._game = game
        self.poll_events_forever()
        value = self.send_receive('play(%s, None)' % get_card_name(current_card))
        self.end()
        return value
    def _display_message(self, *vals):
        self._game.display_message(*vals)

__all__ = dir()