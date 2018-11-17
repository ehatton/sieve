
class Fasta:
    def __init__(
        self,
        reviewed=False,
        accession=None,
        entry_name=None,
        name=None,
        species=None,
        taxid=None,
        gene=None,
        evidence=None,
        version=None,
        fragment=False,
        sequence_lines=[],
    ):
        self.reviewed = reviewed
        self.accession = accession
        self.entry_name = entry_name
        self.name = name
        self.species = species
        self.taxid = taxid
        self.gene = gene
        self.evidence = evidence
        self.version = version
        self.fragment = fragment
        self.sequence_lines = sequence_lines

    # TODO: allow different sequence formats e.g. set line length
    @property
    def sequence(self):
        """Returns sequence as a single string with no spaces or line breaks."""
        return "".join(i.strip() for i in self.sequence_lines)

    def __repr__(self):
        """Defines a nicely-formatted string representation of the class for debugging purposes."""
        return f"Fasta({self.accession}, {self.entry_name}, {len(self)})"

    def __len__(self):
        """Defines the 'length' of the class as the sequence length."""
        return len(self.sequence)

    def header(self):
        """Returns a fasta header string based on the class attributes.
        The header format is in the UniProtKB style."""
        status = "sp" if self.reviewed else "tr"
        if self.fragment:
            name = self.name + " (Fragment)"
        else:
            name = self.name

        header = f">{status}|{self.accession}|{self.entry_name} {name} OS={self.species} OX={self.taxid} GN={self.gene} PE={str(self.evidence)} SV={str(self.version)}"
        return header

    def format(self, line_length=60):
        """Returns a nicely formatted multiline fasta string.
        The line_length parameter can be used to set the sequence line length."""
        formatted_sequence = ""
        for i in range(0, len(self), line_length):
            formatted_sequence += self.sequence[i : i + line_length] + "\n"
        return f"{self.header()}\n{formatted_sequence}"
