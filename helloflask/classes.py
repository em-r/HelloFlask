import os


class OpenDir:
    """A class used to access directory using context managers
        and change directory back after exiting the context 
        manager
    """

    def __init__(self, dest: str):
        self.root = os.getcwd()
        self.destination = dest

    def __enter__(self):
        os.chdir(self.destination)
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.root)
        return None
