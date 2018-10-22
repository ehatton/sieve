import unittest
import upfilter.cli as cli
from click.testing import CliRunner
from collections import namedtuple
from upfilter import FastaParser


# Defining some constants for expected fasta outputs
BOVIN = """>sp|Q2KIJ1|SHLD1_BOVIN Shieldin complex subunit 1 OS=Bos taurus OX=9913 GN=SHLD1 PE=2 SV=1
MATQETTPGSQTEESNALDLPSAYDIRDYVLQRPSQQTNSEAFSSEEACSIPCSSDVDPD
SSNLNTEQNDSWTSENFWFYPSVKGQPETKEEDDGLRKSLDKFYEVFGNPQPASGNSLST
SVCQCLSQKINELKDQENQTYTLRSFQMARVIFNQNGCSILQKHSRDAHFYPVREGSTSL
QDEKLTPGLSKDIIHFLLQQNLMKDQ
"""

HUMAN = """>sp|Q8IYI0|SHLD1_HUMAN Shieldin complex subunit 1 OS=Homo sapiens OX=9606 GN=SHLD1 PE=1 SV=1
MAARDATSGSLSEESSALDLPSACDIRDYVLQGPSQEANSEAFSSLEFHSFPYSSDVDPD
TSNLNIEQNNSWTAENFWLDPAVKGQSEKEEDDGLRKSLDRFYEMFGHPQPGSANSLSAS
VCKCLSQKITQLRGQESQKYALRSFQMARVIFNRDGCSVLQRHSRDTHFYPLEEGSTSLD
DEKPNPGLSKDITHFLLQQNVMKDL
"""

MOUSE = """>sp|Q9D112|SHLD1_MOUSE Shieldin complex subunit 1 OS=Mus musculus OX=10090 GN=Shld1 PE=2 SV=1
MESQAATPSSLSGESCTLDLPAVCDTSSYEASQRVSQGSSNSLSSLESHPFLSSSTTDPD
SNSLNTEQKGSWDSENFWLDPSSKGQLETNEEEDGLRKSLDRFYEAFAHPLPGSGDPLSA
SVCQCLSQTISELEGQESQRYALRSFQMAQVIFSRDGCSILQRHSRDTRFYPLEQEGSSV
DDEEPTPGLSREVIRFLLEQTVMKDS
"""


class TestCliFilter(unittest.TestCase):
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

    def test_filter_accession(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, accession="Q2KIJ1"))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].entry_name, "SHLD1_BOVIN")

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

    def test_filter_gene(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, gene=("Shld1",)))
        self.assertEqual(len(filtered_fasta), 1)
        self.assertEqual(filtered_fasta[0].taxid, "10090")

    def test_filter_evidence(self):
        filtered_fasta = list(cli.filter_all(self.fasta_list, evidence=(1,)))
        self.assertEqual(len(filtered_fasta), 1)


class TestCliMain(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_reviewed_yes(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-r", "yes"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, BOVIN + HUMAN + MOUSE)

    def test_reviewed_no(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-r", "no"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "")

    def test_accession(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-a", "Q8IYI0", "-a", "Q9D112"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, HUMAN + MOUSE)

    def test_min(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-min", "206"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, BOVIN + MOUSE)

    def test_max(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-max", "205"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, HUMAN)

    def test_taxid(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-t", "10090"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, MOUSE)

    def test_gene(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-g", "SHLD1"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, BOVIN + HUMAN)

    def test_evidence(self):
        result = self.runner.invoke(
            cli.main, ["tests/samples/SHLD1.fasta", "-", "-e", "2"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, BOVIN + MOUSE)
