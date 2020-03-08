from netsc import Client
from .other import deserialize_card, serialize_card, GameSubstitute, serialize_color, deserialize_color
from .. import Color

class GameClient(Client):
    def deadj_args_start(self, *args):
        return (GameSubstitute(self),), {}
    def deadj_args_play(self, *args):
        return (deserialize_card(args[0]), GameSubstitute(self)), {}
    def adj_return_play(self, card):
        if card is None:
            return card
        return serialize_card(card)
    def deadj_args_ask(self, q, t, limits=()):
        return (q, getattr(__import__(t[0]), t[1])), {'limits': [deserialize_color(l) for l in limits]}
    def adj_return_ask(self, value):
        if isinstance(value, Color):
            return serialize_color(value)
        return value
    def deadj_args_can_play_card(self, card1, card2):
        return (deserialize_card(card1), deserialize_card(card2)), {}
    def deadj_args_can_play(self, card):
        return (deserialize_card(card),), {}
    def deadj_args_remove_from_hand(self, card):
        return (deserialize_card(card),), {}
    def adj_return___getattribute__(self, value):
        if value is self.wrapped.hand:
            return [serialize_card(x) for x in value]
        else: return value
    def post_call_end(self):
        raise GameOver

class GameOver(BaseException): pass