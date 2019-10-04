from ._color import *
from ._card import *
from ._colors import *

CARD_SET = set()
COLOR_SET = {RED, GREEN, BLUE, YELLOW, WILD}

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
WILD_CARD = Wild()
WILD_DRAW4 = WildDraw4()
CARD_SET.add(WILD_CARD)
CARD_SET.add(WILD_DRAW4)

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

# __all__ = dir()