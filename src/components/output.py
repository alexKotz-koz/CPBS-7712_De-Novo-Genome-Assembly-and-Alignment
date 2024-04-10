import pandas as pd
import json
class Output:
    def __init__(self):
        pass

    def createOutput(self):
        readsInContig = []
        contig = ""
        with open("data/logs/readsInContig.json", "r") as file:
            readsInContig = json.load(file)
        with open("data/output/ALLELES.fasta", "r") as file:
            contig = file.readline()
        

        '''
        sseqid: name of sequencing read (from READS.fastq.gz)
        qseqid: name of contig matched (from ALLELES.fasta)
        sstart: starting coordinate in sequencing read sseqid that matches qseq
            r-kmer location in original read
        send: ending coordinate in sequencing read sseqid that matches qseq
            r-kmer location in original read
        qstart: starting coordinate in contig that matches sseq
            r-kmer location in contig 
        qend: ending coordinate in contig that matches sseq
            r-kmer location in contig
        '''
        

        rows = []
        qseqid = 'contig1'

        for kmer_dict in readsInContig:
            for kmer, reads in kmer_dict.items():
                qstart = contig.index(kmer)
                qend = qstart + len(kmer)
                
                for read, locations in reads.items():
                    sseqid = read
                    for location in locations:
                        for sstart, send in location.items():
                            newRow = {'sseqid': sseqid, 'qseqid':qseqid, 'sstart':sstart, 'send': send, 'qstart': qstart, 'qend': qend}
                            rows.append(newRow)

        outputDf = pd.DataFrame(rows)
        outputDf.to_csv("data/output/output.aln")
        print(outputDf)
