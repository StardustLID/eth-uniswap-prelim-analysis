# from collections import defaultdict

# import numpy as np
# import pandas as pd

from pyammanalysis.subgraph import UNISWAP_V2_SUBGRAPH_URL

from . import base_scraper


class UniV2Scraper(base_scraper.BaseScraper):
    top_pairs_query = """
    {
        pairs(first: 1000, orderBy: reserveUSD, orderDirection: desc) {
            id,
            token0 {
                id
            },
            token1 {
                id
            },
            reserveUSD,
            token0Price,
            token1Price
        }
    }
    """
    """
    Queries the first 1000 `Pair` entities, ordered by decreasing `reserveUSD` (liquidity in USD).
    """

    top_tokens_query = """
    {
        tokens(first: 1000, orderBy: totalLiquidity, orderDirection: desc) {
            id
            symbol
            name
            totalLiquidity
        }
    }
    """
    """
    Queries the first 1000 `Token` entities, ordered by decreasing `totalLiquidity` (liquidity across all pairs).
    """

    def __init__(self, block_number) -> None:
        super().__init__(block_number)
        self.url = UNISWAP_V2_SUBGRAPH_URL

    def top_pairs(self):
        """
        Returns the top 1000 pairs by TVL from Uniswap V2 subgraph.
        The result is only fetched when this function is first called,
        afterwards the result is stored in `self._top_pairs`.
        """
        if self._top_pairs is None:
            pairs_list = self.scrape(UniV2Scraper.top_pairs_query)["data"]

            # flatten dict
            for pool_dict in pairs_list["pairs"]:
                for token in ["token0", "token1"]:
                    pool_dict[token] = pool_dict[token]["id"]

            self._top_pairs = pairs_list

        return self._top_pairs

    def top_tokens(self):
        """
        Returns the top 1000 tokens by TVL from Uniswap V2 subgraph.
        """
        if self._top_tokens is None:
            tokens_list = self.scrape(UniV2Scraper.top_tokens_query)["data"]
            self._top_tokens = tokens_list

        return self._top_tokens
