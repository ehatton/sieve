import click
from upfilter.fasta_parser import FastaParser


# Define help strings for the various options
FILTER_HELP = "Filter by reviewed (SwissProt) or unreviewed (TrEMBL) sequences."
MINLEN_HELP = "Filter by minimun sequence length."
MAXLEN_HELP = "Filter by maxinum sequence length."
TAXID_HELP = 'Filter by NCBI taxonomy ID. You can have multiple taxids e.g. "-t 9606 -t 10090" \
will select both human and mouse sequences.'
GENE_HELP = 'Filter by gene name. Names are case sensitive. You can have multiple gene names e.g.\
 \"-g Shld1 -g SHLD1\".'
EVIDENCE_HELP = 'Filter by protein evidence level. You can have multiple evidence levels e.g. \
"-e 1 -e 2 -e 3" to select evidence levels in the range of 1-3.'


def filter_all(
    fasta_list=None, reviewed=None, minlen=None, maxlen=None, taxid=(), gene=(), evidence=()
):
    """Accepts a list of fasta objects and optional filtering parameters.
    Returns a filtered list of fasta objects."""
    if reviewed == "yes":
        fasta_list = filter(lambda x: x.reviewed, fasta_list)
    elif reviewed == "no":
        fasta_list = filter(lambda x: not x.reviewed, fasta_list)

    if len(taxid) is not 0:
        fasta_list = filter(lambda x: x.taxid in taxid, fasta_list)
    if minlen is not None:
        fasta_list = filter(lambda x: len(x) >= minlen, fasta_list)
    if maxlen is not None:
        fasta_list = filter(lambda x: len(x) <= maxlen, fasta_list)
    if len(gene) is not 0:
        fasta_list = filter(lambda x: x.gene in gene, fasta_list)
    if len(evidence) is not 0:
        fasta_list = filter(lambda x: x.evidence in evidence, fasta_list)

    return fasta_list


@click.command()
@click.argument("infile", type=click.File(mode="r"))
@click.argument("outfile", type=click.File(mode="w"))
@click.option("-r", "--reviewed", type=click.Choice(["yes", "no"]), help=FILTER_HELP)
@click.option("-min", "--minlen", type=int, help=MINLEN_HELP)
@click.option("-max", "--maxlen", type=int, help=MAXLEN_HELP)
@click.option("-t", "--taxid", multiple=True, help=TAXID_HELP)
@click.option("-g", '--gene', multiple=True, help=GENE_HELP)
@click.option(
    "-e",
    "--evidence",
    type=click.Choice(["1", "2", "3", "4", "5"]),
    multiple=True,
    help=EVIDENCE_HELP,
)
def main(infile, outfile, reviewed, minlen, maxlen, taxid, gene, evidence):
    """Reads in file containing UniProt fasta sequences.
    Filters the sequences depending on selected options."""

    # Convert evidence list to int, since click only allows string types in click.Choice
    evidence = tuple(int(x) for x in evidence)

    # Generate, filter, and output the fasta list
    fasta_list = FastaParser(infile)
    filtered_fasta = filter_all(fasta_list, reviewed, minlen, maxlen, taxid, gene, evidence)
    for f in filtered_fasta:
        outfile.write(f.format())
