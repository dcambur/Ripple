class RippleData:
    def __init__(self, name):
        self.name = name
        self.data = dict()

    def create(self, key, value):
        self.data[key] = value

    def read(self, key):
        if key not in self.data.keys():
            return None
        return self.data[key]

    def delete(self, key):
        if key not in self.data.keys():
            return None
        del self.data[key]
        return True
