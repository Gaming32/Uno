_exit_callbacks = []
def register_exit_callback(func):
    _exit_callbacks.append(func)

mods = None