import socket
from . import _network_script as netsc
from ._player import *
from ._core import *

def card2object(card):
    return card.__class__.__name__, card.color.name, card.number
def objects2card(class_name, color_name, number):
    for card in CARD_SET:
        if (card.__class__.__name__ == class_name
        and card.color.name == color_name
        and card.number == number):
            break
    return card

class Server:
    def __init__(self, card_count=7):
        sockobj = socket.socket()
        sockobj.bind(('', 4000))
        sockobj.listen(0)
        print('Waiting for player to join...')
        conn, (host, port) = sockobj.accept()
        self.sockobj = conn
        self.sockobj.send(netsc.objects2data('initialize', card_count))
    def draw(self, count):
        self.sockobj.send(netsc.objects2data('draw', count))
    def remove_from_hand(self, card):
        self.sockobj.send(netsc.objects2data('remove_from_hand', card2object(card)))
    def score(self):
        self.sockobj.send(netsc.objects2data('tally'))
        return netsc.data2objects(self.sockobj.recv(2048))['args']
    def play(self, current_card, game):
        self.sockobj.send(netsc.objects2data('play', card2object(current_card), 'game_mask'))
        while True:
            data = netsc.data2objects(self.sockobj.recv(2048))
            if data['return']:
                data = data['args']
                if data is not None:
                    data = objects2card(*data)
                break
            elif data['name'] == 'print':
                game.display_message(*data['args'])
        return data
    def ask(self, q, t=str, limits=()):
        t = t.__name__
        self.sockobj.send(netsc.objects2data('ask', q, t, limits))
        returnval = netsc.data2objects(self.sockobj.recv(2048))['args']
        if issubclass(t, Card):
            returnval = objects2card(*returnval)
        return returnval
    def end(self):
        self.sockobj.send(netsc.objects2data('end'))
    def doprint(self, *vals):
        self.sockobj.send(netsc.objects2data('doprint', *vals))
    @property
    def hand(self):
        self.sockobj.send(netsc.objects2data('hand'))
        res = []
        ret = netsc.data2objects(self.sockobj.recv(2048))['args']
        for obj in ret:
            res.append(objects2card(*obj))
        return res

class Client:
    class GamePrinter:
        def __init__(self, client):
            self.client = client
        def display_message(self, *vals):
            self.client.sockobj.send(netsc.objects2data('print', *vals))

    def __init__(self, host, port=4000, player_type=RealPlayer):
        self.sockobj = socket.socket()
        self.sockobj.connect((host, port))
        init_call = netsc.data2objects(self.sockobj.recv(2048))
        if not init_call['return'] and init_call['name'] == 'initialize':
            self.player = player_type(*init_call['args'])
            self._running = False
    def listen(self):
        return netsc.data2objects(self.sockobj.recv(2048))
    def listen_function(self):
        value = self.listen()
        if value['name'] == 'end': self.end()
        elif value['name'] == 'draw': self.end(*value['args'])
        elif value['name'] == 'remove_from_hand': self.remove_from_hand(*value['args'])
        elif value['name'] == 'tally': self.score()
        elif value['name'] == 'play': self.play(*value['args'])
        elif value['name'] == 'ask': self.ask(*value['args'])
        elif value['name'] == 'doprint': self.doprint(*value['args'])
        elif value['name'] == 'hand': self.get_hand(*value['args'])
    def end(self):
        self._running = False
        self.player.end()
    def mainloop(self):
        self._running = True
        while self._running:
            self.listen_function()
    def draw(self, count):
        self.player.draw(count)
    def remove_from_hand(self, card):
        card = objects2card(*card)
        self.player.remove_from_hand(card)
    def score(self):
        value = self.player.score()
        self.sockobj.send(netsc.return2data(value))
    def play(self, current_card, game):
        print('Your turn!')
        game = self.GamePrinter(self)
        current_card = objects2card(*current_card)
        returnval = self.player.play(current_card, game)
        if isinstance(returnval, Card):
            returnval = card2object(returnval)
        self.sockobj.send(netsc.return2data(returnval))
        print('Waiting for the other players to complete their turns...')
    def ask(self, q, t='str', limits=()):
        t = eval(t)
        value = self.player.ask(q, t, limits)
        if issubclass(t, Card):
            value = card2object(value)
        self.sockobj.send(netsc.return2data(value))
    def doprint(self, *vals):
        self.player.doprint(*vals)
    def get_hand(self):
        res = []
        for card in self.player.hand:
            res.append(card2object(card))
        self.sockobj.send(netsc.return2data(res))