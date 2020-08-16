import unittest
from sieve import Fasta, parse_fasta
from sieve.fasta_parser import _parse_header
from io import StringIO


class TestFasta(unittest.TestCase):
    """Tests for the sieve Fasta class."""

    @classmethod
    def setUpClass(cls):
        header = ">sp|P60761|NEUG_MOUSE Neurogranin OS=Mus musculus OX=10090 GN=Nrgn PE=1 SV=1"
        seq = "MDCCTESACSKPDDDILDIPLDDPGANAAAAKIQASFRGHMARKKIKSGECGRKGPGPGGPGGAGGARGGAGGGPSGD"
        fields = _parse_header(header)
        cls.header = header
        cls.Fasta = Fasta(sequence=seq, **fields)

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
