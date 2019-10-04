class Color:
    def __init__(self, code, name, ansi):
        self.code = code
        self.name = name
        self.ansi = '3' + str(ansi)

# __all__ = dir()