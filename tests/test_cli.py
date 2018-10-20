import unittest
import upfilter.cli as cli
from collections import namedtuple
from upfilter import FastaParser


# Define a mock parser argument object for use in these tests.
# The infile and outfile attributes are not needed here, hence omitted.
mock_parser_args = namedtuple("MockParserArgs", ["reviewed", "min", "max", "taxid", "evidence"])


class TestCLI(unittest.TestCase):
    """Tests for the command-line interface module."""

    def setUp(self):
        with open("tests/samples/SHLD1.fasta", "r") as infile:
            fasta_list = list(FastaParser(infile))
        self.fasta_list = fasta_list
        
    def test_create_parser(self):
        parser = cli.create_parser()
        options = parser._actions

        # Check that the parser has all the expected options (arguments)
        # Length of the options will be one more that the number defined in the function as it also includes HelpAction
        self.assertEqual(len(options), 8)
        self.assertEqual(options[1].dest, "infile")
        self.assertEqual(options[2].dest, "outfile")
        self.assertEqual(options[3].dest, "reviewed")
        self.assertEqual(options[4].dest, "min")
        self.assertEqual(options[5].dest, "max")
        self.assertEqual(options[6].dest, "taxid")
        self.assertEqual(options[7].dest, "evidence")

    def test_filter_reviewed_yes(self):
        args = mock_parser_args(reviewed="yes", min=None, max=None, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_reviewed_no(self):
        args = mock_parser_args(reviewed="no", min=None, max=None, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_min_200(self):
        args = mock_parser_args(reviewed=None, min=200, max=None, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_min_300(self):
        args = mock_parser_args(reviewed=None, min=300, max=None, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_max_200(self):
        args = mock_parser_args(reviewed=None, min=None, max=200, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_max_300(self):
        args = mock_parser_args(reviewed=None, min=None, max=300, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 3)

    def test_filter_max_min(self):
        args = mock_parser_args(reviewed=None, min=205, max=205, taxid=None, evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].accession, "Q8IYI0")

    def test_filter_taxid(self):
        args = mock_parser_args(reviewed=None, min=None, max=None, taxid=["10090"], evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].accession, "Q9D112")

    def test_filter_taxid_multiple(self):
        args = mock_parser_args(reviewed=None, min=None, max=None, taxid=["9606", "10090"], evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 2)

    def test_filter_max_taxid(self):
        args = mock_parser_args(reviewed=None, min=None, max=205, taxid=["10090"], evidence=None)
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 0)

    def test_filter_evidence(self):
        args = mock_parser_args(reviewed=None, min=None, max=205, taxid=None, evidence=[1])
        filtered_fasta = list(cli.filter_all(args, self.fasta_list))
        self.assertEqual(len(filtered_fasta), 1)

