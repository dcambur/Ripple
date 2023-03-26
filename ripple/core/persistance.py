import os
import json
import threading

from .meta import BackupTypes, OperatorTypes


class AOF:
    def __init__(self, persist_info):
        self.persist_info = persist_info
        self.buffer = []
        self.__create_file()
        self.count = 0

    def __create_file(self):
        if not self.__find():
            open(self.persist_info.full_path, "x").close()

    def __find(self):
        return os.path.exists(self.persist_info.full_path)

    def __update_buffer(self, op, key, value):
        self.buffer.append(f"{op}:{key}:{json.dumps(value)}\n")
        self.count += 1

    def write(self, key, value, op):
        self.__update_buffer(op, key, value)

        if self.count_tick():
            thread = threading.Thread(target=fsync_buffer, args=(self.persist_info, self.buffer.copy(),))
            thread.start()
            self.buffer.clear()
            self.count = 0

    def load(self):
        load_dict = {}
        # line[0] -> operator; line[1] -> key, line[2] -> value
        with open(self.persist_info.full_path, "r") as read_desc:
            for line in read_desc:
                line = line.strip(self.persist_info.LINE_SEPARATOR).split(self.persist_info.DATA_SEPARATOR, 2)
                if line[0] == OperatorTypes.WRITE:
                    load_dict[line[1]] = json.loads(line[2])
                if line[0] == OperatorTypes.DELETE:
                    del load_dict[line[1]]
        return load_dict

    def count_tick(self):
        if self.count == self.persist_info.save_every:
            return True
        return False


class Snapshot:
    def __init__(self, persist_info):
        self.to_write = {}
        self.persist_info = persist_info

        self.count = 0
        self.__create_file()

    def __create_file(self):
        if not self.__find():
            with open(self.persist_info.full_path, "w") as write_desc:
                write_desc.write("{}")

    def __find(self):
        return os.path.exists(self.persist_info.full_path)

    def __update_snapshot(self, key, value, op):
        if op == OperatorTypes.WRITE:
            self.to_write[key] = value
        if op == OperatorTypes.DELETE:
            del self.to_write[key]

        self.count += 1

    def write(self, key, value, op):
        self.__update_snapshot(key, value, op)
        if self.count_tick():
            thread = threading.Thread(target=create_snapshot, args=(self.persist_info, self.to_write.copy(),))
            thread.start()
            self.count = 0

    def load(self):
        with open(self.persist_info.full_path, "r") as read_desc:
            return json.load(read_desc)

    def count_tick(self):
        if self.count == self.persist_info.save_every:
            return True
        return False


def create_snapshot(persist_info, to_write):
    with open(persist_info.full_path, "w") as write_desc:
        json.dump(to_write, write_desc)


def fsync_buffer(persist_info, to_write):
    file = open(persist_info.full_path, "a")

    for record in to_write:
        file.write(record)

    file.flush()
    os.fsync(file)

    file.close()


class Persistence:
    def __init__(self, persist_info):
        self.persist_info = persist_info
        self.backup = self.__get_model()

    def persist(self, command):
        if self.backup:
            self.backup.write(command[0], command[1], command[2])

    def __get_model(self):
        match self.persist_info.model_type:
            case BackupTypes.NONE:
                return None
            case BackupTypes.AOF:
                return AOF(self.persist_info)
            case BackupTypes.SNAPSHOT:
                return Snapshot(self.persist_info)

    def load_backup(self):
        match self.persist_info.model_type:
            case BackupTypes.NONE:
                return {}
            case _:
                return self.backup.load()
