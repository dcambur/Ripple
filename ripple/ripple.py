import os

from ripple.core.db_init import RippleInit
class RippleDB:
    def __init__(self, name, path=os.getcwd()):
        self.db_init = RippleInit(name, path)

    def write(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
