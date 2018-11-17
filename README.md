# upfilter

A little bioinformatics command line tool, for filtering and extracting UniProt FASTA sequences from a file.


## Quickstart

Run the following command to view the available filtering options:
```upfilter --help```


## Installation

Download the latest wheel file from the releases tab and then install with the following pip command:

```bash
pip install upfilter-0.0.0-py3-none-any.whl 
```

## Usage examples
Filter for sequences  

Get help
```bash
upfilter --help
```

The FastaParser class can also be imported for use in your own python scripts.

```python
from upfilter import FastaParser

with open("my_proteins.fasta", "r") as infile:
    for protein in FastaParser(infile):
        print(protein.accession)

```

## Requirements
python verson 3.6 or above.

May also work with earlier versions of python 3 but this has not been tested.

## Built with
- [click](https://click.palletsprojects.com/en/7.x/)

## Development setup

unittest is used for the test suite. To run tests:

```sh
python -m unittest discover 
```

## Release History

* 0.0.0
    * First release


## Author

Emma Hatton-Ellis – ehattonellis@gmail.com

## License

Distributed under the MIT license. See ``LICENSE`` for more information.
