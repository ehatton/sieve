import click
from upfilter.fasta_parser import FastaParser


def filter_all(fasta_list, reviewed, minlen, maxlen, taxid, evidence):
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
@click.option("-r", "--reviewed", type=click.Choice(["yes", "no"]))
@click.option("-min", "--minlen", type=int)
@click.option("-max", "--maxlen", type=int)
@click.option("-t", "--taxid", multiple=True)
@click.option("-e", "--evidence", type=click.Choice(['1', '2', '3', '4', '5']), multiple=True)
def main(infile, outfile, reviewed, minlen, maxlen, taxid, evidence):
    """Entry point to program. Parses command line arguments and outputs filtered fasta sequences."""
    
    # Convert evidence list to int, since click only allows string types in click.Choice
    evidence = tuple(int(x) for x in evidence)

    # Generate, filter, and output the fasta list
    fasta_list = FastaParser(infile)
    filtered_fasta = filter_all(fasta_list, reviewed, minlen, maxlen, taxid, evidence)
    for f in filtered_fasta:
        outfile.write(f.format())


if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
