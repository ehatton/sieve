from functools import partial
from typing import Iterable, Optional, Tuple

import click
from sieve import parse_fasta, parse_text
from sieve.fasta import Fasta
from sieve.fasta_parser import FastaParserError
from sieve.text_parser import TextParserError

# Define help strings for the various options
REVIEWED_HELP = "Filter by reviewed (SwissProt) or unreviewed (TrEMBL) sequences."
ACCESSION_HELP = 'Filter by accession number(s). You can have multiple accessions e.g. "-a P11111\
 -a P22222".'
MINLEN_HELP = "Filter by minimun sequence length."
MAXLEN_HELP = "Filter by maxinum sequence length."
TAXID_HELP = 'Filter by NCBI taxonomy ID. You can have multiple taxids e.g. "-t 9606 -t 10090" \
will select both human and mouse sequences.'
GENE_HELP = 'Filter by gene name. Names are case sensitive. You can have multiple gene names e.g.\
 "-g Shld1 -g SHLD1".'
EVIDENCE_HELP = 'Filter by protein evidence level. You can have multiple evidence levels e.g. \
"-e 1 -e 2 -e 3" to select evidence levels 1-3.'


@click.command()
@click.argument("infile", type=click.File(mode="r"))
@click.argument("outfile", type=click.File(mode="w"))
@click.option("-r", "--reviewed", type=click.Choice(["yes", "no"]), help=REVIEWED_HELP)
@click.option("-a", "--accession", multiple=True, help=ACCESSION_HELP)
@click.option("-min", "--minlen", type=int, help=MINLEN_HELP)
@click.option("-max", "--maxlen", type=int, help=MAXLEN_HELP)
@click.option("-t", "--taxid", multiple=True, help=TAXID_HELP)
@click.option("-g", "--gene", multiple=True, help=GENE_HELP)
@click.option(
    "-e",
    "--evidence",
    type=click.Choice(["1", "2", "3", "4", "5"]),
    multiple=True,
    help=EVIDENCE_HELP,
)
def main(infile, outfile, reviewed, accession, minlen, maxlen, taxid, gene, evidence):
    """Reads in a file containing UniProt fasta sequences. Also accepts UniProt
    text format files as input. Filters the sequences depending on selected
    options. Outputs fasta sequences (regardless of input format).
    
    Required positional arguments are INFILE and OUTFILE, which should point
    to valid filenames. To use stdin and/or stdout instead, pass \"-\" as the
    argument.
    """

    # Convert evidence list to int, since click only allows string types for click.Choice type
    evidence = tuple(int(x) for x in evidence)

    # Set values for filtering function
    filter_by_parameter = partial(
        _filter_by_parameter,
        reviewed=reviewed,
        accession=accession,
        minlen=minlen,
        maxlen=maxlen,
        taxid=taxid,
        gene=gene,
        evidence=evidence,
    )

    # Try fasta and text parsers, otherwise display an error message to the user
    try:
        for fasta in filter_by_parameter(parse_fasta(infile)):
            outfile.write(fasta.format())
    except FastaParserError:
        try:
            for fasta in filter_by_parameter(parse_text(infile)):
                outfile.write(fasta.format())
        except TextParserError:
            raise click.ClickException(
                "Invalid file format. File must be either FASTA or UniProt text format."
            )


def _filter_by_parameter(
    fasta: Iterable[Fasta],
    reviewed: Optional[str] = None,
    accession: Tuple[str, ...] = (),
    minlen: Optional[int] = None,
    maxlen: Optional[int] = None,
    taxid: Tuple[str, ...] = (),
    gene: Tuple[str, ...] = (),
    evidence: Tuple[int, ...] = (),
) -> Iterable[Fasta]:
    """Filters an iterable of Fasta objects based on optional parameters.

    Args:
        fasta: iterable of Fasta objects.
        reviewed: expected value is either 'yes' or 'no'. Defaults to None.
        accession: tuple of UniProt accessions. Defaults to ().
        minlen: minimum sequence length. Defaults to None.
        maxlen: maximum sequence length. Defaults to None.
        taxid: tuple of NCBI taxonomy IDs. Defaults to ().
        gene: tuple of gene names. Defaults to ().
        evidence: tuple of evidence levels (expected values in range 1-5). Defaults to ().

    Returns:
        Iterable[Fasta]: iterable of filtered Fasta objects.
    """

    if reviewed == "yes":
        fasta = filter(lambda x: x.reviewed, fasta)
    elif reviewed == "no":
        fasta = filter(lambda x: not x.reviewed, fasta)

    if len(accession) is not 0:
        fasta = filter(lambda x: x.accession in accession, fasta)
    if len(taxid) is not 0:
        fasta = filter(lambda x: x.taxid in taxid, fasta)
    if minlen is not None:
        fasta = filter(lambda x: len(x) >= minlen, fasta)
    if maxlen is not None:
        fasta = filter(lambda x: len(x) <= maxlen, fasta)
    if len(gene) is not 0:
        fasta = filter(lambda x: x.gene in gene, fasta)
    if len(evidence) is not 0:
        fasta = filter(lambda x: x.evidence in evidence, fasta)

    return fasta
