class Fasta:
    """Class to represent a UniProt fasta object."""

    def __init__(
        self,
        sequence: str,
        reviewed: bool = False,
        accession: str = None,
        entry_name: str = None,
        name: str = None,
        species: str = None,
        taxid: str = None,
        gene: str = None,
        evidence: int = None,
        version: int = None,
        fragment: bool = False,
    ) -> None:
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
        self.sequence = sequence

    def __repr__(self) -> str:
        return f"Fasta({self.accession}, {self.entry_name}, {len(self)})"

    def __len__(self) -> int:
        """Defines the 'length' of the class as the sequence length."""
        return len(self.sequence)

    def header(self) -> str:
        """Returns a fasta header string based on the class attributes.
        The header format is in the UniProt style."""
        status = "sp" if self.reviewed else "tr"
        if self.fragment:
            name = self.name + " (Fragment)"
        else:
            name = self.name

        header = f">{status}|{self.accession}|{self.entry_name} {name} OS={self.species} OX={self.taxid} GN={self.gene} PE={str(self.evidence)} SV={str(self.version)}"
        return header

    def format(self, line_length: int = 60) -> str:
        """Returns a nicely formatted multiline fasta string.
        The line_length parameter can be used to set the sequence line length."""
        formatted_sequence = ""
        for i in range(0, len(self), line_length):
            formatted_sequence += self.sequence[i : i + line_length] + "\n"
        return f"{self.header()}\n{formatted_sequence}"
