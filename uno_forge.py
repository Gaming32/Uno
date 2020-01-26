import sys, os
import uno
import uno.main as unomain
import unoforge

__version__ = '1.0'
__author__ = 'Gaming32'

def _exit_callback():
    for cb in unoforge._exit_callbacks:
        try: cb()
        except Exception:
            print('An error occurred in the mod "%s"' % cb.__module__)
            print('More info:\n   ', *sys.exc_info()[:2])

def getmods():
    for file in os.listdir('mods'):
        if not os.path.isfile('mods/' + file): continue
        yield os.path.splitext(os.path.basename(file))[0]

def getname(mod):
    if hasattr(mod, 'name'):
        return mod.name
    else:
        return mod.__name__

def modslist(quitter):
    print('The following are the installed mods:')
    for mod in mods:
        mod = getname(mod)
        print('+', mod)
    print('Total mods: %i' % len(mods))

unomain.options.insert(-1, ('Mods', modslist))
if not os.path.exists('mods'):
    os.mkdir('mods')
sys.path.append('mods')
mods = []

unoforge.mods = mods
for mod in getmods():
    mods.append(__import__(mod))

unomain.exit_callback = _exit_callback
if unoforge._cards_to_add:
    uno.CARD_LIST[:], uno.WEIGHT_LIST[:] = uno.calculate_chance()

for mod in mods:
    if hasattr(mod, 'init'):
        mod.init()

if __name__ == '__main__': unomain.main()