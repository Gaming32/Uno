import uno
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
EVERYONE_DRAW_CARD = EveryOneDraw()
uno.CARD_SET.add(EVERYONE_DRAW_CARD)
uno.CARD_LIST[:], uno.WEIGHT_LIST[:] = uno.calculate_chance()

name = 'Everyone Draw 4 Card'

if __name__ == '__main__':
    from uno.main import *
    main()