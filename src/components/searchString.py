import sys
import os

# required os set up for testing
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from components.readsToKmers import ReadsToKmers
import json
import pandas as pd


class SearchString:
    def __init__(self, queryData, readsKmerPool, contigs, k):
        self.queryData = queryData
        self.contigs = contigs
        self.readsKmerPool = readsKmerPool
        self.k = 10
        # error checking for test cases, where toy dataset reads and kmers are smaller than the original reads data
        if k < self.k:
            self.k = k

    def queryToKmers(self):
        kmerPool = {}
        sequence = self.queryData.loc[0, "sequence"]
        for index, base in enumerate(sequence):
            kmer = sequence[index : index + self.k]

            if len(kmer) >= self.k:
                if kmer not in kmerPool:
                    kmerPool[kmer] = [{index: index + self.k}]
                else:
                    kmerPool[kmer].append({index: index + self.k})
        return kmerPool

    def kmerPoolsToFile(self, queryKmerPool):

        # write reads and query kmerpool to files for analysis
        with open("data/logs/q-kmerPool.json", "w") as file:
            json.dump(queryKmerPool, file)

        with open("data/logs/r-kmerPool.json", "w") as file:
            json.dump(self.readsKmerPool, file)

    def createContigsInfo(self, queryKmerPool):
        # build contigsInfo to store: contig sequence, length of contig, query string kmers that exist in the contig (with location of kmer in contig)
        contigsInfo = []
        for contig in self.contigs:
            contigLen = len(contig)
            kmerCount = 0
            contigInfo = {"contig": contig, "length": contigLen, "q-kmers": []}
            for index, kmer in enumerate(queryKmerPool):
                if kmer in contig and kmer not in contigInfo["q-kmers"]:
                    kmerCount += 1
                    contigInfo["q-kmers"].append(
                        {
                            kmer: {
                                "index": [
                                    contig.index(kmer),
                                    contig.index(kmer) + self.k,
                                ]
                            }
                        }
                    )
            contigInfo["kmerCount"] = kmerCount
            contigsInfo.append(contigInfo)
        return contigsInfo

    def align(self):
        # break query string into kmers
        queryKmerPool = self.queryToKmers()
        # build contigsInfo (see method for description)
        contigsInfo = self.createContigsInfo(queryKmerPool)
        # find longest contig that contains the most query string kmers
        possibleBestContigs = []
        mostQKmers = 0
        longestContigMostQKmers = ""
        # find mostQKmers
        for contig in contigsInfo:
            if contig["kmerCount"] > mostQKmers:
                mostQKmers = contig["kmerCount"]

        for contig in contigsInfo:
            if contig["kmerCount"] == mostQKmers:
                possibleBestContigs.append(contig)

        chronologicalOrder = {}
        for contig in possibleBestContigs:
            for qkmer in contig["q-kmers"]:
                startIndex = list(qkmer.values())[0]["index"][0]
                if contig["contig"] not in chronologicalOrder:
                    chronologicalOrder[contig["contig"]] = [startIndex]
                else:
                    chronologicalOrder[contig["contig"]].append(startIndex)
        if len(chronologicalOrder) == 1:  # passed
            longestContigMostQKmers = list(chronologicalOrder.keys())[0]
        else:
            # minimum difference between starting indecies
            minDifference = float("inf")
            minContigs = []
            maxKmerCount = float("-inf")
            maxContig = None
            contigsInfoDict = {item["contig"]: item for item in contigsInfo}
            for contig, indices in chronologicalOrder.items():
                # Calculate the differences between consecutive elements
                diffs = [j - i for i, j in zip(indices[:-1], indices[1:])]
                # if the max difference is smaller than the current minimum, update tracking variables
                if max(diffs) < minDifference:
                    minDifference = max(diffs)
                    minContigs = [contig]

                # if the max difference is equal to the current minimum, add the contig to minContigs
                elif max(diffs) == minDifference:
                    minContigs.append(contig)

            # if there is a tie, find the longest contig in contigsInfo
            if len(minContigs) > 1:
                maxKmerCount = float("-inf")
                for contig in minContigs:
                    if contigsInfoDict[contig]["length"] > maxKmerCount:
                        maxKmerCount = contigsInfoDict[contig]["length"]
                        maxContig = contig
            longestContigMostQKmers = maxContig

        rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filePathALLELES = os.path.join(rootDir, "data/output/ALLELES.fasta")
        with open(filePathALLELES, "w") as file:
            file.write(longestContigMostQKmers)

        # find the reads that exist in each contig for ALLELES.fasta and output.aln
        readsInContig = []
        for read in self.readsKmerPool:
            if read in longestContigMostQKmers:
                readsInContig.append({read: self.readsKmerPool[read]})

        filePathReadsInContig = os.path.join(rootDir, "data/logs/readsInContig.json")
        with open(filePathReadsInContig, "w") as file:
            json.dump(readsInContig, file)
        return contigsInfo, longestContigMostQKmers, readsInContig

    def searchString(self):
        queryKmerPool = self.queryToKmers()
        self.kmerPoolsToFile(queryKmerPool=queryKmerPool)
        contigsInfo, longestContigMostQKmers, readsInContig = self.align()
        return contigsInfo, longestContigMostQKmers, readsInContig
