from .. import CARD_SET

def serialize_card(card):
    return (card.__class__.__name__, card.short_name, card.color.name)

def deserialize_card(data):
    for card in CARD_SET:
        if data == serialize_card(card):
            return card
    print('ERROR: could not deserialize card, substituting random card')
    return card

class GameSubstitute:
    def __init__(self, client_obj):
        self.client_obj = client_obj
    def __getattr__(self, attr):
        return getattr(self.client_obj, attr)