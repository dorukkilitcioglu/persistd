import json


def save_dict_to_json(obj, path):
    """ Saves the dictionary object of an object to a json file
    """
    with open(path, 'w') as fp:
        json.dump(obj.__dict__, fp)


def load_dict_from_json(obj, path):
    """ Loads the dictionary object of an object from a json file
    """
    with open(path, 'r') as fp:
        obj.__dict__.update(json.load(fp))
