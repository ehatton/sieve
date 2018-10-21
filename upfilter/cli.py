import click
from upfilter.fasta_parser import FastaParser


def filter_all(fasta_list, reviewed, min, max, taxid, evidence):
    if reviewed == "yes":
        fasta_list = filter(lambda x: x.reviewed, fasta_list)
    elif reviewed == "no":
        fasta_list = filter(lambda x: not x.reviewed, fasta_list)

    if taxid is not None:
        fasta_list = filter(lambda x: x.taxid in taxid, fasta_list)
    if min is not None:
        fasta_list = filter(lambda x: len(x) >= min, fasta_list)
    if max is not None:
        fasta_list = filter(lambda x: len(x) <= max, fasta_list)
    if evidence is not None:
        fasta_list = filter(lambda x: x.evidence in evidence, fasta_list)

    return fasta_list


@click.command()
@click.argument("infile", type=click.File(mode="r"))
@click.argument("outfile", type=click.File(mode="w"))
@click.option("-r", "--reviewed", type=click.Choice(["yes", "no"]))
@click.option("--min", type=int)
@click.option("--max", type=int)
@click.option("-t", "--taxid", multiple=True)
@click.option("-e", "--evidence", type=click.Choice([1, 2, 3, 4, 5]), multiple=True)
def main(infile, outfile, reviewed, min, max, taxid, evidence):
    """Entry point to program. Parses command line arguments and outputs filtered fasta sequences."""
    fasta_list = FastaParser(infile)
    filtered_fasta = filter_all(fasta_list, reviewed, min, max, taxid, evidence)
    for f in filtered_fasta:
        outfile.write(f.format())
        