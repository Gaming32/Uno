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