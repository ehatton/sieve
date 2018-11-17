from sieve import Fasta


def parse_text(filehandle):
    for line in filehandle:
        key = line[:2]
        if key == "ID":
            fasta = Fasta(sequence_lines=[]) # reset sequence lines!
            tokens = line.split()
            fasta.entry_name = tokens[1]
            fasta.reviewed = True if tokens[2] == "Reviewed;" else False
        elif key == "AC":
            if fasta.accession is None:
                accessions = line[5:].rstrip(";\n").split("; ")
                fasta.accession = accessions[0]
        elif key == "GN":
            if line[5:10] == "Name=":
                tokens = line[10:].split(";")
                # Remove evidence tags, if present
                gene_tokens = tokens[0].split(" {")
                fasta.gene = gene_tokens[0]
        elif key == "OS":
            # TODO: check for multiline species name (excluding brackets)
            if fasta.species is None:
                species_line = line[5:].strip().split(" (")
                fasta.species = species_line[0].strip(".")
        elif key == "OX":
            if "NCBI_TaxID" in line:
                tokens = line[5:].strip(";\n").split("; ")
                # Remove evidence tag if present
                taxid_tokens = tokens[0][11:].split(" {")
                fasta.taxid = taxid_tokens[0]
        elif key == 'PE':
            fasta.evidence = int(line[5])
        elif key == "  ":
            sequence_line = line.strip().replace(" ", "")
            fasta.sequence_lines.append(sequence_line)
        elif key == "//":
            yield fasta


class UniProtTextParser:
    def __init__(self, filehandle):
        self.filehandle = filehandle
        self.line = None

    def __next__(self):
        # ID line should always be first
        self.line = next(self.filehandle)
        if not self.line.startswith("ID"):
            raise ValueError(
                f"Invalid file type. Expected UniProt flat file format, found:\n{self.line}"
            )
        entry_name, reviewed = self._parse_id()
        # Initialize new Fasta object
        fasta = Fasta(
            entry_name=entry_name, reviewed=reviewed, sequence_lines=[]
        )

        # Read the rest of the entry, up to the '//' delimiter
        self.line = next(self.filehandle)
        while True:
            key = self.line[:2]
            if key == "AC":
                accessions = self._parse_ac()
                fasta.accession = accessions[0]
            elif key == "DT":
                sequence_version = self._parse_dt()
                if sequence_version is not None:
                    fasta.version = sequence_version
            elif key == "DE":
                name, fragment = self._parse_de()
                if name is not None:
                    fasta.name = name
                fasta.fragment = fragment
            elif self.line.startswith("GN"):
                fasta.gene = self._parse_gn()
            elif key == "OS":
                fasta.species = self._parse_os()
            elif key == "OG":
                self._parse_og()
            elif key == "OC":
                self._parse_oc()
            elif key == "OX":
                fasta.taxid = self._parse_ox()
            elif key == "OH":
                self._parse_oh()
            elif key.startswith("R"):
                self._parse_r()
            elif key == "CC":
                comments = self._parse_cc()
                print(comments)
            elif key == "DR":
                self._parse_dr()
            elif key == "PE":
                fasta.evidence = self._parse_pe()
            elif key == "KW":
                self._parse_kw()
            elif key == "FT":
                self._parse_ft()
            elif key == "SQ":
                self._parse_sq()
            elif key == "  ":
                fasta.sequence_lines = self._parse_sequence()
            elif key == "//":
                break
        return fasta

    def __iter__(self):
        return self

    def _parse_id(self):
        tokens = self.line.split()
        entry_name = tokens[1]
        reviewed = True if tokens[2] == "Reviewed;" else False
        return entry_name, reviewed

    def _parse_ac(self):
        accessions = self.line[5:].rstrip(";\n").split("; ")
        while self.line.startswith("AC"):
            self.line = next(self.filehandle)
            accessions += self.line[5:].rstrip(";\n").split("; ")
        return accessions

    def _parse_dt(self):
        while self.line.startswith("DT"):
            if "sequence version" in self.line:
                _, version_string = self.line[5:].strip().split(", ")
                version = version_string[17:-1]
            self.line = next(self.filehandle)
        return version

    def _parse_de(self):
        fragment = False
        if "RecName" in self.line or "SubName" in self.line:
            name = self.line[19:].rstrip(";\n")
        while self.line.startswith("DE"):
            self.line = next(self.filehandle)
            if "Fragment" in self.line:
                fragment = True
        return name, fragment

    def _parse_gn(self):
        gene = None
        while self.line.startswith("GN"):
            if self.line[5:10] == "Name=":
                tokens = self.line[10:].split(";")
                # Remove evidence tags, if present
                try:
                    gene, _ = tokens[0].split(" {")
                except ValueError:
                    gene = tokens[0]
            self.line = next(self.filehandle)
        return gene

    def _parse_os(self):
        species_string = self.line[5:].strip()
        while True:
            self.line = next(self.filehandle)
            if not self.line.startswith("OS"):
                break
            species_string += self.line[5:].strip()
        end = species_string.find(" (")
        species = species_string[:end]
        return species

    def _parse_og(self):
        while self.line.startswith("OG"):
            self.line = next(self.filehandle)

    def _parse_oc(self):
        while self.line.startswith("OC"):
            self.line = next(self.filehandle)

    def _parse_ox(self):
        if "NCBI_TaxID" in self.line:
            tokens = self.line[5:].strip(";\n").split("; ")
            # Remove evidence tag if present
            try:
                taxid, _ = tokens[0][11:].split(" {")
            except ValueError:
                taxid = tokens[0][11:]
        self.line = next(self.filehandle)
        return taxid

    def _parse_oh(self):
        while self.line.startswith("OH"):
            self.line = next(self.filehandle)

    def _parse_r(self):
        while self.line.startswith("R"):
            self.line = next(self.filehandle)

    def _parse_cc(self):
        comment = None
        comments = []
        while self.line.startswith("CC"):
            if self.line.startswith("CC   -!- "):
                if comment:
                    comments.append(comment)
                comment = self.line[8:].strip()
            else:
                comment += self.line[7:].strip()
            self.line = next(self.filehandle)
        return comments

    def _parse_dr(self):
        while self.line.startswith("DR"):
            self.line = next(self.filehandle)

    def _parse_ft(self):
        while self.line.startswith("FT"):
            self.line = next(self.filehandle)

    def _parse_pe(self):
        evidence = self.line[5]
        self.line = next(self.filehandle)
        return evidence

    def _parse_kw(self):
        while self.line.startswith("KW"):
            self.line = next(self.filehandle)

    def _parse_sq(self):
        self.line = next(self.filehandle)

    def _parse_sequence(self):
        sequence_lines = []
        while self.line.startswith("  "):
            seq = self.line.strip().replace(" ", "")
            sequence_lines.append(seq)
            self.line = next(self.filehandle)
        return sequence_lines


if __name__ == "__main__":
    with open("pias4.txt", "r") as infile:
        for entry in UniProtTextParser(infile):
            print(entry)
            print(entry.header())
