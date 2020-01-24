import sys
from ._player import *
# from ._network import *
from ._game import *

player_types = [
    ('computer players', ComputerPlayer),
    ('real players (1 or 0)', RealPlayer),
    # ('LAN players', Server),
]

def get_number(value):
        try: value = int(value)
        except ValueError:
            print('Please enter a number.')
            return
        else: return value

def play_game(quitter):
    player_list = []
    for (label, klass) in player_types:
        value = get_number(input('How many %s would you like? ' % label))
        while value is None:
            value = get_number(input('How many %s would you like? ' % label))
        for _ in range(value):
            player_list.append(klass())
    game = Game(player_list)
    game.begin()

def join_game(quitter):
    while True:
        host = input('Hostname/IP of the game to join: ')
        try: client = Client(host)
        except socket.error:
            print('Unable to connect to game')
            continue
        else: break
    client.mainloop()

def end(quitter):
    print('Goodbye.')
    quitter[0] = True

options = [
    ('Play Game', play_game),
    # ('Join Network Game', join_game),
    ('Quit', end),
]

def opt_display(name, opts):
    value = name
    for (n, (label, func)) in enumerate(opts):
        value += '\t%i:%s' % (n, label)
    return value

def menu(name, options):
    quitter = [False]
    while True:
        print(opt_display(name, options))
        value = input('Which option: ')
        value = get_number(value)
        if value is None: continue
        elif value < len(options):
            options[value][1](quitter)
        else: print('Invalid option: %s' % value)
        if quitter[0]: return

def exit_callback(): pass

def main():
    try: menu('Main Menu', options)
    except KeyboardInterrupt: pass
    exit_callback()

# __all__ = dir()

if __name__ == '__main__': main()