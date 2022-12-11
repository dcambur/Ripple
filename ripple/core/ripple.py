from ripple.core import persist_const
from ripple.core.persistance import RipplePersist


class RippleDB:
    def __init__(self, persist_as=persist_const.NONE):
        self.data = dict()
        self._persist_manager = RipplePersist(persist_as)

    def create(self, key, value):
        self.data[key] = value

    def read(self, key):
        if key not in self.data.keys():
            return None
        return self.data[key]

    def delete(self, key):
        if key not in self.data.keys():
            return None
        del self.data[key]
        return True

    def init(self):
        self._persist_manager.init()



