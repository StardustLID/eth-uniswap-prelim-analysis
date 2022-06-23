"""
The `amm_arb` module is inspired by Robert Andrew Martin's [CryptoGraphArb](https://github.com/robertmartin8/CryptoGraphArb) project, which uses graph theory to discover arbitrage opportunities in a cryptocurrency market via the [CryptoCompare](https://min-api.cryptocompare.com/) API.

This module adapts it such that prices are read from Uniswap V3 subgraph directly.
Other DEX may be added in the future.
"""

from .uniswapv2_scraper import UniV2Scraper
from .uniswapv3_scraper import UniV3Scraper

__all__ = [
    "UniV2Scraper",
    "UniV3Scraper",
]
