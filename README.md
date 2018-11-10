# upfilter

A little bioinformatics command line tool, for filtering and extracting UniProt FASTA sequences from a file. 


## Installation

Download the latest wheel file from the releases tab and then install with the following pip command:

```bash
pip install 
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
