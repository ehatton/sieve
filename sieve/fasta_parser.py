import re
from sieve import Fasta


class FastaParser:
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
        return Fasta(*fields, lines[1:])

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

