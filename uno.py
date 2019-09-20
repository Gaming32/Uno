import numpy.random as nrandom
import math, random, socket, pickle, time, _thread, string
_ordinal = (lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]))

class Color:
    def __init__(self, name, ansi):
        self.name = name
        self.ansi = '3' + str(ansi)

class Card:
    def __init__(self, long_name, short_name, color, number, weight, points):
        self.long_name = long_name
        self.short_name = short_name
        self.color = color
        self.number = number
        self.weight = weight
        self.points = points
    def played(self, game): pass
    def __str__(self):
        return '\u001b[%sm%s\u001b[37m' % (self.color.ansi, self.short_name)
    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.long_name)

class Player:
    def __init__(self, card_count=7):
        self.hand = []
        self.draw(card_count)
        self.name = 'Player'
    def draw(self, count):
        self.hand.extend(draw(count))
    def remove_from_hand(self, card):
        self.hand.remove(card)
    def score(self):
        score = 0
        for card in self.hand:
            score += card.points
        return score
    def play(self, current_card, game):
        def do():
            while True:
                card = self._play(current_card)
                if self.can_play_card(current_card, card):
                    game.display_message("%s has %i cards" % (self.name, len(self.hand)-1))
                    return card
        if self.can_play(current_card):
            return do()
        else:
            game.display_message("%s couldn't play and had to draw a card" % self.name)
            self.draw(1)
            if self.can_play(current_card):
                return do()
            else:
                game.display_message("%s still couldn't play and had to be skipped" % self.name)
                return None
    def _play(self, current_card):
        for card in self.hand:
            if self.can_play_card(current_card, card):
                return card
        # return self.hand[random.randint(0, len(self.hand)-1)]
    def end(self): pass
    def doprint(self, *vals): pass
    def can_play_card(self, current_card, card):
        return card.number == current_card.number or card.color == current_card.color
    def can_play(self, current_card):
        for card in self.hand:
            if self.can_play_card(current_card, card):
                return True
        else: return False
class RealPlayer(Player):
    def __init__(self, card_count=7):
        super().__init__(card_count)
        self.name = input('What is your name? ')
    def _play(self, current_card):
        self.doprint('Current card:', current_card)
        self.doprint(*self.hand)
        hand_colors = {}
        for card in self.hand:
            if card.color.name not in hand_colors:
                hand_colors[card.color.name] = []
            hand_colors[card.color.name].append(card)
        desired_color = '!'
        while not desired_color or desired_color.lower()[0] not in hand_colors:
            desired_color = input('What color do you want to play? ')
        desired_color = desired_color.lower()[0]
        self.doprint(*hand_colors[desired_color])
        color_numbers = []
        for card in hand_colors[desired_color]:
            color_numbers.append(str(card.number))
        desired_number = ''
        while desired_number not in color_numbers:
            desired_number = input('What number do you want to play? ')
            desired_number = desired_number.strip()
            # try: desired_number = int(desired_number)
            # except ValueError: desired_number = ''
        for card in hand_colors[desired_color]:
            if str(card.number) == desired_number: break
        return card
    def doprint(self, *vals): print(*vals)
class ComputerPlayer(Player):
    NAMES = [
        'Hal',
        'Cortana',
        'Alexa',
        'Bixby',
        'Siri'
    ]
    def __init__(self, card_count=7):
        super().__init__(card_count)
        self.name = random.choice(self.NAMES)
    def _play(self, current_card):
        self.hand.sort(key=(lambda x: x.points), reverse=True)
        for card in self.hand:
            if self.can_play_card(current_card, card):
                return card

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

def draw(count):
    hand = nrandom.choice(CARD_LIST, count, False, WEIGHT_LIST)
    return list(hand)

class Game:
    def __init__(self, players):
        self.players = players
        self.ix = random.randrange(len(self.players))
        self.player = players[self.ix]
        self.card = draw(1)[0]
        self.direction = 1
    def next_player(self):
        self.ix = (self.ix + self.direction) % len(self.players)
        self.player = self.players[self.ix]
    def display_message(self, *vals):
        for player in self.players:
            player.doprint(*vals)
    def game_over(self):
        for player in self.players:
            player.end()
    def begin(self):
        while True:
            card = self.player.play(self.card, self)
            if card is None: self.next_player()
            elif card.number == self.card.number or card.color == self.card.color:
                self.card = card
                if card in self.player.hand:
                    self.player.remove_from_hand(card)
                if not len(self.player.hand): break
                card.played(self)
                self.next_player()
        player_scores = self.players[:]
        player_scores.sort(key=(lambda x: x.score()), reverse=True)
        for (i, player) in enumerate(player_scores[:-1]):
            self.display_message(player.name, 'came in', _ordinal(len(self.players)-i),
            'place with', player.score(), 'points.')
        self.display_message(self.player.name, 'wins!')

