import unittest
import upfilter.cli as cli
from collections import namedtuple
from upfilter import FastaParser


class TestCLI(unittest.TestCase):
    """Tests for the command-line interface module."""

    def setUp(self):
        with open("tests/samples/SHLD1.fasta", "r") as infile:
            fasta_list = list(FastaParser(infile))
        self.fasta_list = fasta_list

    def test_filter_reviewed_yes(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, reviewed="yes"))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_reviewed_no(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, reviewed="no"))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_minlen_200(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, minlen=200))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_minlen_300(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, minlen=300))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_maxlen_200(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, maxlen=200))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_maxlen_300(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, maxlen=300))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_maxlen_minlen(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, minlen=205, maxlen=205))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].accession, "Q8IYI0")

    def test_filter_taxid(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, taxid=["10090"]))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].accession, "Q9D112")

    def test_filter_taxid_multiple(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, taxid=["9606", "10090"]))
        self.assertEqual(len(filtered_fasta), 2)

    def test_filter_maxlen_taxid(self):
        filtered_fasta = list(
            cli.filter_all(self.fasta_list, maxlen=205, taxid=["10090"])
        )
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_evidence(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, evidence=(1,)))
        self.assertEqual(len(filtered_fasta), 1)
