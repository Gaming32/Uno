from .. import CARD_SET, _colors, Wild, copy

COLOR_SET = {getattr(_colors, c) for c in dir(_colors) if isinstance(getattr(_colors, c), _colors.Color)}
WILD_SET = set()
color_list = list(COLOR_SET)
for card in CARD_SET:
    if isinstance(card, Wild):
        temp_list = (copy.copy(card) for i in range(len(color_list)))
        for (i, subcard) in enumerate(temp_list):
            subcard.color = color_list[i]
            WILD_SET.add(subcard)
del color_list, card, temp_list, i, subcard

def serialize_card(card):
    return (card.__class__.__name__, card.short_name, card.color.name)

def deserialize_card(data):
    for card in CARD_SET | WILD_SET:
        if data == serialize_card(card):
            return card
    print('ERROR: could not deserialize card, substituting random card')
    return card

def serialize_color(color):
    return (color.code, color.name)

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