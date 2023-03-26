import threading
from .meta import OperatorTypes


class Transaction:
    def __init__(self, db):
        self.db = db
        self.transaction_store = []
        self.lock = threading.Lock()

    def add(self, key, value):
        self.transaction_store.append([key, value, OperatorTypes.WRITE])

    def __commit(self):
        with self.lock:
            for command in self.transaction_store:
                if command[2] == OperatorTypes.WRITE:
                    self.db.create(command[0], command[1])
                if command[2] == OperatorTypes.DELETE:
                    self.db.delete(command[0], command[1])
        self.transaction_store = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.__commit()
        else:
            self.transaction_store = []
        return True
