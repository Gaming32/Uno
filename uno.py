import numpy.random as nrandom
import math, random, socket, pickle
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
    def score(self):
        score = 0
        for card in self.hand:
            score += card.points
        return score
    def play(self, current_card):
        def do():
            while True:
                card = self._play(current_card)
                if self.can_play_card(current_card, card):
                    print("%s has %i cards" % (self.name, len(self.hand)-1))
                    return card
        if self.can_play(current_card):
            return do()
        else:
            print("%s couldn't play and had to draw a card" % self.name)
            self.draw(1)
            if self.can_play(current_card):
                return do()
            else:
                print("%s still couldn't play and had to be skipped" % self.name)
                return None
    def _play(self, current_card):
        for card in self.hand:
            if self.can_play_card(current_card, card):
                return card
        # return self.hand[random.randint(0, len(self.hand)-1)]
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
        print('Current card:', current_card)
        print(*self.hand)
        hand_colors = {}
        for card in self.hand:
            if card.color.name not in hand_colors:
                hand_colors[card.color.name] = []
            hand_colors[card.color.name].append(card)
        desired_color = '!'
        while not desired_color or desired_color.lower()[0] not in hand_colors:
            desired_color = input('What color do you want to play? ')
        desired_color = desired_color.lower()[0]
        print(*hand_colors[desired_color])
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

class Network:
    def __init__(self):
        self.sock1 = socket.socket()
        self.sock2 = socket.socket()
    def send_receive(self, cmd):
        self.send(cmd)
        return self.receive()
    def send(self, cmd):
        self.sock1.send(b'\x00' + cmd.encode())
    def receive(self):
        data = self.sock1.recv(2049)
        if data[0] == b'\x01':
            return pickle.loads(data[1:])
    def poll_event(self):
        data = self.sock1.recv(2049)
        if data[0] == b'\x00':
            self.sock1.send(b'\x01' + pickle.dumps(eval('self.self.'+data[1:])))
class NetworkWrapper(Network):
    def __init__(self, host, player):
        super().__init__()
        self.sock1.connect((host, 4000))
        self.sock2.connect((host, 4001))
        self.player = player
class NetworkPlayer(Player, Network):
    def __init__(self):
        Network.__init__(self)
        self.sock1.bind(('', 4000))
        self.sock2.bind(('', 4001))
        self.sock1.listen(0)
        self.sock1, addr1 = self.sock1.accept()
        self.sock2.listen(0)
        while True:
            sock2, addr2 = self.sock2.accept()
            if addr2[0] == addr1[0]: break
        self.sock2 = sock2
        # self.wrapper = 
        Player.__init__(self, self.send_receive('player.card_count'))

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
    def begin(self):
        while True:
            card = self.player.play(self.card)
            if card is None: self.next_player()
            elif card.number == self.card.number or card.color == self.card.color:
                self.card = card
                if card in self.player.hand:
                    self.player.hand.remove(card)
                if not len(self.player.hand): break
                card.played(self)
                self.next_player()
        player_scores = self.players[:]
        player_scores.sort(key=(lambda x: x.score()), reverse=True)
        for (i, player) in enumerate(player_scores[:-1]):
            print(player.name, 'came in', _ordinal(len(self.players)-i),
            'place with', player.score(), 'points.')
        print(self.player.name, 'wins!')

class Skip(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'S', color, 's', 2, 20)
    def played(self, game):
        game.ix += 1
        print("%s has been skipped"
        % game.players[game.ix%len(game.players)].name)
        # % game.players[(game.ix+1)%len(game.players)].name)
class Reverse(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'R', color, 'r', 2, 20)
    def played(self, game):
        if len(game.players) < 3:
            game.ix += 1
            print("%s has been skipped"
            % game.players[game.ix%len(game.players)].name)
        else:
            game.direction = -game.direction
            print("%s has reversed the direction" % game.player.name)
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

if __name__ == '__main__':
    # game = Game([Player(), RealPlayer()])
    p2 = Player()
    p2.name = 'Player2'
    game = Game([Player(), RealPlayer(), p2])
    game.begin()