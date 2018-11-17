import re


class UniProtFastaParser:
    """Generator class which reads in a UniProt fasta format file.
    Accepts filehandle as input and yields Fasta objects."""

    def __init__(self, filehandle):
        self.filehandle = filehandle
        self.line = next(self.filehandle)
        # A simple test to check that the file looks like UniProt fasta format
        if not self.line.startswith((">sp", ">tr")):
            raise ValueError(
                "Invalid file format. This parser requires a UniProt fasta format file."
            )

    def __next__(self):
        # Initialize lines with fasta header
        lines = [self.line]

        # Get the next line...this should always be the first sequence line
        # If we have reached end of file, this raises StopIteration
        self.line = next(self.filehandle)

        # Get rest of sequence lines and collect in lines list
        while not self.line.startswith(">"):
            lines.append(self.line)
            try:
                self.line = next(self.filehandle)
            # When the last line is reached we need to return the lines list
            # StopIteration is handled in line 13 above, in the next call to the iterator
            except StopIteration:
                break

        fields = self._parse_header(lines[0])
        return UniProtFasta(*fields, lines[1:])

    def __iter__(self):
        return self

    @staticmethod
    def _parse_header(line):
        """Reads a UniProt format fasta header line and parses out all the different fields."""

        # A hideous regex for parsing the header line
        # Note that the gene name is optional so there is a nested capture group for this
        header_re = re.compile(
            r"^>(sp|tr)\|(\w{6,10})\|(\w{,10}_\w{,5})\s(.+)\sOS=(.+)\sOX=(\d+)\s(GN=(.+)\s)*PE=(\d)\sSV=(\d+)$"
        )
        captures = re.match(header_re, line).groups()

        # Convert the first capture into a boolean
        reviewed = True if captures[0] == "sp" else False

        # Check for fragment flag in name and remove
        name = captures[3]
        if name.endswith(" (Fragment)"):
            fragment = True
            name = name.strip(" (Fragment)")
        else:
            fragment = False

        evidence = int(captures[8])
        version = int(captures[9])

        fields = (
            reviewed,
            *captures[1:3],
            name,
            *captures[4:6],
            captures[7],
            evidence,
            version,
            fragment,
        )
        return fields


class UniProtFasta:
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
        return f"UniProtFasta({self.accession}, {self.entry_name}, {len(self)})"

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
