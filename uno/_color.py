class Color:
    def __init__(self, code, name, ansi):
        self.code = code
        self.name = name
        self.ansi = '3' + str(ansi)
    def __eq__(self, other):
        return (
            self.code == other.code and
            self.name == other.name
        )
    def __hash__(self):
        return hash(self.code) * 1 + hash(self.name) * 8

# __all__ = dir()