import unittest
import sys
import pandas as pd
sys.path.insert(0, '../')
from src.components.reads_to_kmers import ReadsToKmers

class TestReadsToKmers(unittest.TestCase):
    def setUp(self):
        # Create a sample readsData DataFrame for testing
        self.readsData = pd.DataFrame({
            'id': [1, 2, 3],
            'read': ['ACGTACGTAC', 'ACGTACGTAC', 'ACGTACGTAC']
        })
        #print(self.readsData)

    def test_extract_kmers(self):
        # Create an instance of ReadsToKmers
        rtk = ReadsToKmers(self.readsData)
        kmerPool, k = rtk.extract_kmers()
        self.check_kmerPool(kmerPool=kmerPool)
        self.check_k(k=k)

    def check_kmerPool(self, kmerPool):
        self.assertDictEqual(kmerPool,{'ACGTACGTAC':{1:1,2:1,3:1}})

    def check_k(self, k):
        self.assertEqual(k, 10)
        #print(kmerPool)
        #print(k)

        # Assert the expected output
        # TODO: Add your assertions here

if __name__ == '__main__':
    unittest.main()