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
        options = value[1:]
        for (i, option) in enumerate(options):
            options[i] = option.split(':', 1)[1]
        return ('menu_load', name, options)
    elif value.startswith('Which option:'):
        return ('menu_wait',)
    elif value.endswith('cards') and ' has ' in value:
        value = value.rsplit(' ', 3)
        return ('card_count', value[0], value[2])
    elif value.startswith('Current card:'):
        value = value[len('Current card: '):]
        return ('current_card', deserialize_card(value))
    elif value.startswith('\u001b[3'):
        return ('hand', [deserialize_card(x) for x in value.split()])
    elif value.startswith('How many '):
        return ('player_count_question', value.strip())
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
        self.value = ''
        _print('CustomStdout initialized\n')
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
        _print('Event dequeued:   %r\n' % (event,))
        return event

class CustomStdin:
    def __init__(self):
        self.value = ''
        self.lock = _thread.allocate_lock()
        _print('CustomStdin initialized\n')
    def writeline(self, value):
        self.lock.acquire()
        self.value = value + '\n'
        self.lock.release()
        _print('Message sent:     %r\n' % value)
    def readline(self, size=-1):
        if hasattr(self, 'value'):
            self.value = ''
        value = ''
        new = '!'
        while new != '\n':
            self.lock.acquire()
            if self.value:
                new = self.value[0]
                value += new
                self.value = self.value[1:]
            self.lock.release()
            time.sleep(0.5)
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
        self.root.protocol('WM_DELETE_WINDOW', (lambda: _thread.interrupt_main()))
        self.root.mainloop()

    def clear_screen(self):
        for widget in self.temp_widgets.values():
            if hasattr(widget, 'destroy'):
                widget.destroy()
        self.temp_widgets.clear()
    def event_loop(self):
        event = (None, None)
        while event[0] != 'game_exit':
            event = self.readstream.dequeue()
            if event[0] == 'menu_load':
                self.clear_screen()
                label = Label(self.root, text=event[1])
                label.pack()
                self.temp_widgets['menu_label'] = label
                self.root.title('Menu: ' + event[1])
                menu = event[2]
            elif event[0] == 'menu_wait':
                for (i, label) in enumerate(menu):
                    button = Button(self.root, text=label)
                    def command(ix=i):
                        self.writestream.writeline(str(ix))
                    button.config(command=command)
                    button.pack()
                    self.temp_widgets['menu_item_%i' % i] = button
            elif event[0] == 'player_count_question' or event[0] == 'name_question':
                self.clear_screen()
                self.root.title('Game Setup')

                if event[0] == 'name_question':
                    event = event + ('What is your name? ',)
                label = Label(self.root, text=event[1].replace('?', ':'))
                label.pack(side=LEFT)
                self.temp_widgets['label'] = label

                if event[0] == 'name_question':
                    var = StringVar(self.root, value='Player')
                else:
                    var = IntVar(self.root, value=1)
                self.temp_widgets['var'] = var
                entry = Entry(self.root, textvariable=var)
                entry.pack(side=LEFT)
                self.temp_widgets['entry'] = entry

                def command(var=var):
                    self.writestream.writeline(str(var.get()))
                button = Button(self.root, text='Ok', command=command)
                button.pack(side=LEFT)
                self.temp_widgets['button'] = button
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