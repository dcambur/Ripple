from ripple.core.ripple import RippleDB


class Transaction:
    def __init__(self, db):
        self.db = db
        self.transaction_store = {}

    def add(self, key, value):
        self.transaction_store[key] = value

    def __commit(self):
        return self.db.data.update(self.transaction_store)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__commit()
