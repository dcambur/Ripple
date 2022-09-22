import os
import json


# json-based log file writing
class AppendFile:
    def __init__(self, filename, dest, write_mode=None):
        self.filename = filename
        self.dest = dest
        self.format = ".rplog"
        self.write_mode = write_mode
        self.full_path = f"{self.dest}{self.filename}{self.format}"

    def init_log(self):
        if not os.path.exists(self.dest):
            raise FileNotFoundError
        if not os.path.isfile(self.full_path):
            open(self.full_path, "w").close()

    def write_log(self, data):
        self.init_log()
        with open(self.full_path, "r") as file:
            if os.path.getsize(self.full_path):
                cur_json = json.load(file)
            else:
                cur_json = {}

        with open(self.full_path, "w") as file:
            for key, value in data.items():
                cur_json[key] = value
            json.dump(cur_json, file)

    def read_file(self):
        with open(self.full_path, "r") as file:
            json_data = json.load(file)
        return json_data
