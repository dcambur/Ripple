import os
import json

from ripple.core import const


class AOF:
    def __init__(self, name="ripple"):
        self.name = name + ".adb"
        self.__write = "+"
        self.__delete = "-"
        self.__aof_separator = ":"
        self.__line_separator = "\n"
        self.__create_file()

    def __create_file(self):
        if not self.__find_aof():
            open(self.name, "x").close()

    def __find_aof(self):
        return os.path.exists(self.name)

    def aof_load(self, load_dict):
        # line[0] -> operator; line[1] -> key, line[2] -> value
        with open(self.name, "r") as read_desc:
            for line in read_desc:
                line = line.strip(self.__line_separator).split(self.__aof_separator, 2)
                if line[0] == self.__write:
                    load_dict[line[1]] = json.loads(line[2])
                if line[0] == self.__delete:
                    del load_dict[line[1]]
        return load_dict

    def aof_write(self, key, value, op):
        with open(self.name, "a") as write_desc:
            write_desc.write(f"{op}:{key}:{json.dumps(value)}\n")


class Snapshot:
    def __init__(self, name, save_after=5):
        self.__snapshot_name = name + ".sdb"
        self.__create_file()
        self.save_after = save_after
        self.count = 0

    def __create_file(self):
        if not self.__find_snapshot():
            with open(self.__snapshot_name, "w") as write_desc:
                write_desc.write("{}")

    def __find_snapshot(self):
        return os.path.exists(self.__snapshot_name)

    def snapshot_write(self, data_dict):
        if self.count_tick():
            with open(self.__snapshot_name, "w") as write_desc:
                json.dump(data_dict, write_desc)

    def snapshot_load(self):
        with open(self.__snapshot_name, "r") as read_desc:
            return json.load(read_desc)

    def count_tick(self):
        self.count += 1
        if self.count == self.save_after:
            self.count = 0
            return True
        return False


class RipplePersist:
    def __init__(self, persist_as, name="ripple"):
        self.__name = name
        self.__persist_as = persist_as
        self.model = self.__get_model()

    def __get_model(self):
        match self.__persist_as:
            case const.NONE:
                return None
            case const.AOF:
                return AOF(self.__name)
            case const.SNAPSHOT:
                return Snapshot(self.__name)

    def sync_db(self, data_dict):
        match self.__persist_as:
            case const.NONE:
                return data_dict
            case const.AOF:
                return self.model.aof_load(data_dict)
            case const.SNAPSHOT:
                return self.model.snapshot_load()
        return data_dict
