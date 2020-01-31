import sys
import queue, _thread, io, time

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
    if '\t' in value and ':' in value:
        value = value.split('\t')
        name = value[0]
        options = value[1]
        return ('menu_load', value[0], value[1:])
    elif value.startswith('Which option:'):
        return ('menu_wait',)
    elif value.startswith('Current card:'):
        value = value[len('Current card: '):]
        return ('current_card', deserialize_card(value))
    elif value.startswith('\u001b[3'):
        return ('hand', [deserialize_card(x) for x in value.split()])
    elif value.startswith('How many '):
        return ('player_count', value.strip())
    elif value.startswith('What color do you want to play?'):
        return ('color_question',)
    elif value.startswith('What number do you want to play?'):
        return ('number_question',)
    elif value.startswith('What is your name?'):
        return ('name_question',)
    elif value.startswith('Goodbye'):
        return ('game_exit',)
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
        event = self.queue.get()
        _print('Event dequeued: %r\n' % (event,))
        return event

class CustomStdin(io.StringIO):
    def writeline(self, value):
        sys.stdin.truncate(0)
        sys.stdin.seek(0)
        sys.stdin.write(value + '\n')
    def readline(self, size=-1):
        value = ''
        new = '!'
        while new != '\n':
            new = self.read(1)
            value += new
        value += '\n'
        return value

import uno
import uno.main as unomain
from tkinter import *

class GameWindowManager:
    def __init__(self):
        self.readstream = CustomStdout()
        sys.stdout = self.readstream
        self.writestream = CustomStdin()
        sys.stdin = self.writestream

        self.widgets = {}
        self.temp_widgets = {}
        self.root = None
    def run(self):
        self.root = Tk()
        self.root.mainloop()

    def clear_screen(self):
        for widget in self.temp_widgets:
            widget.destroy()
        self.temp_widgets.clear()
    def event_loop(self):
        event = (None, None)
        while event[0] != 'game_exit':
            event = self.readstream.dequeue()
            if event[0] == 'menu_load':
                menu = (event[1], event[2])
            elif event[0] == 'menu_wait':
                self.clear_screen()
                self.root.title('Menu: ' + menu[0])
                for (i, label) in enumerate(menu[1]):
                    button = Button(self.root, text=label)
                    def command(ix=i):
                        self.writestream.writeline(str(ix))
                    button.config(command=command)
                    button.pack()
        self.root.destroy()

def init():
    manager = GameWindowManager()
    _thread.start_new_thread(manager.run, ())
    _thread.start_new_thread(manager.event_loop, ())
    # time.sleep(0.5)
    # unomain.menu = manager.menu

if __name__ == '__main__':
    init()
    unomain.main()