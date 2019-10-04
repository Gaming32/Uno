import sys, os
import uno
from uno._main import *

def getmods():
    for file in os.listdir('mods'):
        if not os.path.isfile('mods/' + file): continue
        yield os.path.splitext(os.path.basename(file))[0]
def modslist(quitter):
    print('The following are the installed mods:')
    for mod in mods:
        if hasattr(mod, 'name'):
            mod = mod.name
        else:
            mod = mod.__name__
        print('+', mod)
options.insert(-1, ('Mods', modslist))
if not os.path.exists('mods'):
    os.mkdir('mods')
sys.path.append('mods')
mods = []
for mod in getmods():
    mods.append(__import__(mod))

if __name__ == '__main__': main()