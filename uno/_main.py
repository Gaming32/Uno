from ._player import *
from ._network import *

def main():
    def get_number(value):
        try: value = int(value)
        except ValueError:
            print('Please enter a number.')
            return
        else: return value
    def play_game():
        player_list = []

        value = get_number(input('How many ComputerPlayers would you like? '))
        while value is None:
            value = get_number(input('How many ComputerPlayers would you like? '))
        for _ in range(value):
            player_list.append(ComputerPlayer())

        value = get_number(input('How many RealPlayers would you like? '))
        while value is None:
            value = get_number(input('How many RealPlayers would you like? '))
        for _ in range(value):
            player_list.append(RealPlayer())

        value = get_number(input('How many NetworkPlayers would you like? '))
        while value is None:
            value = get_number(input('How many NetworkPlayers would you like? '))
        for _ in range(value):
            player_list.append(NetworkPlayer())

        game = Game(player_list)
        game.begin()
    def join_game():
        player = RealPlayer()
        while True:
            host = input('Hostname/IP of the game to join: ')
            try: wrapper = NetworkWrapper(host, player)
            except socket.error:
                print('Unable to connect to game')
                continue
            else: break
        wrapper.poll_events()
    while True:
        print('Main Menu\t0:Play Game\t1:Join Network Game\t2:Quit')
        value = input('Which option: ')
        value = get_number(value)
        if value == 2:
            print('Goodbye.')
            import sys; sys.exit()
        elif value == 0: play_game()
        elif value == 1: join_game()
        elif value is None: continue
        else: print('Invalid option: %s' % value)

__all__ = dir()

if __name__ == '__main__': main()