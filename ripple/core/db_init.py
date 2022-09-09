import os


class RippleInit:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.extension = "rpdb"
        self.full_path = f"{self.path}\\{self.name}.{self.extension}"

    def create_storage(self):
        if not os.path.exists(self.full_path):
            if not os.path.exists(self.path):
                raise FileNotFoundError
            open(self.full_path, "x").close()

    def open_read(self):
        return open(self.full_path, "r")

    def open_write(self):
        return open(self.full_path, "w")
