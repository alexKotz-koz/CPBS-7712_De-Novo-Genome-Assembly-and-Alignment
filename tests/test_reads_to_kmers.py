import unittest
import pandas as pd
# Manually navigate to /src/, for importing of ReadsToKmers class
import sys
sys.path.insert(0, '../src/components')
from readsToKmers import ReadsToKmers

class TestReadsToKmers(unittest.TestCase):
    def setUp(self):
        # Create a sample readsData DataFrame for testing
        self.readsData = pd.DataFrame({
            'id': [1, 2, 3],
            'read': ['GCACGTACGTTT', 'ACGTACGTAC', 'ACGTACGTAC']
        })
        #print(self.readsData)

    # parent test
    def testExtractKmers(self):
        rtk = ReadsToKmers(self.readsData)
        kmerPool, k = rtk.extractKmers()

        self.checkKmerPool(kmerPool=kmerPool)
        self.checkK(k=k)

    # child test: 
        # kmerPool structure = {'kmer': {readID1: [{start index in read: stop index in read}]}}
        # every possible kmer is in the kmer pool
    def checkKmerPool(self, kmerPool):
        self.assertDictEqual(kmerPool,
            {
                'ACGTACGTA': {2: [{0: 9}], 3: [{0: 9}]}, 
                'CGTACGTAC': {2: [{1: 10}], 3: [{1: 10}]},
                'GCACGTACG': {1: [{0:9}]},
                'CACGTACGT': {1: [{1:10}]},
                'ACGTACGTT': {1: [{2:11}]},
                'CGTACGTTT': {1: [{3:12}]},
            }
        )

    # child test: kmer length is static and consistent across all kmers
    def checkK(self, k):
        self.assertEqual(k, 9)

if __name__ == '__main__':
    unittest.main()