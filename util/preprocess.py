def get_sequence(file):
    """
        preprocess a tokenized file into list of list
    """
    with open(file, "r") as f:
        seqs = []
        row = []
        for line in f.readlines():
            if line == "\n":
                seqs.append(row)
                row = []
                continue
            row.append( line.strip("\n").split("\t") )
    return seqs