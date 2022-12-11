from ripple.core import persist_const


class RipplePersist:
    def __init__(self, persist_as):
        self.__aof_separator = ":"
        self.__write = "+"
        self.__delete = "-"
        self.__aof_name = "ripple.adb"
        self.__snapshot_name = "ripple.sdb"
        self.__persist_as = persist_as

    def aof_write(self, key, value, op):
        with open(self.__aof_name, "a") as write_desc:
            write_desc.write(f"{op}:{key}:{value}")

    def aof_load(self, load_dict):
        with open(self.__aof_name, "r") as read_desc:
            for line in read_desc:
                line.split(self.__aof_separator)

                # 0 - operator; 1 - key, 2 - value
                if line[0] == self.__write:
                    load_dict[line[1]] = line[2]

                if line[0] == self.__delete:
                    del load_dict[line[1]]

    def init(self):
        pass
