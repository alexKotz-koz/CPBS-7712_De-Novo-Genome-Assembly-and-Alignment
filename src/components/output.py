import pandas as pd
import json
import os

"""
out.aln file structure:

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
"""


class Output:

    def __init__(self):
        pass

    # Input: all of the read-kmers that exist in the final contig with thier associated metadata (readsInContig.json), final contig string (ALLELES.fasta)
    # Output: output.aln file (specs above)
    def createOutput(self):
        readsInContig = []
        contig = ""
        rows = []
        qseqid = "contig1"

        # os management for GitHub workflow
        scriptDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        readsInContigFilePath = os.path.join(scriptDir, "data/logs/readsInContig.json")
        ALLELESFilePath = os.path.join(scriptDir, "data/output/ALLELES.fasta")

        with open(readsInContigFilePath, "r") as file:
            readsInContig = json.load(file)
        with open(ALLELESFilePath, "r") as file:
            contig = file.readline()

        # for each read that has been idetified in the ALLELES.fasta contig
        for kmerDict in readsInContig:
            # kmerDict contains the read-kmers that exist in the contig (with location of read-kmer in read)
            for kmer, reads in kmerDict.items():

                # get start and stop location of read-kmer in contig
                qstart = contig.index(kmer)
                qend = qstart + len(kmer)

                # iterate over reads where read-kmer is found
                for read, locations in reads.items():
                    sseqid = read
                    for location in locations:
                        # get location of read-kmer in original read
                        for sstart, send in location.items():
                            newRow = {
                                "sseqid": sseqid,
                                "qseqid": qseqid,
                                "sstart": sstart,
                                "send": send,
                                "qstart": qstart,
                                "qend": qend,
                            }
                            rows.append(newRow)

        outputDf = pd.DataFrame(rows)
        outputDf.to_csv("data/output/output.aln", sep="\t", index=False)
