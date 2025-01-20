class TextFile:
    def __init__(self, filepath:str):
        self.filepath = filepath

    def load(self):
        with open(self.filepath) as f:
            return f.read()

    def save(self, text:str):
        with open(self.filepath, 'w') as f:
            f.write(text)