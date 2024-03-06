class ReadsToKmers:
    def __init__(self, readsData):
        self.readsData = readsData
        self.k = 9

    def extract_kmers(self):
        # kmerPool structure = {<kmer>: {readId: number of times the kmer is in this read}}
        kmerPool = {}
        readsData = self.readsData
        k = self.k
        
        # iterate over each of the reads in the readsData
        for index, read in readsData.iterrows():
            # get the id and read from each row pair
            id = read['id']
            sequence = read['read']
            # for each base in the sequence(read)
            for index, base in enumerate(sequence):
                # kmer = substring of the sequence (iteration number (index) to the index + k)
                kmer = sequence[index:index+k]
                # check if the new kmer is greater than or equal to the set size of k
                if len(kmer) >= k:
                    # if so, check to see if the kmer exists in kmerPool
                    if kmer not in kmerPool:
                        kmerPool[kmer] = {}
                    # if the read id is not in the kmer subdictionary, add the read id to the kmer subdictionary and set the count to 1
                    if id not in kmerPool[kmer]:
                        kmerPool[kmer][id] = 1
                    # the read id is in the kmer subdictionary so increment the count (resulting in a number representing the total number of times the kmer exists in the read)
                    else:
                        kmerPool[kmer][id] += 1
                    
        #print(f"\nstructure of kmerPool ... <kmer>: <readId>:<count of kmer in pool> \n\n kmerPool: {kmerPool}")
        #print(len(kmerPool))
        '''# Sort the kmerPool by the number of unique ids associated with each kmer
        sorted_kmerPool = sorted(kmerPool.items(), key=lambda item: len(item[1]))

        # The kmer that appears most is the last item in the sorted list
        most_common_kmer, ids = sorted_kmerPool[-1]

        print(f"The kmer that appears most is: {most_common_kmer}")     '''   
        return kmerPool, k    