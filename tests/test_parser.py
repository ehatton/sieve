import unittest
from upfilter.fasta_parser import Fasta, FastaParser
from io import StringIO


class TestFasta(unittest.TestCase):
    """Tests for the upfilter Fasta class."""

    def setUp(self):
        header = ">sp|P60761|NEUG_MOUSE Neurogranin OS=Mus musculus OX=10090 GN=Nrgn PE=1 SV=1"
        seq = [
            "MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGG\n",
            "PGGAGGARGGAGGGPSGD\n",
        ]
        fields = FastaParser._parse_header(header)
        self.header = header
        self.fasta = Fasta(*fields, seq)

    def test_repr(self):
        self.assertEqual(self.fasta.__repr__(), "Fasta(P60761, NEUG_MOUSE, 78)")

    def test_sequence(self):
        self.assertEqual(
            self.fasta.sequence,
            "MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGGPGGAGGARGGAGGGPSGD",
        )

    def test_len(self):
        self.assertEqual(len(self.fasta), 78)

    def test_header(self):
        self.assertEqual(self.fasta.header(), self.header)

    def test_format(self):
        formatted = """>sp|P60761|NEUG_MOUSE Neurogranin OS=Mus musculus OX=10090 GN=Nrgn PE=1 SV=1
MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGG
PGGAGGARGGAGGGPSGD\n"""
        self.assertEqual(self.fasta.format(), formatted)


class TestFastaFragment(unittest.TestCase):
    """Additional tests for the upfilter Fasta class, to check that it works with sequences annotated as fragment."""

    def setUp(self):
        header = ">tr|E9PW65|E9PW65_MOUSE Bone morphogenetic protein receptor type-1A (Fragment) OS=Mus musculus OX=10090 GN=Bmpr1a PE=4 SV=2"
        seq = [
            "MTQLYTYIRLLGACLFIISHVQGQNLDSMLHGTGMKSDLDQKKPENGVTLAPEDTLPFLK",
            "CYCSGHCPDDAINNTCITNGHCFAIIEEDDQGETTLTSGCMKYEGSDF",
        ]
        fields = FastaParser._parse_header(header)
        self.header = header
        self.fasta = Fasta(*fields, seq)

    def test_header(self):
        self.assertEqual(self.fasta.header(), self.header)


class TestFastaParser(unittest.TestCase):
    """Tests for the upfilter FastaParser class."""

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

    def test_parser(self):
        with open("tests/samples/SHLD1.fasta", "r") as infile:
            fasta = list(i for i in FastaParser(infile))
        # Check that we get a list of 3 items
        self.assertEqual(len(fasta), 3)
        # Check that the items are Fasta objects
        self.assertIsInstance(fasta[0], Fasta)
        # Check that the sequence of the last item is the expected length
        self.assertEqual(len(fasta[2]), 206)

    def test_file_format_check(self):
        invalid_fasta = StringIO("ID   BRCA1_MOUSE\nAC   P12345\n")
        self.assertRaises(ValueError, FastaParser, invalid_fasta)
