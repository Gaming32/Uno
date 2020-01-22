# Running
To run Uno, use the command `python -m uno`.
To run Uno Forge, use the command `python -m uno_forge`.
# Installing
To install use the command `python -m pip install uno-game`, (`python -m pip install uno-game-forge` for Uno Forge).
# Modding
NOTE: The latest version of uno_forge supports the following uno versions: 1.0.2
## Starting
Create a mod in the `mods` folder with a compatable Python file extension and follow the following conventions:

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
To add a custom main menu item, modify `unomain.options`. `unomain.options` is a list of `(label, func)`. `func` accepts a 1-item list called `quitter`. `quitter[0]` is set to `False` be default, setting it to `True` causes the menu to close; being the main menu, this will most likely end the program.