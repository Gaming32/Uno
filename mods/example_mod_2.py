import uno
import uno.main as unomain
import unoforge
class EveryOneDraw(uno.Wild):
    def __init__(self):
        super().__init__('Everyone Draw 4', 'ED4', 'ed4')
    def played(self, game):
        super().played(game)
        for player in game.players:
            if player is not game.player:
                player.draw(4)
        if len(game.players) < 3:
            game.ix += 1
        print('%s made everyone draw four cards.' % game.player.name)
unoforge.add_single_card(EveryOneDraw)

name = 'Everyone Draw 4 Card'

if __name__ == '__main__': unomain.main()