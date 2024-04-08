from components.readsToKmers import ReadsToKmers
import json
class SearchString:
    def __init__(self, queryData, readsKmerPool, contigs, k):
        self.queryData = queryData
        self.contigs = contigs
        self.readsKmerPool = readsKmerPool
        self.k = k
    
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
        queryKmerPool = self.queryToKmers()

        kmerMatchCount = 0

        print(f"Number of q kmers: {len(queryKmerPool)}")
        print(f"Number of r kmers: {len(self.readsKmerPool)}")

        with open("q-kmerPool.json", "w") as file:
            json.dump(queryKmerPool, file)

        with open("r-kmerPool.json", "w") as file:
            json.dump(self.readsKmerPool, file)

        qkeys = set(queryKmerPool.keys())
        rkeys = set(self.readsKmerPool.keys())
        kmerMatchCount = qkeys & rkeys
        print(f"Total number of q kmers in r kmerpool: {len(kmerMatchCount)}")

        for contig in self.contigs:
            for kmer in queryKmerPool:
                if kmer in contig:
                    print("here")
                    print(kmer)
        




