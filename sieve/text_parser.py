from sieve import Fasta


def text_parser(filehandle):
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
        elif key == 'DT':
            if 'sequence version' in line:
                tokens = line[5:].strip('.\n').split()
                fasta.version = int(tokens[3])
        elif key == 'DE':
            if "RecName" in line:
                fasta.name = _extract_name(line)
            # Get the first SubName if no RecName found
            elif fasta.name is None and line[5:12] == "SubName":
                fasta.name = _extract_name(line)
            elif line[5:10] == "Flags" and "Fragment" in line:
                fasta.fragment = True
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


def _extract_name(line):
    tokens = line[19:-2].split(' {')
    name = tokens[0]
    return name
