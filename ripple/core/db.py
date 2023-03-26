import threading
from .meta import BackupInfo
from .persistance import Persistence


class RippleDB:
    def __init__(self, persist_info=BackupInfo):
        self.persist_info = persist_info
        self.persist_manager = Persistence(persist_info)
        self.data = self.persist_manager.load_backup()

    def create(self, key, value):
        self.data[key] = value
        record = [key, self.data[key], self.persist_info.WRITE]
        self.persist_manager.persist(record)

    def read(self, key):
        if key not in self.data.keys():
            return None
        return self.data[key]

    def delete(self, key):
        if key not in self.data.keys():
            return None

        record = [key, self.data[key], self.persist_info.DELETE]
        del self.data[key]

        self.persist_manager.persist(record)

        return True

    def create_snapshot(self):
        thread = threading.Thread(target=self.persist_manager.backup.write, args=(self.data,))
        thread.start()
