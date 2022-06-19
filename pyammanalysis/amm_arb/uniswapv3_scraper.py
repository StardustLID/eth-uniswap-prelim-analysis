import numpy as np
import pandas as pd

from pyammanalysis.graphql_helper import run_query

# from tqdm import tqdm


UNISWAP_V3_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"


def top_uniswapv3_pairs():
    """
    Returns the top 1000 pairs by TVL from Uniswap V3 subgraph.
    """
    top_tvl_pools_query = """
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
    pairs_list = run_query(UNISWAP_V3_SUBGRAPH_URL, top_tvl_pools_query)["data"]

    # flatten dict
    for pool_dict in pairs_list["pools"]:
        for token in ["token0", "token1"]:
            pool_dict[token] = pool_dict[token]["id"]

    return pairs_list


def top_uniswapv3_tokens():
    """
    Returns the top 1000 tokens by TVL from Uniswap V3 subgraph.
    """
    top_tvl_tokens_query = """
    {
        tokens(first: 1000, orderBy: totalValueLockedUSD, orderDirection: desc) {
            id
            symbol
            totalValueLockedUSD
        }
    }
    """
    tokens_list = run_query(UNISWAP_V3_SUBGRAPH_URL, top_tvl_tokens_query)["data"]
    return tokens_list


def get_connected_tokens():
    """
    Loads the pairs from Uniswap V3 that have 3 or more connections

    :return: 'connected' pairs, e.g {USDT:[BTC,ETH], ETH:[ADA, OMG]}
    :rtype: {str : str list} dict
    """
    pairs = top_uniswapv3_pairs()

    flattened_tokens_in_pools = np.concatenate(
        [[x["token0"], x["token1"]] for x in pairs]
    )
    unique, counts = np.unique(flattened_tokens_in_pools, return_counts=True)
    token_count = dict(zip(unique, counts))

    return {k: v for k, v in token_count.items() if len(v) >= 3}


def create_adj_matrix(outfile="adjacency_matrix.csv"):
    # fetch list of top token symbols
    top_100_tokens_dicts = top_uniswapv3_tokens()["tokens"][:100]
    addr2sym_dict = {token["id"]: token["symbol"] for token in top_100_tokens_dicts}
    top_100_tokens = list(map(lambda x: x["id"], top_100_tokens_dicts))

    # create empty df
    df = pd.DataFrame(columns=top_100_tokens, index=top_100_tokens, dtype=np.float64)

    # TODO: consider multi-paths for the same pairs
    # fill in the adjacency matrix
    for pool in top_uniswapv3_pairs()["pools"]:
        token0 = pool["token0"]
        token1 = pool["token1"]
        if token0 in top_100_tokens and token1 in top_100_tokens:
            # indexing allows chaining: df[a][b] * df[b][c] = df[a][c]
            df[token0][token1] = pool["token1Price"]
            df[token1][token0] = pool["token0Price"]

    # map addr to symbol in the final step
    df = df.rename(index=addr2sym_dict).rename(columns=addr2sym_dict)

    df.to_csv(outfile)
    return df


if __name__ == "__main__":
    top_uniswapv3_pairs()
    top_uniswapv3_tokens()
