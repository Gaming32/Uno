import _thread
from time import sleep
from .._player import Player
from .server import GameServer

class ServerHandler:
    _player_count_so_far = 0
    _initted = False
    server = None
    card_count = None
    def __init__(self, card_count=7):
        self.id = _player_count_so_far
        ServerHandler.card_count = card_count
        ServerHandler._player_count_so_far += 1
    def poll_loop(self):
        while self._initted:
            self.server.Pump()
            sleep(0.0001)
    def start(self):
        if not ServerHandler._initted:
            ServerHandler._initted = True
            ServerHandler.server = GameServer(None, ('', 1920), self._player_count_so_far)
            _thread.start_new_thread(self.poll_loop, ())
    def __del__(self):
        ServerHandler._player_count_so_far = 0
        ServerHandler._initted = False
        ServerHandler.server = None
        ServerHandler.card_count = None
    def _function(self, funcname, args=[], kwargs={}):
        self.server.Send({'action': funcname, 'args': args, 'kwargs': kwargs})

    def start(self):
        pass

def _client_poll_loop(ql, listener): ...

def connect_to_server(): ...