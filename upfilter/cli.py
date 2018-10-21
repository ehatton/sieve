import click
from upfilter.fasta_parser import FastaParser


def filter_all(
    fasta_list=None, reviewed=None, minlen=None, maxlen=None, taxid=(), evidence=()
):
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
    if len(evidence) is not 0:
        fasta_list = filter(lambda x: x.evidence in evidence, fasta_list)

    return fasta_list


@click.command()
@click.argument("infile", type=click.File(mode="r"))
@click.argument("outfile", type=click.File(mode="w"))
@click.option(
    "-r",
    "--reviewed",
    type=click.Choice(["yes", "no"]),
    help="Filter by reviewed (SwissProt) or unreviewed (TrEMBL) sequences.",
)
@click.option("-min", "--minlen", type=int, help="Filter by minimun sequence length.")
@click.option("-max", "--maxlen", type=int, help="Filter by maxinum sequence length.")
@click.option(
    "-t",
    "--taxid",
    multiple=True,
    help="Filter by NCBI taxonomy ID. You can have multiple taxids e.g. \"-t 9606 -t 10090\" will \
select both human and mouse sequences.",
)
@click.option(
    "-e",
    "--evidence",
    type=click.Choice(["1", "2", "3", "4", "5"]),
    multiple=True,
    help="Filter by protein evidence level. You can have multiple evidence levels e.g. \"-e 1 -e\
 2 -e 3\" to select evidence levels in the range of 1-3.",
)
def main(infile, outfile, reviewed, minlen, maxlen, taxid, evidence):
    """Reads in file containing UniProt fasta sequences.
    Filters the sequences depending on selected options."""

    # Convert evidence list to int, since click only allows string types in click.Choice
    evidence = tuple(int(x) for x in evidence)

    # Generate, filter, and output the fasta list
    fasta_list = FastaParser(infile)
    filtered_fasta = filter_all(fasta_list, reviewed, minlen, maxlen, taxid, evidence)
    for f in filtered_fasta:
        outfile.write(f.format())
