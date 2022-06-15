# eth-uniswap-prelim-analysis
Preliminary data analysis on Uniswap V3 on Ethereum.

## Project structure
```bash
.
├── analysis
│   ├── data                        # data generated during notebook run (gitignored)
│   └── chart_data.ipynb            # analysis of Uniswap V3 info page chart data
├── cookbook                        # useful code snippets written in notebooks
├── pyammanalysis                   # local python module
│   ├── __init__.py                 # make pyammanalysis a Python module
│   ├── config.py                   # configurations like external API URL
│   ├── graphql_helper.py           # wrapper around HTTP request.post to the subgraph URL
│   └── pwlf_helper.py              # wrapper around pwlf (Piecewise Linear Fit) package
├── .gitignore                      # ignore files that cannot be committed to Git
├── LICENSE.txt                     # MIT license file
├── poetry.lock                     # lock versions of dependencies managed by poetry
├── pyproject.toml                  # build system dependencies
└── README.md                       # this file
```

## Installing dependencies
```bash
poetry install
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