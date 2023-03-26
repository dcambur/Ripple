import threading
from ripple.core.db import RippleDB
from ripple.core.meta import SnapshotInfo, AOFInfo
from datetime import datetime


def create_data(db, key, value):
    db.create(key, value)


def read_data(db, key):
    print(f"Reading key {key}: {db.read(key)}")


def delete_data(db, key):
    db.delete(key)


def worker(db, key, value):
    create_data(db, key, value)
    read_data(db, key)


if __name__ == "__main__":
    n1 = datetime.now()
    snapshot_meta = SnapshotInfo("", "dumbdb", 5)
    aof_meta = AOFInfo("", "dumbdb", 5)
    db = RippleDB(snapshot_meta)

    threads = []
    for i in range(10):
        key = f"key{i}"
        value = f"value{i}"
        thread = threading.Thread(target=worker, args=(db, key, value))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    ne = datetime.now() - n1
    print(ne)
