import uno as _uno
import uno.main as _unomain

_exit_callbacks = []
def register_exit_callback(func):
    _exit_callbacks.append(func)

mods = None

def add_menu_option(label, func, index=None):
    """Arguments
---------
label : str
    The label for the option
func : callable
    Callable to call when option is selected; return `True` to exit the menu
index : int, None
    Where to put the option (uses list.insert); if is `None` adds to end (uses list.append)"""
    def menu_option(quitter, func=func):
        ret = func()
        if ret is not None:
            quitter[0] = bool(ret)
    opt = (label, func)
    if index is None:
        _unomain.options.append(opt)
    else:
        _unomain.options.insert(index, opt)

_cards_to_add = set()
def add_single_card(card_class):
    card_obj = card_class()
    _uno.CARD_SET.add(card_obj)
    _cards_to_add.add(card_obj)
    return card_obj

def menu(name, **opts):
    """Note: OrderedDict reccomended for `opts` argument"""
    unomain.menu(name, list(opts.items()))

def add_custom_player_type(label, player_class):
    """`label` is displayed as "How many %s would you like?" Where %s is `label`"""
    unomain.player_types.append((label, player_class))