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
        mostQKmers = 0
        longestContig = 0
        longestContigMostQKmers = ""
        for contig in contigsInfo:
            if contig['kmerCount'] > mostQKmers or (contig['kmerCount'] == mostQKmers and contig['length']>longestContig):
                mostQKmers = contig['kmerCount']
                longestContig = contig['length']
                longestContigMostQKmers = contig
        with open("data/output/ALLELES.fasta", 'w') as file:
            file.write(longestContigMostQKmers['contig'])

        # find the reads that exist in each contig for ALLELES.fasta and output.aln
        readsInContig = []
        for read in self.readsKmerPool:
            if read in longestContigMostQKmers['contig']:
                readsInContig.append({read:self.readsKmerPool[read]})
        with open("data/logs/readsInContig.json", "w") as file:
            json.dump(readsInContig, file)
                   

        return contigsInfo, longestContigMostQKmers, readsInContig


