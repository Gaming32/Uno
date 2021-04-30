from netsc import Server
from .other import serialize_card, deserialize_card, serialize_color, deserialize_color
from . import shared
from .. import Color


class GameServer(Server):
    bind_addr = ('', 8660)
    attrs = ['hand', 'name']
    _hand_count = 7
    _name = None
    _is_replacing = False

    def __getattr__(self, attr):
        if attr == 'hand':
            hand = super().__getattr__(attr)
            self._hand_count = len(hand)
            return hand
        if attr == 'name':
            if self._name is None:
                self._name = super().__getattr__(attr)
            return self._name
        return super().__getattr__(attr)

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
        else:
            return value

    def post_func_end(self):
        self.sock.close()
        shared.player_count -= 1

    def _replace_player(self, game=None):
        if self._is_replacing:
            return
        self._is_replacing = True
        if game is None:
            game = self.wrapped
        from .. import ComputerPlayer
        game.player = ComputerPlayer(self._hand_count)
        game.player.name = self._name
        game.players[game.ix] = game.player
        game.display_message('Player', self._name,
                             'has quit. A computer will take their place')
        self._is_replacing = False
        return game.player

    def play(self, current_card, game):
        try:
            return self.__getattr__('play')(current_card, game)
        except ConnectionError:
            p = self._replace_player()
            if p:
                return p.play(current_card, game)

    def doprint(self, *vals, end='\n'):
        try:
            return self.__getattr__('doprint')(*vals, end=end)
        except ConnectionError:
            p = self._replace_player()
            if p:
                return p.doprint(*vals, end=end)
