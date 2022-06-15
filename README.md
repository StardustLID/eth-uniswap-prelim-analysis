# eth-uniswap-prelim-analysis
Preliminary data analysis on Uniswap V3 on Ethereum.

<!-- buttons -->
[![python](https://img.shields.io/badge/python-v3-brightgreen.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
