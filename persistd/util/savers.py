import json
import os
from shutil import copyfile


def make_dirs(path):
    dest_dir = os.path.dirname(path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    return True


def save_dict_to_json(obj, path, excluded_keys=[]):
    """ Saves the dictionary object of an object to a json file

    Optionally excludes the given keys
    """
    make_dirs(path)
    persisted_dict = {key: value for key, value in obj.__dict__.items() if key not in excluded_keys}
    with open(path, 'w') as fp:
        json.dump(persisted_dict, fp)


def load_dict_from_json(obj, path):
    """ Loads the dictionary object of an object from a json file
    """
    with open(path, 'r') as fp:
        obj.__dict__.update(json.load(fp))


def copy_file(src, dest):
    """ Copies a file from source to destination, while creating
    the intermediate folders.
    """
    make_dirs(dest)
    copyfile(src, dest)
    return True
