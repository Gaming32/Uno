import uno
import uno.main as unomain
import unoforge

def exit_1():
    print('exit 1')
def exit_2():
    print('loaded mods (except 1):', unoforge.mods-1)

unoforge.register_exit_callback(exit_1)
unoforge.register_exit_callback(exit_2)