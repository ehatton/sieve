"""Tools for reading and filtering UniProt fasta sequences."""
__version__ = "1.0.0"

# Give access to the Fasta and FastaParser classes from the top level of the package
from .fasta import Fasta
from .fasta_parser import FastaParser
from .text_parser import text_parser
