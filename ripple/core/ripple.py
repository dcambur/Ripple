import threading

from ripple.core import persist_const
from ripple.core.persistance import RipplePersist


class RippleDB:
    def __init__(self, persist_as=persist_const.NONE):
        self.__write = "+"
        self.__delete = "-"
        self.__persist_manager = RipplePersist(persist_as)
        self.data = self.__persist_manager.sync_db(dict())

    def create(self, key, value):
        self.data[key] = value
        self.__persist_manager.aof_write(key, value, self.__write)

    def read(self, key):
        if key not in self.data.keys():
            return None
        return self.data[key]

    def delete(self, key):
        if key not in self.data.keys():
            return None
        del self.data[key]
        self.__persist_manager.aof_write(key, self.data[key], self.__delete)
        return True

    def create_snapshot(self):
        thread = threading.Thread(target=self.__persist_manager.snapshot_write, args=(self.data,))
        thread.start()
