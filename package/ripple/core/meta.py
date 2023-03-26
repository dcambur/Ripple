class OperatorTypes:
    WRITE = "+"
    DELETE = "-"


class BackupTypes:
    NONE = "NONE"
    AOF = "AOF"
    SNAPSHOT = "SNAPSHOT"


class BackupInfo:
    def __init__(self, model_type=None, save_every=None):
        self.model_type = model_type
        self.save_every = save_every


class NONEInfo(BackupInfo):
    __MODEL_TYPE = BackupTypes.NONE

    def __init__(self):
        super().__init__(self.__MODEL_TYPE)


class AOFInfo(BackupInfo):
    __MODEL_TYPE = BackupTypes.AOF
    DATA_SEPARATOR = ":"
    LINE_SEPARATOR = "\n"
    __FORMAT = ".adb"

    def __init__(self, path, name, save_every=10):
        super().__init__(self.__MODEL_TYPE, save_every)
        self.full_path = path + name + self.__FORMAT
        # TO DO: Implement save_every (in seconds/minutes/etc) in next versions


class SnapshotInfo(BackupInfo):
    __MODEL_TYPE = BackupTypes.SNAPSHOT
    __FORMAT = ".sdb"

    def __init__(self, path, name, save_every=100):
        super().__init__(self.__MODEL_TYPE, save_every)
        self.full_path = path + name + self.__FORMAT
