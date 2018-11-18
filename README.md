# sieve

A little bioinformatics command line tool, for filtering and extracting [UniProt](https://www.uniprot.org) FASTA sequences from a file.

For more information about the UniProt FASTA format, take a look at the official [UniProt guide.](https://www.uniprot.org/help/fasta-headers)

## Quickstart

Run the following command to view all the available filtering options:
```bash
sieve --help
```

## Installation

Download the latest wheel file from the releases tab and then install with the following pip command:

```bash
pip install upfilter-1.0.0-py3-none-any.whl 
```

## Usage examples
Filter for human sequences (taxonomy id 9606):

```bash
sieve uniprot.fasta out.fasta -t 9606
```

Filter for human sequences with a maximum length of 100:

```bash
sieve uniprot.fasta out.fasta -t 9606 -max 100
```

Filter for human sequences with a length between 50 and 100:

```bash
sieve uniprot.fasta out.fasta -t 9606 -min 50 -max 100
```

Filter for sequences with gene name BRCA1 or BRCA1, reading from stdin and writing to stdout:
```bash
sieve - - -g BRCA1 -g BRCA2 < uniprot.fasta > out.fasta
```

Convert UniProt text format (flatfile) to FASTA format:
```bash
sieve uniprot.txt uniprot.fasta
```

Get help:
```bash
sieve --help
```

The FastaParser class (for UniProt FASTA files) or text_parser function (for UniProt text files) can also be used in your own python scripts:

```python
from sieve import FastaParser

with open("my_proteins.fasta", "r") as infile:
    for protein in FastaParser(infile):
        print(protein) # or do your custom filtering here

```

## Requirements
python verson 3.6 or above.

May also work with earlier versions of python 3 but this has not been tested.

## Built with
- [click](https://click.palletsprojects.com/en/7.x/)
- [flit](https://github.com/takluyver/flit)

## Development setup

unittest is used for the test suite. To run tests:

```sh
python -m unittest discover 
```

## Release History

* 1.0.0
    * First release

## Author

Emma Hatton-Ellis – ehattonellis@gmail.com

## License

Distributed under the MIT license. See ``LICENSE`` for more information.
