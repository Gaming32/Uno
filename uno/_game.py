from ._mods import *
from ._player import *


class _TempPlayer:
    name = 'The game'


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

    def display_message(self, *vals, end='\n'):
        for player in self.players:
            player.doprint(*vals, end=end)

    def display_message_to_others(self, *vals, end='\n'):
        for player in self.players:
            if player is not self.player:
                player.doprint(*vals, end=end)

    def game_over(self):
        for player in self.players:
            player.end()

    def begin(self):
        for player in self.players:
            player.start(self)
            player.doprint('You are playing against:', ', '.join(
                p.name for p in self.players if p is not player))

        old_player = self.player
        self.player = _TempPlayer()
        while True:
            try:
                self.card.played(self)
            except Exception:
                continue
            else:
                break
        self.player = old_player
        del old_player

        while True:
            # self.display_message_to_others('Waiting for', self.player.name, 'to play...', end='\r')
            card = self.player.play(self.card, self)
            if card is None:
                self.next_player()
            else:
                self.card = card
                if card in self.player.hand:
                    self.player.remove_from_hand(card)
                if not len(self.player.hand):
                    break
                card.played(self)
                self.next_player()

        player_scores = self.players[:]
        for playerix in range(len(player_scores)):
            if player_scores[playerix] is self.player:
                break
        del player_scores[playerix]
        player_scores.sort(key=(lambda x: x.score()), reverse=True)
        for (i, player) in enumerate(player_scores):
            self.display_message(player.name, 'came in', ordinal(len(self.players)-i),
                                 'place with', player.score(), 'points.')
        self.display_message(self.player.name, 'wins!')
        for player in self.players:
            player.end()

# __all__ = dir()
