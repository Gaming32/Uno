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

class Wild(Card):
    def __init__(self, long_name='Wild', short_name='W', number='w'):
        super().__init__(long_name, short_name, WILD, number, 4, 50)
    def played(self, game):
        game.card = copy.copy(self)
        game.card.color = game.player.ask(
            'What color would you like to change the color to? ', Color, limits=(WILD,))
        print('%s changed the color to %s.' % (game.player.name, game.card.color.name))
class WildDraw4(Wild):
    def __init__(self):
        super().__init__('Wild Draw 4', 'D4', 'd4')
    def played(self, game):
        super().played(game)
        game.ix += 1
        print("%s forced %s to draw four cards"
        % (game.player.name,
        game.players[game.ix%len(game.players)].name))
        game.players[game.ix%len(game.players)].draw(4)

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

from ._game import *
_r_core = False
if not _r_core:
    from ._core import *
    _r_core = True

__all__ = dir()