from yaml import safe_load


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return safe_load(f)
