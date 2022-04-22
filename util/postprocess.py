def joinSeqTag(seqs, tags):
    output = []
    for i in range(len(seqs)):
        temp = []
        for token, tag in zip(seqs[i], tags[i]):
            if tag != "O":
                temp.append( (token[0],tag) )

        output.append(temp)
        
    return output