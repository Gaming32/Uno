from netsc import Server
from .other import serialize_card, deserialize_card, serialize_color, deserialize_color
from .. import Color

class GameServer(Server):
    bind_addr = ('', 8660)
    attrs = ['hand', 'name']
    def adj_args_start(self, game):
        self.wrapped = game
        return None,
    def adj_args_play(self, *args, **kwargs):
        args = list(args)
        args[0] = serialize_card(args[0])
        args[1] = None
        return tuple(args)
    def deadj_return_play(self, card):
        if card is None:
            return card
        return deserialize_card(card)
    def adj_args_ask(self, q, t, limits=()):
        self.last_ask_type = t
        return q, (t.__module__, t.__name__), [serialize_color(l) for l in limits]
    def deadj_return_ask(self, value):
        if self.last_ask_type == Color:
            return deserialize_color(value)
        return value
    def adj_args_can_play_card(self, card1, card2):
        return serialize_card(card1), serialize_card(card2)
    def adj_args_can_play(self, card):
        return serialize_card(card),
    def adj_args_remove_from_hand(self, card):
        return serialize_card(card),
    def deadj_return___getattribute__(self, value):
        if isinstance(value, tuple):
            return [deserialize_card(x) for x in value]
        else: return value
    def post_func_end(self):
        self.sock.close()