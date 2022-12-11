import os
import json

from ripple.core import persist_const

class RipplePersist:
    def __init__(self, persist_as=persist_const.NONE):
        self.__aof_separator = ":"
        self.__write = "+"
        self.__delete = "-"
        self.__aof_name = "ripple.adb"
        self.__snapshot_name = "ripple.sdb"
        self.__persist_as = persist_as

    def aof_write(self, key, value, op):
        if self.__persist_as == persist_const.AOF:
            with open(self.__aof_name, "a") as write_desc:
                write_desc.write(f"{op}:{key}:{json.dumps(value)}\n")

    def find_aof(self):
        return os.path.exists(self.__aof_name)

    def aof_load(self, load_dict):
        with open(self.__aof_name, "r") as read_desc:
            for line in read_desc:
                line = line.strip("\n").split(self.__aof_separator, 2)
                # 0 - operator; 1 - key, 2 - value
                if line[0] == self.__write:
                    load_dict[line[1]] = json.loads(line[2])

                if line[0] == self.__delete:
                    del load_dict[line[1]]
        return load_dict

    def sync_db(self, data_dict):
        match self.__persist_as:
            case persist_const.NONE:
                return data_dict
            case persist_const.AOF:
                if self.find_aof():
                    data_dict = self.aof_load(data_dict)
                    return data_dict
            case persist_const.SNAPSHOT:
                # TO BE IMPLEMENTED
                pass

        return data_dict
