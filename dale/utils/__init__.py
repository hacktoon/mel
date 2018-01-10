import os


def read_file(path):
    with open(path, 'r') as file_obj:
        return file_obj.read()


def read_environment(name, default=''):
    return os.environ.get(name, default)
