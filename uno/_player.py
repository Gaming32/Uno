from ._color import *
from ._mods import *
from ._core import *
from ._card import *
from .lang import *

class Player:
    __slots__ = ['hand', 'name']
    def __init__(self, card_count=7):
        self.hand = []
        self.draw(card_count)
        self.name = 'Player'
    def start(self, game): pass
    def draw(self, count):
        self.hand.extend(draw(count))
    def remove_from_hand(self, card):
        self.hand.remove(card)
    def handmeth(self, methname, *args, **kwargs):
        return getattr(self.hand, methname, (lambda hand, *args, **kwargs: None))(*args, **kwargs)
    def handfunc(self, funcname, *args, **kwargs):
        return getattr(__builtins__, funcname, (lambda hand, *args, **kwargs: None)) (self.hand, *args, **kwargs)
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
    def doprint(self, *vals, end='\n'): pass
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
        while True:
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
            while desired_number not in color_numbers and not desired_number.startswith('esc'):
                desired_number = input('What number do you want to play? ')
                desired_number = desired_number.strip().lower()
                # try: desired_number = int(desired_number)
                # except ValueError: desired_number = ''
            if desired_number.startswith('esc'): continue
            for card in hand_colors[desired_color]:
                if str(card.number) == desired_number: break
            return card
    def _ask(self, q, t):
        return input(q)
    def doprint(self, *vals, end='\n'): print(*vals, end=end)
class ComputerPlayer(Player):
    NAMES = [
        'Hal',
        'Cortana',
        'Alexa',
        'Bixby',
        'Siri'
    ]
    used_names = set()
    name_loop_count = 0
    def __init__(self, card_count=7):
        super().__init__(card_count)
        if self.used_names == set(self.NAMES):
            self.used_names.clear()
            ComputerPlayer.name_loop_count += 1
        namelist = list(set(self.NAMES) - self.used_names)
        self.name = random.choice(namelist)
        self.used_names.add(self.name)
        name_id = self.name_loop_count
        if name_id > 0:
            name_id = name_id + 1
        self.name += ' ' + int_to_roman(name_id)
        self.name = self.name.strip()
    @staticmethod
    def tally_special(cardlist):
        value = tally(cardlist)
        multiple = 0.5 * len(cardlist) + 0.5
        return value * multiple
    @staticmethod
    def choose_color(cardlist):
        cards = sort_cards(cardlist)
        cols = list(cards)
        cols.sort(key=(lambda x: ComputerPlayer.tally_special(cards[x])))
        return cols[0]
    def _ask(self, q, t):
        if q == questions['wild']:
            return self.choose_color(self.hand)
        else: return super()._ask(q, t)
    def _play(self, current_card):
        cards = sort_cards(self.hand)
        cols = list(cards)
        playable_cols = set()
        for color in cols:
            for card in cards[color]:
                if self.can_play_card(current_card, card):
                    playable_cols.add(color)
        # colored_cards = [cards[x] for x in playable_cols]
        colored_cards = []
        for color in playable_cols:
            colored_cards += cards[color]
        color = self.choose_color(colored_cards)
        col_cards = cards[color]
        col_cards.sort(key=(lambda x: x.points), reverse=True)
        for card in col_cards:
            if self.can_play_card(current_card, card):
                return card
    def end(self):
        self.used_names.clear()
        ComputerPlayer.name_loop_count = 0

def draw(count):
    hand = nrandom.choice(CARD_LIST, count, False, WEIGHT_LIST)
    return list(hand)

# __all__ = dir()