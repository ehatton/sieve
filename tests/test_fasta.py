import unittest
from sieve import Fasta, FastaParser
from io import StringIO


class TestFasta(unittest.TestCase):
    """Tests for the sieve Fasta class."""

    def setUp(self):
        header = ">sp|P60761|NEUG_MOUSE Neurogranin OS=Mus musculus OX=10090 GN=Nrgn PE=1 SV=1"
        seq = [
            "MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGG\n",
            "PGGAGGARGGAGGGPSGD\n",
        ]
        fields = FastaParser._parse_header(header)
        self.header = header
        self.Fasta = Fasta(*fields, seq)

    def test_repr(self):
        self.assertEqual(self.Fasta.__repr__(), "Fasta(P60761, NEUG_MOUSE, 78)")

    def test_sequence(self):
        self.assertEqual(
            self.Fasta.sequence,
            "MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGGPGGAGGARGGAGGGPSGD",
        )

    def test_len(self):
        self.assertEqual(len(self.Fasta), 78)

    def test_header(self):
        self.assertEqual(self.Fasta.header(), self.header)

    def test_format(self):
        formatted = """>sp|P60761|NEUG_MOUSE Neurogranin OS=Mus musculus OX=10090 GN=Nrgn PE=1 SV=1
MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGG
PGGAGGARGGAGGGPSGD\n"""
        self.assertEqual(self.Fasta.format(), formatted)


class TestFastaFragment(unittest.TestCase):
    """Additional tests for the sieve Fasta class, to check that it works with sequences annotated as fragment."""

    def setUp(self):
        header = ">tr|E9PW65|E9PW65_MOUSE Bone morphogenetic protein receptor type-1A (Fragment) OS=Mus musculus OX=10090 GN=Bmpr1a PE=4 SV=2"
        seq = [
            "MTQLYTYIRLLGACLFIISHVQGQNLDSMLHGTGMKSDLDQKKPENGVTLAPEDTLPFLK",
            "CYCSGHCPDDAINNTCITNGHCFAIIEEDDQGETTLTSGCMKYEGSDF",
        ]
        fields = FastaParser._parse_header(header)
        self.header = header
        self.Fasta = Fasta(*fields, seq)

    def test_header(self):
        self.assertEqual(self.Fasta.header(), self.header)
