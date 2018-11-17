import click
from sieve import FastaParser, text_parser


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


def check_format(infile):
    """Accepts a filehandle as input. 
    
    Reads the first line of the file and checks to see if it looks like a
    UniProt fasta file or a UniProt text file.

    Returns the string 'fasta' or 'text' depending of the file format detected.

    Raises ValueError if no valid file format is detected."""

    filetype = None
    # Check the first line of the file
    line = infile.readline()
    if line.startswith((">sp", ">tr")):
        filetype = "fasta"
    elif line.startswith("ID   "):
        filetype = "text"
    else:
        raise ValueError(
            "sieve requires either a UniProt fasta file or UniProt text file as input."
        )
    # Return file pointer to start of file
    infile.seek(0)
    return filetype


def filter_all(
    fasta_list=None,
    reviewed=None,
    accession=(),
    minlen=None,
    maxlen=None,
    taxid=(),
    gene=(),
    evidence=(),
):
    """Accepts a list of fasta objects and optional filtering parameters.
    Returns a filtered list of fasta objects."""
    if reviewed == "yes":
        fasta_list = filter(lambda x: x.reviewed, fasta_list)
    elif reviewed == "no":
        fasta_list = filter(lambda x: not x.reviewed, fasta_list)

    if len(accession) is not 0:
        fasta_list = filter(lambda x: x.accession in accession, fasta_list)
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
    argument."""

    # Convert evidence list to int, since click only allows string types for click.Choice type
    evidence = tuple(int(x) for x in evidence)

    # Check whether the file is valid fasta or text format
    filetype = check_format(infile)

    # Generate, filter, and output the fasta list
    if filetype == "fasta":
        fasta_list = FastaParser(infile)
    elif filetype == "text":
        fasta_list = text_parser(infile)

    filtered_fasta = filter_all(
        fasta_list, reviewed, accession, minlen, maxlen, taxid, gene, evidence
    )
    for f in filtered_fasta:
        outfile.write(f.format())
