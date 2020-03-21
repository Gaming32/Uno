from ._mods import *
from ._color import *
from ._colors import *

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
    def __eq__(self, other):
        return (
            self.short_name == other.short_name and
            self.number == other.number and
            self.color == other.color
        )
    def __hash__(self):
        return hash(self.short_name) * 1 + hash(self.number) * 8 + hash(self.color) * 64

class Skip(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'S', color, 's', 2, 20)
    def played(self, game):
        game.ix += game.direction
        game.display_message("%s has been skipped"
        % game.players[game.ix%len(game.players)].name)
        # % game.players[(game.ix+1)%len(game.players)].name)
class Reverse(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'R', color, 'r', 2, 20)
    def played(self, game):
        if len(game.players) <= 2:
            game.ix += game.direction
            game.display_message("%s has been skipped"
            % game.players[game.ix%len(game.players)].name)
        else:
            game.direction = -game.direction
            game.display_message("%s has reversed the direction" % game.player.name)
class Draw2(Card):
    def __init__(self, long_name, color):
        super().__init__(long_name, 'D2', color, 'd2', 2, 20)
    def played(self, game):
        game.ix += game.direction
        game.display_message("%s forced %s to draw two cards"
        % (game.player.name,
        game.players[game.ix%len(game.players)].name))
        game.players[game.ix%len(game.players)].draw(2)

class Wild(Card):
    def __init__(self, long_name='Wild', short_name='W', number='w'):
        super().__init__(long_name, short_name, WILD, number, 4, 50)
    def played(self, game):
        game.card = copy.copy(self)
        game.card.color = game.player.ask(
            questions['wild'], Color, limits=(WILD,))
        game.display_message('%s changed the color to %s.' % (game.player.name, game.card.color.name))
class WildDraw4(Wild):
    def __init__(self):
        super().__init__('Wild Draw 4', 'D4', 'd4')
    def played(self, game):
        cur_color = game.card.color
        super().played(game)
        game.ix += game.direction
        attacked_player = game.players[game.ix%len(game.players)]
        game.display_message("%s forced %s to draw four cards."
        % (game.player.name, attacked_player.name))
        called = attacked_player.ask(questions['call wild'], bool)
        if called:
            if cur_color in sort_cards(game.player.hand):
                game.display_message("%s called and forced %s to draw four cards instead."
                % (attacked_player.name, game.player.name))
                game.player.draw(4)
                game.ix -= 1
            else:
                game.display_message("%s called and was wrong, so they had to draw six cards."
                % attacked_player.name)
                attacked_player.draw(6)
        else: attacked_player.draw(4)

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
def tally(seq):
    res = 0
    for card in seq:
        res += card.points
    return res
def sort_cards(seq, n='object'):
    if n == 'object':
        do = compile('card.color', '<card_sort>', 'eval')
    elif n == 'code':
        do = compile('card.color.code', '<card_sort>', 'eval')
    res = {}
    for card in seq:
        if eval(do) not in res:
            res[eval(do)] = []
        res[eval(do)].append(card)
    return res

from ._game import *
_r_core = False
if not _r_core:
    from ._core import *
    _r_core = True

# __all__ = dir()