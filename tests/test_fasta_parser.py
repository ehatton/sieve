import unittest
from sieve.fasta_parser import Fasta, parse_fasta, _parse_header, FastaParserError
from io import StringIO


class TestFastaParser(unittest.TestCase):
    """Tests for the sieve FastaParser class."""

    def test_parse_header(self):
        header = ">sp|P11111|NECK2_BPT4 Neck protein gp14 OS=Enterobacteria phage T4 OX=10665 GN=14 PE=1 SV=1"
        fields = _parse_header(header)
        self.assertEqual(fields["reviewed"], True)
        self.assertEqual(fields["accession"], "P11111")
        self.assertEqual(fields["entry_name"], "NECK2_BPT4")
        self.assertEqual(fields["name"], "Neck protein gp14")
        self.assertEqual(fields["species"], "Enterobacteria phage T4")
        self.assertEqual(fields["taxid"], "10665")
        self.assertEqual(fields["gene"], "14")
        self.assertEqual(fields["evidence"], 1)
        self.assertEqual(fields["version"], 1)
        self.assertEqual(fields["fragment"], False)

    def test_parse_header_fragment(self):
        header = ">tr|E9PW65|E9PW65_MOUSE Bone morphogenetic protein receptor type-1A (Fragment) OS=Mus musculus OX=10090 GN=Bmpr1a PE=4 SV=2"
        fields = _parse_header(header)
        self.assertEqual(fields["reviewed"], False)
        self.assertEqual(fields["accession"], "E9PW65")
        self.assertEqual(fields["entry_name"], "E9PW65_MOUSE")
        self.assertEqual(fields["name"], "Bone morphogenetic protein receptor type-1A")
        self.assertEqual(fields["species"], "Mus musculus")
        self.assertEqual(fields["taxid"], "10090")
        self.assertEqual(fields["gene"], "Bmpr1a")
        self.assertEqual(fields["evidence"], 4)
        self.assertEqual(fields["version"], 2)
        self.assertEqual(fields["fragment"], True)

    def test_parse_header_no_gene(self):
        header = ">sp|P0C8S0|SMAKA_DANRE Small membrane A-kinase anchor protein OS=Danio rerio OX=7955 PE=3 SV=1"
        fields = _parse_header(header)
        self.assertEqual(fields["reviewed"], True)
        self.assertEqual(fields["accession"], "P0C8S0")
        self.assertEqual(fields["name"], "Small membrane A-kinase anchor protein")
        self.assertEqual(fields["species"], "Danio rerio")
        self.assertEqual(fields["taxid"], "7955")
        self.assertEqual(fields["gene"], None)
        self.assertEqual(fields["evidence"], 3)
        self.assertEqual(fields["version"], 1)
        self.assertEqual(fields["fragment"], False)

    def test_parse_header_trembl(self):
        header = ">tr|A0A075F882|A0A075F882_MOUSE Heat shock factor 1, isoform CRA_a OS=Mus musculus OX=10090 GN=Hsf1 PE=2 SV=1"
        fields = _parse_header(header)
        self.assertEqual(fields["reviewed"], False)
        self.assertEqual(fields["accession"], "A0A075F882")
        self.assertEqual(fields["entry_name"], "A0A075F882_MOUSE")
        self.assertEqual(fields["name"], "Heat shock factor 1, isoform CRA_a")
        self.assertEqual(fields["species"], "Mus musculus")
        self.assertEqual(fields["taxid"], "10090")
        self.assertEqual(fields["gene"], "Hsf1")
        self.assertEqual(fields["evidence"], 2)
        self.assertEqual(fields["version"], 1)
        self.assertEqual(fields["fragment"], False)

    def test_parser(self):
        with open("tests/fixtures/SHLD1.fasta", "r") as infile:
            fasta = list(parse_fasta(infile))
        # Check that we get a list of 3 items
        self.assertEqual(len(fasta), 3)
        # Check that the items are Fasta objects
        self.assertIsInstance(fasta[0], Fasta)
        # Check that the sequence of the last item is the expected length
        self.assertEqual(len(fasta[2]), 206)

    def test_parser_trembl(self):
        with open("tests/fixtures/A0A075F882.fasta", "r") as infile:
            fasta = list(parse_fasta(infile))
        # Check that we get a list of 1 item
        self.assertEqual(len(fasta), 1)
        # Check that the items are Fasta objects
        self.assertIsInstance(fasta[0], Fasta)

    def test_file_format_check(self):
        invalid_fasta = StringIO("ID   BRCA1_MOUSE\nAC   P12345\n")
        with self.assertRaises(FastaParserError):
            list(parse_fasta(invalid_fasta))

    def test_file_format_check_sp(self):
        valid_sp = StringIO(">sp|Q9D112|SHLD1_MOUSE ")
        # Check that instantiating the class doesn't throw an error
        parse_fasta(valid_sp)

    def test_file_format_check_tr(self):
        valid_tr = StringIO(">tr|A0A075F882|A0A075F882_MOUSE")
        # Check that instantiating the class doesn't throw an error
        parse_fasta(valid_tr)


class TestFastaParserFragment(unittest.TestCase):
    """Additional tests for the header parser, to check that it works with sequences annotated as fragment."""

    @classmethod
    def setUpClass(cls):
        header = ">tr|E9PW65|E9PW65_MOUSE Bone morphogenetic protein receptor type-1A (Fragment) OS=Mus musculus OX=10090 GN=Bmpr1a PE=4 SV=2"
        cls.header_fields = _parse_header(header)

    def test_header_name(self):
        expected_name = "Bone morphogenetic protein receptor type-1A"
        self.assertEqual(self.header_fields["name"], expected_name)

    def test_header_fragment(self):
        self.assertTrue(self.header_fields["fragment"])
