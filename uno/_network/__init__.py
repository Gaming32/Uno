from .server import GameServer
from .client import GameClient

def NetworkPlayer(card_count=7):
    return GameServer(None)