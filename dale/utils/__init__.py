import os


class Index:
    def __init__(self, start=0, end=None):
        self.start = start
        self.end = end

    def __bool__(self):
        return all([self.start, self.end])


def read_file(path):
    with open(path, "r") as file_obj:
        return file_obj.read()


def read_environment(name, default=""):
    return os.environ.get(name, default)
