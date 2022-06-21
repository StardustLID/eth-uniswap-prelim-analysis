from yaml import safe_load

DATA_PATH = "data"

SUBPLOTS_PER_ROW = 3
SUBPLOT_WIDTH = 8
SUBPLOT_HEIGHT = 5
PLOT_WIDTH = SUBPLOTS_PER_ROW * SUBPLOT_WIDTH


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return safe_load(f)