class Skip(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'S', color, 's', 2, 20)
    def played(self, game):
        game.ix += 1
        game.display_message("%s has been skipped"
        % game.players[game.ix%len(game.players)].name)
        # % game.players[(game.ix+1)%len(game.players)].name)
class Reverse(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'R', color, 'r', 2, 20)
    def played(self, game):
        if len(game.players) < 3:
            game.ix += 1
            game.display_message("%s has been skipped"
            % game.players[game.ix%len(game.players)].name)
        else:
            game.direction = -game.direction
            game.display_message("%s has reversed the direction" % game.player.name)
class Draw2(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'D2', color, 'd2', 2, 20)
    def played(self, game):
        game.ix += 1
        print("%s forced %s to draw two cards"
        % (game.player.name,
        game.players[game.ix%len(game.players)].name))
        game.players[game.ix%len(game.players)].draw(2)

RED = Color('r', 1)
GREEN = Color('g', 2)
BLUE = Color('b', 4)
YELLOW = Color('y', 3)

CARD_SET = set()

for color in ('red', 'green', 'blue', 'yellow'):
    for number in range(1, 10):
        exec("%s_%i = Card('%s %i', '%i', %s, %i, 2, %i)" %
            (color.upper(), number, color.capitalize(), number, number, color.upper(), number, number))
        CARD_SET.add(eval('%s_%i' % (color.upper(), number)))

    exec("%s_0 = Card('%s 0', '0', %s, 0, 1, 0)" % (color.upper(), color.capitalize(), color.upper()))
    CARD_SET.add(eval('%s_0' % color.upper()))

    exec("%s_SKIP = Skip('%s Skip', %s)" % (color.upper(), color.capitalize(), color.upper()))
    CARD_SET.add(eval('%s_SKIP' % color.upper()))

    exec("%s_REVERSE = Reverse('%s Reverse', %s)" % (color.upper(), color.capitalize(), color.upper()))
    CARD_SET.add(eval('%s_REVERSE' % color.upper()))

    exec("%s_DRAW2 = Draw2('%s Draw 2', %s)" % (color.upper(), color.capitalize(), color.upper()))
    CARD_SET.add(eval('%s_DRAW2' % color.upper()))

def calculate_chance():
    weight_total = 0
    cards = []
    chances = []
    for card in CARD_SET:
        cards.append(card)
        weight_total += card.weight
    for card in CARD_SET:
        chances.append(card.weight / weight_total)
    return cards, chances
CARD_LIST, WEIGHT_LIST = calculate_chance()

def get_card_name(card):
    value = card.long_name.upper().replace(' ', '_')
    prevchar = ''
    newval = ''
    reached__ = False
    for char in value:
        if reached__ and prevchar == '_' and char in string.digits:
            newval = newval[:-1]
        if prevchar == '_' and not reached__:
            reached__ = True
        newval += char
        prevchar = char
    return newval

if __name__ == '__main__':
    def get_number(value):
        try: value = int(value)
        except ValueError:
            print('Please enter a number.')
            return
        else: return value
    def play_game():
        player_list = []

        value = get_number(input('How many ComputerPlayers would you like? '))
        while value is None:
            value = get_number(input('How many ComputerPlayers would you like? '))
        for _ in range(value):
            player_list.append(ComputerPlayer())

        value = get_number(input('How many RealPlayers would you like? '))
        while value is None:
            value = get_number(input('How many RealPlayers would you like? '))
        for _ in range(value):
            player_list.append(RealPlayer())

        value = get_number(input('How many NetworkPlayers would you like? '))
        while value is None:
            value = get_number(input('How many NetworkPlayers would you like? '))
        for _ in range(value):
            player_list.append(NetworkPlayer())

        game = Game(player_list)
        game.begin()
    def join_game():
        player = RealPlayer()
        while True:
            host = input('Hostname/IP of the game to join: ')
            try: wrapper = NetworkWrapper(host, player)
            except socket.error:
                print('Unable to connect to game')
                continue
            else: break
        wrapper.poll_events()
    while True:
        print('Main Menu\t0:Play Game\t1:Join Network Game\t2:Quit')
        value = input('Which option: ')
        value = get_number(value)
        if value == 2:
            print('Goodbye.')
            exit()
        elif value == 0: play_game()
        elif value == 1: join_game()
        elif value is None: continue
        else: print('Invalid option: %s' % value)

    # game = Game([Player(), RealPlayer()])
    # p2 = Player()
    # p2.name = 'Player2'
    # game = Game([Player(), RealPlayer(), p2])
    # game.begin()