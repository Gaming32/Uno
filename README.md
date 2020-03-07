# Running
To run Uno, use the command `python -m uno`.
To run Uno Forge, use the command `python -m uno_forge`.
# Installing
To install use the command `python -m pip install uno-game`, (`python -m pip install uno-game-forge` for Uno Forge).
# Modding
NOTE: The latest version of uno_forge supports the following uno versions: 1.0.2
## Starting
Create a mod in the `mods` folder or the `~/.uno_forge_mods` folder with a compatable Python file extension and follow the following conventions:

File start:
``` python
import uno
import uno.main as unomain
import unoforge # Optional
```

File end:
``` python
if __name__ == '__main__': unomain.main()
```
## Features
### Custom main menu item
To add a custom main menu item, use the function `unoforge.add_menu_function`. A callback passed to this function may return `True` to exit the menu.
### Executing something when the game ends
To execute something when the game ends, use the function `unoforge.register_exit_callback`.