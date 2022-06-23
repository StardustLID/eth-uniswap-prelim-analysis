from typing import Union

import numpy as np
import pandas as pd

from pyammanalysis.subgraph import UNISWAP_V2_SUBGRAPH_URL

from . import base_scraper


class UniV2Scraper(base_scraper.BaseScraper):
    top_pairs_query = """
    {
        pairs(first: 1000, orderBy: trackedReserveETH, orderDirection: desc, block: {number: 14931986}) {
            id,
            token0 {
                id
            },
            token1 {
                id
            },
            trackedReserveETH,
            token0Price,
            token1Price
        }
    }
    """
    """
    Queries the first 1000 `Pair` entities, ordered by decreasing `trackedReserveETH`.
    """

    top_tokens_query = """
    {
        tokens(first: 1000, orderBy: totalLiquidity, orderDirection: desc, block: {number: 14931986}) {
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

    @staticmethod
    def flatten_pairs_for_tokens(pairs_list: list, key: str = "symbol") -> list:
        tokens = []
        for pair_dict in pairs_list:
            for token in ["token0", "token1"]:
                tokens.append(pair_dict[token][key])
        return tokens

    def tx_query(self, token_key: str = "symbol"):
        """
        Returns tx, list of pools and tokens involved given a tx hash.
        """
        tx_query = """
        {
            transaction(id: "0xe976f2ebd70135153e8522c3aaa3c9d489717ef621d69b9e00a9f215d0474918") {
                blockNumber
                timestamp
                swaps {
                    pair {
                        id
                        token0 {
                            id
                            symbol
                        }
                        token1 {
                            id
                            symbol
                        }
                        token0Price
                        token1Price
                    }
                    amount0In
                    amount1In
                    amount0Out
                    amount1Out
                }
            }
        }
        """
        transaction = self.scrape(tx_query)["data"]["transaction"]
        pairs = [x["pair"] for x in transaction["swaps"]]
        tokenIds = (list(set(UniV2Scraper.flatten_pairs_for_tokens(pairs, "id"))),)
        tokenSymbols = list(set(UniV2Scraper.flatten_pairs_for_tokens(pairs, "symbol")))

        # flatten dict
        for pool_dict in pairs:
            for token in ["token0", "token1"]:
                pool_dict[token] = pool_dict[token][token_key]

        return {
            "transaction": transaction,
            "pairs": pairs,
            "pairIds": [x["id"] for x in pairs],
            "tokenIds": tokenIds,
            "tokenSymbols": tokenSymbols,
        }

    def top_pairs(self, key: str = "symbol"):
        """
        Returns the top 1000 pairs by `trackedReserveETH` from Uniswap V2 subgraph.
        The result is only fetched when this function is first called,
        afterwards the result is stored in `self._top_pairs`.
        """
        if self._top_pairs is None:
            pairs_list = self.scrape(UniV2Scraper.top_pairs_query)["data"]

            # flatten dict
            for pool_dict in pairs_list["pairs"]:
                for token in ["token0", "token1"]:
                    pool_dict[token] = pool_dict[token][key]

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

    def create_adj_matrix(
        self,
        outfile="univ2_adj_matrix.csv",
        pairs: Union[list, None] = None,
        tokens: Union[list, None] = None,
    ):
        """
        `pairs`: list of pair dicts
        `tokens`: list of token symbols
        """
        if self._adj_matrix is None:
            # fetch top tokens if none is given
            if tokens is None:
                top_tokens_dicts = self.top_tokens()["tokens"]
                tokens = list(map(lambda x: x["symbol"], top_tokens_dicts[:100]))

            # create empty df
            df = pd.DataFrame(columns=tokens, index=tokens, dtype=np.float64)

            # fetch top pairs if none is given
            if pairs is None:
                pairs = self.top_pairs()["pairs"]

            # fill in the adjacency matrix
            for pair in pairs:
                token0 = pair["token0"]
                token1 = pair["token1"]
                if token0 in tokens and token1 in tokens:
                    # indexing allows chaining: df[a][b] * df[b][c] = df[a][c]
                    df[token0][token1] = pair["token1Price"]
                    df[token1][token0] = pair["token0Price"]

            # map addr to name in the final step
            # DON'T use symbol - there are different wrappers for the same coin
            # E.g. USDC, wormhole wrapped USDC, wormhole (POS) USDC...
            # df = df.rename(index=addr2name_dict).rename(columns=addr2name_dict)

            df.to_csv(outfile)
            self._adj_matrix = df

        return self._adj_matrix
