import uno
import uno.main as unomain
import unoforge

def exit_1(mods):
    print('exit 1')
def exit_2(mods):
    print('loaded mods (except 1):', mods-1)

unoforge.register_exit_callback(exit_1)
unoforge.register_exit_callback(exit_2)