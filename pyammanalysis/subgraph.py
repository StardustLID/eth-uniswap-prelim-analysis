"""
The `subgraph` module provides constants and functions for interacting with
the subgraphs of different DeFi protocols.

A subgraph can be queried with GraphQL queries via HTTP POST method.
In Python, this can be achieved by `requests` HTTP library, or the `gql` GraphQL library.
"""
import requests

SUSHISWAP_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"
"""
Subgraph URL of Sushiswap.
Schema at https://github.com/sushiswap/sushiswap-subgraph.
"""

UNISWAP_V2_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
"""
Subgraph URL of Uniswap V2. Note that the schema is considerably different from V3.
Schema at https://github.com/Uniswap/v2-subgraph/blob/master/schema.graphql.
"""

UNISWAP_V3_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
"""
Subgraph URL of Uniswap V3. Note that the schema is considerably different from V2.
Schema at https://github.com/Uniswap/v3-subgraph/blob/main/schema.graphql.
"""


def run_query(url: str, query):
    """
    Use ``requests.post`` to make an API call to the subgraph URL
    """
    # endpoint where you are making the request
    request = requests.post(url, "", json={"query": query})
    if request.status_code == 200:
        try:
            return request.json()["data"]
        except Exception:
            raise Exception(request.json())
    else:
        raise Exception(
            f"Query failed. Return code is {request.status_code}.      {query}"
        )
