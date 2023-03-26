import threading
from ripple.core.meta import SnapshotInfo, AOFInfo
from ripple.core.db import RippleDB


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
    snapshot_meta = SnapshotInfo("", "dumbdb")
    db = RippleDB(snapshot_meta)

    threads = []
    for i in range(200):
        key = f"key{i}"
        value = f"value{i}"
        thread = threading.Thread(target=worker, args=(db, key, value))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All threads completed.")
