from PodSixNet.Server import Server
from .channel import GameChannel

class GameServer(Server):
    channelClass = GameChannel
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_count = 0
        self.channels = {}
    def Connected(self, channel, addr):
        self.channels[self.conn_count] = channel
        channel.Send({'action': '_init', 'id': self.conn_count})
        self.conn_count += 1