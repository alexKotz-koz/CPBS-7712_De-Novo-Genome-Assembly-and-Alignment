class ReadsToKmers:
    def __init__(self, readsData, k):
        self.readsData = readsData
        self.k = int(k)

    # Input: Reads data
    # Ouput: kmerPool and k (length of kmers)
    def extractKmers(self):
        # kmerPool structure = {<kmer>: {readId: location of the kmer in the read}}
        kmerPool = {}
        readsData = self.readsData
        k = self.k

        for index, read in readsData.iterrows():
            # get the id and read from each row pair
            id = read['id']
            sequence = read['read']
            for index, base in enumerate(sequence):
                # kmer = substring of the sequence (iteration number (index) to the index + k)
                kmer = sequence[index:index+k]
                # check if the new kmer is greater than or equal to the set size of k
                if len(kmer) >= k:
                    # if so, check to see if the kmer exists in kmerPool
                    if kmer not in kmerPool:
                        kmerPool[kmer] = {}
                    # if the read id is not in the kmer subdictionary, add the read id and the location of the kmer in the read to the kmer subdictionary
                    if id not in kmerPool[kmer]:
                        kmerPool[kmer][id] = [{index:index+k}]
                    else:
                        kmerPool[kmer][id].append({index:index+k})
        return kmerPool, k    
    
