from netsc import Client
from .other import deserialize_card, serialize_card, GameSubstitute

class GameClient(Client):
    def deadj_args_start(self, *args):
        return (GameSubstitute(self),)
    def deadj_args_play(self, *args):
        return (deserialize_card(args[0]), GameSubstitute(self))
    def adj_return_play(self, card):
        if card is None:
            return card
        return serialize_card(ret)
    def deadj_args_can_play_card(self, card1, card2):
        return deserialize_card(card1), deserialize_card(card2)
    def deadj_args_can_play(self, card):
        return deserialize_card(card)