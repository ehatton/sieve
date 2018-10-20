import argparse
import sys
from upfilter.fasta_parser import FastaParser


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="file to read, must contain UniProt fasta sequences",
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="file to write, filtered UniProt fasta sequences",
    )
    parser.add_argument(
        "-r",
        "--reviewed",
        help="filter for reviewed (SwissProt) or unreviewed (TrEMBL) entries",
        choices=["yes", "no"],
    )
    parser.add_argument(
        "--min", help="filter fasta sequences by minimum sequence length", type=int
    )
    parser.add_argument(
        "--max", help="filter fasta sequences by maximum sequence length", type=int
    )
    parser.add_argument(
        "-t",
        "--taxid",
        nargs="*",
        help="filter fasta sequences with given NCBI taxonomy id(s)",
    )
    parser.add_argument("-e", "--evidence", choices=[1, 2, 3, 4, 5], nargs="*", type=int, help="filter fasta sequences by evidence level(s)")

    return parser


def filter_all(parser_args, fasta_list):
    if parser_args.reviewed == "yes":
        fasta_list = filter(lambda x: x.reviewed, fasta_list)
    elif parser_args.reviewed == "no":
        fasta_list = filter(lambda x: not x.reviewed, fasta_list)

    if parser_args.taxid is not None:
        fasta_list = filter(lambda x: x.taxid in parser_args.taxid, fasta_list)
    if parser_args.min is not None:
        fasta_list = filter(lambda x: len(x) >= parser_args.min, fasta_list)
    if parser_args.max is not None:
        fasta_list = filter(lambda x: len(x) <= parser_args.max, fasta_list)
    if parser_args.evidence is not None:
        fasta_list = filter(lambda x: x.evidence in parser_args.evidence, fasta_list)

    return fasta_list


def main():
    """Entry point to program. Parses command line arguments and outputs filtered fasta sequences."""
    parser = create_parser()
    parser_args = parser.parse_args()

    with parser_args.infile as infile, parser_args.outfile as outfile:
        fasta_list = FastaParser(infile)
        filtered_fasta = filter_all(parser_args, fasta_list)
        for f in filtered_fasta:
            outfile.write(f.format())


if __name__ == "__main__":
    main()
