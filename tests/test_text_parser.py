from unittest import TestCase
from sieve import parse_text


class TestTextParser(TestCase):
    def setUp(self):
        with open("tests/samples/pias4.txt", "r") as filehandle:
            fastalist = list(parse_text(filehandle))
        self.fastalist = fastalist

    def test_accession(self):
        self.assertEqual(self.fastalist[0].accession, "Q8N2W9")

    def test_id(self):
        self.assertEqual(self.fastalist[0].entry_name, "PIAS4_HUMAN")

    def test_gene(self):
        self.assertEqual(self.fastalist[0].gene, "PIAS4")
        self.assertEqual(self.fastalist[1].gene, "Pias4")

    def test_species(self):
        self.assertEqual(self.fastalist[1].species, "Mus musculus")

    def test_taxid(self):
        self.assertEqual(self.fastalist[0].taxid, "9606")

    def test_evidence(self):
        self.assertEqual(self.fastalist[1].evidence, 1)

    def test_length(self):
        self.assertEqual(len(self.fastalist[0]), 510)
        # Check that sequence lines are not accumulated in subsequent entries
        self.assertEqual(len(self.fastalist[1]), 507)
