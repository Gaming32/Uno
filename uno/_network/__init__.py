from .server import GameServer
from .client import GameClient, GameOver
from . import shared

def NetworkPlayer(card_count=7):
    server = GameServer(None)
    print('Waiting for Player', shared.player_count+1, 'to join...', end='\r')
    addr = server.accept()
    player_name = server.name
    print('%s joined the game!' % player_name, ' '*(11+len(player_name)))
    shared.player_count += 1
    return server