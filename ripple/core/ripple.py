import threading

from ripple.core import const
from ripple.core.persistance import RipplePersist


class RippleDB:
    def __init__(self, persist_as=const.NONE):

        self.persist_as = persist_as
        self.__persist_manager = RipplePersist(self.persist_as)
        self.data = self.__persist_manager.sync_db(dict())

    def persist(self, command):
        if self.persist_as == const.SNAPSHOT:
            self.__persist_manager.model.snapshot_write(self.data)
        if self.persist_as == const.AOF:
            self.__persist_manager.model.aof_write(command[0], command[1], command[2])

    def create(self, key, value):
        self.data[key] = value
        self.persist([key, value, const.WRITE])

    def read(self, key):
        if key not in self.data.keys():
            return None
        return self.data[key]

    def delete(self, key):
        if key not in self.data.keys():
            return None

        tmp_record = [key, self.data[key], const.DELETE]
        del self.data[key]
        self.persist(tmp_record)

        return True

    def create_snapshot(self):
        thread = threading.Thread(target=self.__persist_manager.model.snapshot_write, args=(self.data,))
        thread.start()
