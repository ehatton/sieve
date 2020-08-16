import re
from typing import Iterator, TextIO
from sieve import Fasta


def parse_fasta(filehandle: TextIO) -> Iterator[Fasta]:
    """[summary]

    Args:
        filehandle ([type]): [description]

    Yields:
        Fasta: UniProt Fasta objects
    """

    header = next(filehandle)
    if not header.startswith(">"):
        raise ValueError(
            "Unexpected file format. First line of FASTA should start with '>'."
        )
    sequence = ""
    for line in filehandle:
        if line.startswith(">"):
            header_fields = _parse_header(header)
            yield Fasta(**header_fields, sequence=sequence)
            # Reset variables
            header = line
            sequence = ""
        else:
            sequence += line.replace(" ", "").strip()
    # Get the last entry
    header_fields = _parse_header(header)
    yield Fasta(**header_fields, sequence=sequence)


def _parse_header(header: str) -> dict:
    """Reads a UniProt format fasta header line and parses out all the different fields.

    Args:
        header: UniProt fasta header line in string format

    Returns:
        Dict: dictionary of header fields
    """

    # Note that the gene name is optional so there is a nested capture group for this
    header_re = re.compile(
        r">(?P<reviewed>sp|tr)\|(?P<accession>\w{6,10})\|(?P<entry_name>\w{,10}_\w{,5})\s(?P<name>.+)\sOS=(?P<species>.+)\sOX=(?P<taxid>\d+)\s(GN=(?P<gene>.+)\s)*PE=(?P<evidence>\d)\sSV=(?P<version>\d+)$"
    )
    raw_fields = re.match(header_re, header).groupdict()
    header_fields = _convert_fields(raw_fields)
    return header_fields


def _convert_fields(fields: dict) -> dict:
    """Helper function which converts a dictionary of header fields (as strings)
     into a version which can be used by the Fasta object init function.

    The suffix "(Fragment)" is removed from the name, if necessary, and the
    field "Fragment" is added to the dict.

    The field "reviewed" is converted from the string "sp" or "tr" to a boolean.

    The fields "evidence" and "version" are converted to int.

    Args:
        fields (Dict[str]): a dictionary of fasta header fields as strings

    Returns:
        Dict: a dictionary of header fields which can be passed to the Fasta
        object init function.
    """
    header_fields = fields.copy()

    # Add fragment field and strip "Fragment" from name if necessary
    if fields["name"].endswith(" (Fragment)"):
        header_fields["fragment"] = True
        header_fields["name"] = fields["name"].strip(" (Fragment)")
    else:
        header_fields["fragment"] = False

    # Convert reviewed to boolean
    header_fields["reviewed"] = True if fields["reviewed"] == "sp" else False

    # Convert evidence and version to int
    header_fields["version"] = int(fields["version"])
    header_fields["evidence"] = int(fields["evidence"])

    return header_fields
