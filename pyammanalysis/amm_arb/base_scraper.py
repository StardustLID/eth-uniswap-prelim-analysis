import pandas as pd

from pyammanalysis.subgraph import run_query


class BaseScraper:
    """
    BaseScraper object is instantiated given a block number, i.e. each object
    stores the snapshot of all fetched pairs and tokens in the corresponding block.
    """

    url: str
    block_number: int
    _top_pairs: list
    _top_tokens: list
    _adj_matrix: pd.DataFrame

    def __init__(self, block_number) -> None:
        self.block_number = block_number
        self._top_pairs = None
        self._top_tokens = None
        self._adj_matrix = None

    def scrape(self, query: str):
        return run_query(self.url, query)
