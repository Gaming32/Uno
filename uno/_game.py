from ._mods import *
from ._player import *

class Game:
    def __init__(self, players):
        self.players = players
        self.ix = random.randrange(len(self.players))
        self.player = players[self.ix]
        self.card = draw(1)[0]
        self.direction = 1
    def next_player(self):
        self.ix = (self.ix + self.direction) % len(self.players)
        self.player = self.players[self.ix]
    def display_message(self, *vals):
        for player in self.players:
            player.doprint(*vals)
    def game_over(self):
        for player in self.players:
            player.end()
    def begin(self):
        for player in self.players:
            player.start(self)
        while True:
            card = self.player.play(self.card, self)
            if card is None: self.next_player()
            else:
                self.card = card
                if card in self.player.hand:
                    self.player.remove_from_hand(card)
                if not len(self.player.hand): break
                card.played(self)
                self.next_player()
        player_scores = self.players[:]
        player_scores.sort(key=(lambda x: x.score()), reverse=True)
        for (i, player) in enumerate(player_scores[:-1]):
            self.display_message(player.name, 'came in', ordinal(len(self.players)-i),
            'place with', player.score(), 'points.')
        self.display_message(self.player.name, 'wins!')

# __all__ = dir()