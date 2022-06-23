from collections import defaultdict

import numpy as np
import pandas as pd

from pyammanalysis.subgraph import UNISWAP_V3_SUBGRAPH_URL

from . import base_scraper


class UniV3Scraper(base_scraper.BaseScraper):
    top_pools_query = """
    {
        pools(first: 1000, orderBy: totalValueLockedUSD, orderDirection: desc) {
            id,
            token0 {
                id
            },
            token1 {
                id
            },
            feeTier,
            liquidity,
            token0Price,
            token1Price
        }
    }
    """
    """
    Queries the first 1000 `Pool` entities, ordered by decreasing `totalValueLockedUSD`.
    """

    top_tokens_query = """
    {
        tokens(first: 1000, orderBy: totalValueLockedUSD, orderDirection: desc) {
            id
            symbol
            name
            totalValueLockedUSD
        }
    }
    """
    """
    Queries the first 1000 `Token` entities, ordered by decreasing `totalValueLockedUSD`.
    """

    def __init__(self, block_number) -> None:
        super().__init__(block_number)
        self.url = UNISWAP_V3_SUBGRAPH_URL

    @staticmethod
    def flatten_pools_for_tokens(pools_list: list, key: str = "symbol") -> list:
        tokens = []
        for pair_dict in pools_list:
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
                    pool {
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
                    amount0
                    amount1
                }
            }
        }
        """
        transaction = self.scrape(tx_query)["transaction"]
        pools = [x["pool"] for x in transaction["swaps"]]
        tokenIds = (list(set(UniV3Scraper.flatten_pools_for_tokens(pools, "id"))),)
        tokenSymbols = list(set(UniV3Scraper.flatten_pools_for_tokens(pools, "symbol")))

        # flatten dict
        for pool_dict in pools:
            for token in ["token0", "token1"]:
                pool_dict[token] = pool_dict[token][token_key]

        return {
            "transaction": transaction,
            "pools": pools,
            "poolIds": [x["id"] for x in pools],
            "tokenIds": tokenIds,
            "tokenSymbols": tokenSymbols,
        }

    def top_pairs(self):
        """
        Returns the top 1000 pairs by TVL from Uniswap V3 subgraph.
        The result is only fetched when this function is first called,
        afterwards the result is stored in `self._top_pairs`.
        """
        if self._top_pairs is None:
            pairs_list = self.scrape(UniV3Scraper.top_pools_query)

            # flatten dict
            for pool_dict in pairs_list["pools"]:
                for token in ["token0", "token1"]:
                    pool_dict[token] = pool_dict[token]["id"]

            self._top_pairs = pairs_list

        return self._top_pairs

    def top_tokens(self):
        """
        Returns the top 1000 tokens by TVL from Uniswap V3 subgraph.
        """
        if self._top_tokens is None:
            tokens_list = self.scrape(UniV3Scraper.top_tokens_query)
            self._top_tokens = tokens_list

        return self._top_tokens

    def get_connected_tokens(self, min_degree: int = 3):
        """
        Loads the pairs from Uniswap V3 that have 3 or more connections

        :return: 'connected' pairs, e.g {USDT:[BTC,ETH], ETH:[ADA, OMG]}
        :rtype: {str : str list} dict
        """
        pairs = self.top_pairs()

        flattened_tokens_in_pools = np.concatenate(
            [[x["token0"], x["token1"]] for x in pairs]
        )
        unique, counts = np.unique(flattened_tokens_in_pools, return_counts=True)
        token_count = dict(zip(unique, counts))

        return {k: v for k, v in token_count.items() if len(v) >= min_degree}

    def create_adj_matrix(self, outfile="adjacency_matrix.csv"):
        if self._adj_matrix is None:
            # fetch list of top token names
            top_tokens_dicts = self.top_tokens()["tokens"]
            addr2name_dict = defaultdict(
                lambda: "oof", {x["id"]: x["name"] for x in top_tokens_dicts}
            )
            top_100_tokens = list(map(lambda x: x["id"], top_tokens_dicts[:100]))

            # create empty df
            df = pd.DataFrame(
                columns=top_100_tokens, index=top_100_tokens, dtype=np.float64
            )

            # TODO: consider multi-paths for the same pairs
            # fill in the adjacency matrix
            for pool in self.top_pairs()["pools"]:
                token0 = pool["token0"]
                token1 = pool["token1"]
                if token0 in top_100_tokens and token1 in top_100_tokens:
                    # indexing allows chaining: df[a][b] * df[b][c] = df[a][c]
                    df[token0][token1] = pool["token1Price"]
                    df[token1][token0] = pool["token0Price"]

            # map addr to name in the final step
            # DON'T use symbol - there are different wrappers for the same coin
            # E.g. USDC, wormhole wrapped USDC, wormhole (POS) USDC...
            df = df.rename(index=addr2name_dict).rename(columns=addr2name_dict)

            df.to_csv(outfile)
            self._adj_matrix = df

        return self._adj_matrix
