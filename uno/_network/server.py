from PodSixNet.Server import Server
from .channel import GameChannel

class GameServer(Server):
    channelClass = GameChannel
    def __init__(self):
        super().__init__()