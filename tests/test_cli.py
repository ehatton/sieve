import unittest
import upfilter.cli as cli
from collections import namedtuple
from upfilter import FastaParser


class TestFilter(unittest.TestCase):
    """Tests for the command-line interface module."""

    def setUp(self):
        with open("tests/SHLD1.fa", "r") as infile:
            fasta_list = list(FastaParser(infile))
        self.fasta_list = fasta_list

        self.mock_parser_args = namedtuple(
            "MockParserArgs", ["infile", "outfile", "reviewed", "min", "max", "taxid"]
        )

    def test_create_parser(self):
        parser = cli.create_parser()
        options = parser._actions

        # Check that the parser has all the expected options (arguments)
        # Length of the options will be one more that the number defined in the function as it also includes HelpAction
        self.assertEqual(len(options), 7)
        self.assertEqual(options[1].dest, "infile")
        self.assertEqual(options[2].dest, "outfile")
        self.assertEqual(options[3].dest, "reviewed")
        self.assertEqual(options[4].dest, "min")
        self.assertEqual(options[5].dest, "max")
        self.assertEqual(options[6].dest, "taxid")

    # def test_filter_all():
    #     parser_args =
