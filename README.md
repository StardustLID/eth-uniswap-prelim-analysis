# eth-uniswap-prelim-analysis
Preliminary data analysis on Uniswap V3 on Ethereum.

<!-- buttons -->
[![python](https://img.shields.io/badge/python-v3-brightgreen.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Project structure
```bash
.
├── analysis
│   ├── data                        # data (gitignored, content omitted)
│   ├── 1-DataCollection.ipynb      # fetch data from subgraph and parse as DataFrames
│   ├── 2-TokenVolumeAnalysis.ipynb # analysis of token trading volume
│   ├── 3-PoolVolumeAnalysis.ipynb  # analysis of pool trading volume
│   └── 4-PoolTvlAnalysis.ipynb     # analysis of pool TVL
├── cookbook                        # useful code snippets written in notebooks
│   ├── data                        # data (gitignored, content omitted)
│   ├── subgraph_examples.ipynb     # implementation of Uniswap V3 subgraph tutorial
│   └── vertex_degrees.ipynb        # analysis of connectedness of Uniswap V3 tokens
├── pyammanalysis                   # local python module
│   ├── amm_arb                     # sub-module for AMM arbitrage
│   │   ├── __init__.py
│   │   ├── graph_arbitrage.py      # variant of Bellman-Ford algorithm to find arbitrage
│   │   └── uniswapv3_scraper.py    # scrape token pairs and produce adjacency list
│   ├── __init__.py
│   ├── subgraph.py                 # subgraph helper functions
│   ├── pwlf_helper.py              # wrapper around pwlf (Piecewise Linear Fit) package
│   └── util.py                     # configurations like external API URL
├── .flake8                         # `flake8` Python style enforcement config file
├── .gitignore                      # ignore files that cannot be committed to Git
├── .pre-commit-config.yaml         # `pre-commit` hook config file
├── config.yaml                     # configs like whitelisted tokens
├── LICENSE.txt                     # MIT license file
├── poetry.lock                     # lock versions of dependencies managed by poetry
├── pyproject.toml                  # build system dependencies
└── README.md                       # this file
```

## Installing dependencies
```bash
poetry install
```
Note: The remaining commands assume you are in a poetry shell. If you aren't, follow the instructions in the section [Activating the virtual environment](#activating-the-virtual-environment).

After setting up `poetry`, install the `pre-commit` hook:
```bash
pre-commit install
```

You can optionally run the pre-commit hook manually:
```bash
pre-commit run --all-files
```

## Activating the virtual environment
```bash
poetry shell
```
Note: If you use VSCode, you may need to [manually set the interpreter for the project](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter) for reading Python scripts and Jupyter notebooks.

Exit/deactivate:
```bash
exit
```
