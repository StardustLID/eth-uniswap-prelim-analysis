import os

from yaml import safe_load

DATA_PATH = "data"
"""
Relative path to the `data` folder from the current program's parent directory.
"""

DATA_TOKEN_DAY_PATH = os.path.join(DATA_PATH, "token", "day")
"""
Relative path to the `data/token/day` folder from the current program's parent directory.
"""

DATA_POOL_DAY_PATH = os.path.join(DATA_PATH, "pool", "day")
"""
Relative path to the `data/pool/day` folder from the current program's parent directory.
"""

SUBPLOTS_PER_ROW = 3
SUBPLOT_WIDTH = 8
SUBPLOT_HEIGHT = 5
PLOT_WIDTH = SUBPLOTS_PER_ROW * SUBPLOT_WIDTH

START_TIMESTAMP = 1619170975
"""
Starting timestamp for day-based token and pool time series.
Represents GMT: Friday, April 23, 2021 9:42:55 AM.
"""

UNISWAP_V3_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
"""
Subgraph URL of Uniswap V3. Can be queried with GraphQL queries via HTTP POST method.
In Python, this can be achieved by `requests` HTTP library, or the `gql` GraphQL library.
"""


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return safe_load(f)
