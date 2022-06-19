import numpy as np

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


def get_connected_pairs_from_ex():
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


if __name__ == "__main__":
    top_uniswapv3_pairs()
    top_uniswapv3_tokens()
