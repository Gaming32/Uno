from ._color import *
from ._mods import *
from ._core import *
from ._card import *

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
        return tally(self.hand)
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
    def ask(self, q, t=str, limits=()):
        while True:
            value = self._ask(q, t)
            value, valid = self._validate_ask(value, t, limits)
            if valid: return value
    def _ask(self, q, t):
        if issubclass(t, Color):
            return random.choice(list(COLOR_SET))
        elif issubclass(t, str):
            return random.choice(string.printable)
        elif issubclass(t, bool):
            return bool(random.randint(0, 1))
    def _validate_ask(self, v, t, limits):
        ret = ()
        if isinstance(v, t): ret = v, True
        elif issubclass(t, Color):
            for color in COLOR_SET:
                if color.code == str(v[0]):
                    ret = color, True
                    break
            else:
                ret = v, False
        elif issubclass(t, bool):
            if isinstance(v, str):
                v = v.lower()
                if v[0] == 'y':
                    ret = True, True
                elif v[0] == 'n':
                    ret = False, True
                elif v[0] == 't':
                    ret = True, True
                elif v[0] == 'f':
                    ret = False, True
                elif v[0] == '1':
                    ret = True, True
                elif v[0] == '0':
                    ret = False, True
                else:
                    ret = v, False
            else:
                ret = bool(v), True
        else: ret = v, False
        if ret[0] in limits: return ret[0], False
        else: return ret
    def end(self): pass
    def doprint(self, *vals): pass
    def can_play_card(self, current_card, card):
        return (card.color == WILD or
        card.number == current_card.number or
        card.color == current_card.color)
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
        hand_colors = sort_cards(self.hand, 'code')
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
    def _ask(self, q, t):
        return input(q)
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
    def _ask(self, q, t):
        if q == questions['wild']:
            cards = sort_cards(self.hand)
            cols = list(cards)
            cols.sort(key=(lambda x: tally(cards[x])))
            return cols[0]
        else: return super()._ask(q, t)
    def _play(self, current_card):
        self.hand.sort(key=(lambda x: x.points), reverse=True)
        for card in self.hand:
            if self.can_play_card(current_card, card):
                return card

def draw(count):
    hand = nrandom.choice(CARD_LIST, count, False, WEIGHT_LIST)
    return list(hand)

# __all__ = dir()