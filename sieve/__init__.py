"""Tools for reading and filtering UniProt fasta sequences."""
__version__ = "0.0.0"

# Give access to the Fasta and FastaParser classes from the top level of the package
from sieve.fasta import Fasta
from sieve.fasta_parser import FastaParser
from sieve.text_parser import parse_text
