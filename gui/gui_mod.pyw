import sys
import queue, _thread, io

def deserialize_card(value):
    for card in uno.CARD_SET:
        if str(card) == value:
            return card
    _print('ERROR: could not deserialize card, substituting random card\n')
    return card

_stderr_mutex = _thread.allocate_lock()
def _print(value):
    _stderr_mutex.acquire()
    sys.stderr.write(value)
    _stderr_mutex.release()

def parse_stdout(value:str):
    if value.startswith('Current card:'):
        value = value[:len('Current card: ')]
        return ('current_card', deserialize_card(value))
    elif value.startswith('\u001b[3'):
        return ('hand', [deserialize_card(x) for x in value.split()])
    elif value.startswith('How many '):
        return ('player_count', value.strip())
    elif value.startswith('What color do you wand to play?'):
        return ('color_question',)
    elif value.startswith('What number do you want to play?'):
        return ('number_question',)
    elif value.startswith('What is your name?'):
        return ('name_question',)
    else:
        _print('ERROR: could not parse input %r\n' % value)
        return ('error', 'parse_failed')

class CustomStdout:
    def __init__(self):
        self.queue = queue.Queue()
        _print('CustomStdout initialized\n')
        self.value = ''
    def write(self, value):
        self.value += value
        if value.endswith('\n'):
            self.flush()
    def flush(self):
        self.value = self.value.strip('\n')
        if not self.value: return
        _print('Message recieved: %r\n' % self.value)
        self.queue.put(parse_stdout(self.value))
        self.value = ''
    def dequeue(self):
        event = self.queue.get_nowait()
        _print('Event dequeued: %s\n' % event)
        return event

def write_stdin(self, value):
    sys.stdin.truncate(0)
    sys.stdin.seek(0)
    sys.stdin.write(value + '\n')

import uno
import uno.main as unomain
from tkinter import *

class GameWindowManager:
    def __init__(self):
        sys.stdout = CustomStdout()
        # sys.stdin = io.StringIO()
        self.widgets = {}
        self.root = None
    def run(self):
        self.root = Tk()
        self.root.mainloop()

    def clear_screen(self):
        pass
    def menu(self, name, options):
        self.clear_screen()

def init():
    manager = GameWindowManager()
    # unomain.menu = manager.menu
    _thread.start_new_thread(manager.run, ())

if __name__ == '__main__':
    init()
    unomain.main()