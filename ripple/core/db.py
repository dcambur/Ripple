import threading
from .meta import BackupInfo, OperatorTypes, NONEInfo
from .persistance import Persistence


class RippleDB:
    def __init__(self, persist_info=NONEInfo()):
        self.persist_info = persist_info
        self.persist_manager = Persistence(persist_info)
        self.data = self.persist_manager.load_backup()
        self.lock = threading.Lock()

    def create(self, key, value):
        with self.lock:
            self.data[key] = value
            record = [key, self.data[key], OperatorTypes.WRITE]
            self.persist_manager.persist(record)

    def read(self, key):
        with self.lock:
            if key not in self.data:
                return None
            return self.data[key]

    def delete(self, key):

        with self.lock:
            if key not in self.data:
                return None

            record = [key, self.data[key], OperatorTypes.DELETE]
            del self.data[key]
            self.persist_manager.persist(record)

            return True

    def create_snapshot(self):
        thread = threading.Thread(target=self.persist_manager.backup.write, args=(self.data,))
        thread.start()
