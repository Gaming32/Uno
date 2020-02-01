from netsc import Server
from .other import serialize_card, deserialize_card

class GameServer(Server):
    bind_addr = ('', 8660)
    def adj_args_start(self, game):
        self.wrapped = game
        return None
    def adj_args_play(self, *args, **kwargs):
        args = list(args)
        args[0] = serialize_card(args[0])
        args[1] = None
        return tuple(args)
    def deadj_return_play(self, card):
        if card is None:
            return card
        return deserialize_card(card)
    def adj_args_can_play_card(self, card1, card2):
        return serialize_card(card1), serialize_card(card2)
    def adj_args_can_play(self, card):
        return serialize_card(card)