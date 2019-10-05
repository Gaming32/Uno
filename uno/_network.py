class Token:
    def __init__(self, string):
        self.reset(string)
    def reset(self, string):
        self.string = string
    def tokenize(self):
        for char in self.string:
            pass