from .. import CARD_SET
from .. import _colors

def serialize_card(card):
    return (card.__class__.__name__, card.short_name, card.color.name)

def deserialize_card(data):
    for card in CARD_SET:
        if data == serialize_card(card):
            return card
    print('ERROR: could not deserialize card, substituting random card')
    return card

def serialize_color(color):
    return (color.code, color.name)

COLOR_SET = {getattr(_colors, c) for c in dir(_colors) if isinstance(getattr(_colors, c), _colors.Color)}
def deserialize_color(data):
    for color in COLOR_SET:
        if data == serialize_color(color):
            return color
    print('ERROR: could not deserialize color, substituting random color')
    return color

class GameSubstitute:
    def __init__(self, client_obj):
        self.client_obj = client_obj
    def __getattr__(self, attr):
        return getattr(self.client_obj, attr)