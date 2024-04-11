from components.readsToKmers import ReadsToKmers
import json
import pandas as pd
class SearchString:
    def __init__(self, queryData, readsKmerPool, contigs, k):
        self.queryData = queryData
        self.contigs = contigs
        self.readsKmerPool = readsKmerPool
        self.k = 10
    
    def queryToKmers(self):
        #kmersInstance = ReadsToKmers(readsData=self.queryData, k=self.k)
        #queryKmerPool, k = kmersInstance.extractKmers()
        kmerPool = {}
        sequence = self.queryData.loc[0, 'sequence']
        for index, base in enumerate(sequence):
                
            # kmer = substring of the sequence (iteration number (index) to the index + k)
            kmer = sequence[index:index+self.k]
            
            # check if the new kmer is greater than or equal to the set size of k
            if len(kmer) >= self.k:
                
                # if so, check to see if the kmer exists in kmerPool
                if kmer not in kmerPool:
                    kmerPool[kmer] = [{index:index+self.k}]
                else:
                    kmerPool[kmer].append({index:index+self.k})
        return kmerPool
            
    
    def align(self):
        # break query string into kmers
        queryKmerPool = self.queryToKmers()

        kmerMatchCount = 0

        print(f"Number of q kmers: {len(queryKmerPool)}")
        print(f"Number of r kmers: {len(self.readsKmerPool)}")

        # write read and query kmerpool to files for analysis
        with open("data/logs/q-kmerPool.json", "w") as file:
            json.dump(queryKmerPool, file)

        with open("data/logs/r-kmerPool.json", "w") as file:
            json.dump(self.readsKmerPool, file)

        # check number of kmers that exist in both kmerpools
        qkeys = set(queryKmerPool.keys())
        rkeys = set(self.readsKmerPool.keys())
        kmerMatchCount = qkeys & rkeys
        print(f"Total number of q kmers in r kmerpool: {len(kmerMatchCount)}")


        # build contigsInfo to store: contig sequence, length of contig, query string kmers that exist in the contig (with location of kmer in contig)
        contigsInfo = []
        for contig in self.contigs:
            contigLen = len(contig)
            kmerCount = 0
            contigInfo = {'contig': contig, 'length': contigLen, 'q-kmers':[]}
            for index, kmer in enumerate(queryKmerPool):
                if kmer in contig and kmer not in contigInfo['q-kmers']:
                    kmerCount += 1
                    print(f"start index of kmer: {contig.index(kmer)}")
                    contigInfo['q-kmers'].append({kmer:{'index':[contig.index(kmer),contig.index(kmer)+self.k]}})
                    print(kmer)
            contigInfo['kmerCount'] = kmerCount
            contigsInfo.append(contigInfo)

        # find longest contig that contains the most query string kmers
        possibleBestContigs = []
        mostQKmers = 0
        longestContig = 0
        longestContigMostQKmers = ""
        # find mostQKmers 
        for contig in contigsInfo:
            if contig['kmerCount'] > mostQKmers: #or (contig['kmerCount'] == mostQKmers and contig['length']>longestContig) :
                mostQKmers = contig['kmerCount']

        for contig in contigsInfo:
            if contig['kmerCount'] == mostQKmers:
                possibleBestContigs.append(contig)
        
        chronologicalOrder = {}
        for contig in possibleBestContigs:
            for i, qkmer in enumerate(contig['q-kmers']):
                startIndex = list(qkmer.values())[0]['index'][0]
                if contig['contig'] not in chronologicalOrder:
                    chronologicalOrder[contig['contig']] = [startIndex]
                else:
                    chronologicalOrder[contig['contig']].append(startIndex)
        if len(chronologicalOrder) == 1: #passed
            longestContigMostQKmers = list(chronologicalOrder.keys())[0]
        else:
            #minimum difference between starting indecies 
            minDifference = float('inf')
            minContigs = []

            contigsInfoDict = {item['contig']: item for item in contigsInfo}
            
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
            
            # if there is a tie, find the contig in contigsInfo
            if len(minContigs) > 1:
                maxKmerCount = float('-inf')
                maxContig = None

                for contig in minContigs:
                    if contigsInfoDict[contig]['kmerCount'] > maxKmerCount:
                        maxKmerCount = contigsInfoDict[contig]['kmerCount']
                        maxContig = contig

            longestContigMostQKmers = maxContig            

    
        with open("data/output/ALLELES.fasta", 'w') as file:
            file.write(longestContigMostQKmers)

        # find the reads that exist in each contig for ALLELES.fasta and output.aln
        readsInContig = []
        for read in self.readsKmerPool:
            if read in longestContigMostQKmers:
                readsInContig.append({read:self.readsKmerPool[read]})
        with open("data/logs/readsInContig.json", "w") as file:
            json.dump(readsInContig, file)
                   

        return contigsInfo, longestContigMostQKmers, readsInContig


