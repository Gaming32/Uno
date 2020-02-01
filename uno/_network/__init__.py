from .server import GameServer
from .client import GameClient

def NetworkPlayer(card_count=7):
    server = GameServer(None)
    addr = server.accept()
    print('%s joined the game!' % (addr,))
    return server