from netsc import Server
from .other import serialize_card

class GameServer(Server):
    bind_addr = ('', 8660)
    def start(self, game):
        self.wrapped = game
        super().start(None)
    def adj_args_play(self, *args, **kwargs):
        args = list(args)
        args[0] = serialize_card(args[0])
        args[1] = None
        return tuple(args)