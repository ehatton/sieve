import unittest
from sieve.fasta_parser import Fasta, FastaParser
from io import StringIO


class TestFastaParser(unittest.TestCase):
    """Tests for the sieve FastaParser class."""

    def test_parse_header(self):
        header = ">sp|P11111|NECK2_BPT4 Neck protein gp14 OS=Enterobacteria phage T4 OX=10665 GN=14 PE=1 SV=1"
        fields = FastaParser._parse_header(header)
        self.assertEqual(fields[0], True)
        self.assertEqual(fields[1], "P11111")
        self.assertEqual(fields[2], "NECK2_BPT4")
        self.assertEqual(fields[3], "Neck protein gp14")
        self.assertEqual(fields[4], "Enterobacteria phage T4")
        self.assertEqual(fields[5], "10665")
        self.assertEqual(fields[6], "14")
        self.assertEqual(fields[7], 1)
        self.assertEqual(fields[8], 1)
        self.assertEqual(fields[9], False)

    def test_parse_header_fragment(self):
        header = ">tr|E9PW65|E9PW65_MOUSE Bone morphogenetic protein receptor type-1A (Fragment) OS=Mus musculus OX=10090 GN=Bmpr1a PE=4 SV=2"
        fields = FastaParser._parse_header(header)
        self.assertEqual(fields[0], False)
        self.assertEqual(fields[1], "E9PW65")
        self.assertEqual(fields[2], "E9PW65_MOUSE")
        self.assertEqual(fields[3], "Bone morphogenetic protein receptor type-1A")
        self.assertEqual(fields[4], "Mus musculus")
        self.assertEqual(fields[5], "10090")
        self.assertEqual(fields[6], "Bmpr1a")
        self.assertEqual(fields[7], 4)
        self.assertEqual(fields[8], 2)
        self.assertEqual(fields[9], True)

    def test_parse_header_no_gene(self):
        header = ">sp|P0C8S0|SMAKA_DANRE Small membrane A-kinase anchor protein OS=Danio rerio OX=7955 PE=3 SV=1"
        fields = FastaParser._parse_header(header)
        self.assertEqual(fields[0], True)
        self.assertEqual(fields[1], "P0C8S0")
        self.assertEqual(fields[3], "Small membrane A-kinase anchor protein")
        self.assertEqual(fields[4], "Danio rerio")
        self.assertEqual(fields[5], "7955")
        self.assertEqual(fields[6], None)
        self.assertEqual(fields[7], 3)
        self.assertEqual(fields[8], 1)
        self.assertEqual(fields[9], False)

    def test_parse_header_trembl(self):
        header = ">tr|A0A075F882|A0A075F882_MOUSE Heat shock factor 1, isoform CRA_a OS=Mus musculus OX=10090 GN=Hsf1 PE=2 SV=1"
        fields = FastaParser._parse_header(header)
        self.assertEqual(fields[0], False)
        self.assertEqual(fields[1], "A0A075F882")
        self.assertEqual(fields[2], "A0A075F882_MOUSE")
        self.assertEqual(fields[3], "Heat shock factor 1, isoform CRA_a")
        self.assertEqual(fields[4], "Mus musculus")
        self.assertEqual(fields[5], "10090")
        self.assertEqual(fields[6], "Hsf1")
        self.assertEqual(fields[7], 2)
        self.assertEqual(fields[8], 1)
        self.assertEqual(fields[9], False)

    def test_parser(self):
        with open("tests/samples/SHLD1.fasta", "r") as infile:
            fasta = list(i for i in FastaParser(infile))
        # Check that we get a list of 3 items
        self.assertEqual(len(fasta), 3)
        # Check that the items are Fasta objects
        self.assertIsInstance(fasta[0], Fasta)
        # Check that the sequence of the last item is the expected length
        self.assertEqual(len(fasta[2]), 206)

    def test_parser_trembl(self):
        with open("tests/samples/A0A075F882.fasta", "r") as infile:
            fasta = list(i for i in FastaParser(infile))
        # Check that we get a list of 1 item
        self.assertEqual(len(fasta), 1)
        # Check that the items are Fasta objects
        self.assertIsInstance(fasta[0], Fasta)

    def test_file_format_check(self):
        invalid_fasta = StringIO("ID   BRCA1_MOUSE\nAC   P12345\n")
        self.assertRaises(ValueError, FastaParser, invalid_fasta)

    def test_file_format_check_sp(self):
        valid_sp = StringIO(">sp|Q9D112|SHLD1_MOUSE ")
        # Check that instantiating the class doesn't throw an error
        FastaParser(valid_sp)

    def test_file_format_check_tr(self):
        valid_tr = StringIO(">tr|A0A075F882|A0A075F882_MOUSE")
        # Check that instantiating the class doesn't throw an error
        FastaParser(valid_tr)
