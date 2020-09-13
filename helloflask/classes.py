import os


class OpenDir:

    def __init__(self, dest):
        self.root = os.getcwd()
        self.destination = dest

    def __enter__(self):
        os.chdir(self.destination)
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.root)
        return None
