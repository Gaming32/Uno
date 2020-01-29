import sys
import queue, _thread

def deserialize_card(value):
    for card in uno.CARD_SET:
        if str(card) == value:
            return card
    _print('ERROR: could not deserialize card, substituting random card\n')
    return card

_stderr_mutex = _thread.allocate_lock()
def _print(value):
    _stderr_mutex.acquire()
    sys.stdout.write(value)
    _stderr_mutex.release()

def parse_stdout(value:str):
    if value.startswith('Current card:'):
        value = value[:len('Current card: ')]
        return ('current_card', deserialize_card(value))
    elif value.startswith('\u001b[3'):
        return ('hand', [deserialize_card(x) for x in value.split()])
    elif value.startswith('How many '):
        return ('player_count', value.strip())
    elif value.startswith('What color would you like to play?'):
        return ('color_question',)
    elif value.startswith('What number would you like to play?'):
        return ('number_question',)
    else:
        _print('ERROR: could not parse input "%s"\n' % value)
        return ('error', 'parse_failed')

class CustomStdout:
    def __init__(self):
        self.queue = queue.Queue()
        _print('CustomStdout initialized\n')
    def write(self, value):
        pass
    def flush(self):
        pass
    def dequeue(self):
        event = self.queue.get_nowait()
        _print('Event dequeued: %s\n' % event)

import uno
import uno.main as unomain
from tkinter import *

def init():
    pass

if __name__ == '__main__':
    init()
    unomain.main()