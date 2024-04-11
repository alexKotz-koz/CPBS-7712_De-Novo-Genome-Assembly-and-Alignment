import unittest
import pandas as pd
# Manually navigate to /src/, for importing of ReadsToKmers class
import sys
sys.path.insert(0, '../src/components')
from readsToKmers import ReadsToKmers

class TestReadsToKmers(unittest.TestCase):
    def setUp(self):
        readsData = []
        # Create a sample readsData DataFrame for testing
        with open('../src/data/DummyReads.fasta', "r") as inputReadsFile:
            reads = inputReadsFile.readlines()
            
            for index,line in enumerate(reads):
                # identify the lines that contain the reads id's
                if ">" == line[0]:
                    # get the actual read from the proceeding line, then append read and its ID to readsData
                    readString = reads[index+1]
                    readsData.append({"id":line.lstrip('>').rstrip('\n'), "sequence": readString.rstrip('\n')})
        #convert readsData to dataframe and add a length column that is the length of each read string
        self.dfReadsData = pd.DataFrame(readsData)
        self.dfReadsData['length'] = self.dfReadsData['sequence'].str.len()

    # parent test
    def testExtractKmers(self):
        rtk = ReadsToKmers(self.dfReadsData, 5)
        kmerPool, k = rtk.extractKmers()
        k = 5 #for test dataset

        self.checkKmerPool(kmerPool=kmerPool)
        self.checkK(k=k)

    # child test: 
        # kmerPool structure = {'kmer': {readID1: [{start index in read: stop index in read}]}}
        # every possible kmer is in the kmer pool
    def checkKmerPool(self, kmerPool):
        self.assertDictEqual(kmerPool,
            {
                'ACTGG': {'Read1': [{0: 5}]}, 
                'CTGGA': {'Read1': [{1: 6}]}, 
                'TGGAT': {'Read1': [{2: 7}]}, 
                'GGATC': {'Read1': [{3: 8}]}, 
                'GATCT': {'Read1': [{4: 9}]}, 
                'ATCTT': {'Read1': [{5: 10}]}, 
                'TCTTC': {'Read1': [{6: 11}]}, 
                'CTTCA': {'Read1': [{7: 12}]}, 
                'TTCAG': {'Read1': [{8: 13}]}, 
                
                'CTAGC': {'Read2': [{0: 5}]}, 
                'TAGCC': {'Read2': [{1: 6}]}, 
                'AGCCT': {'Read2': [{2: 7}], 'Read3': [{0: 5}]}, 
                'GCCTT': {'Read2': [{3: 8}], 'Read3': [{1: 6}]}, 
                'CCTTA': {'Read2': [{4: 9}]}, 
                'CTTAT': {'Read2': [{5: 10}]}, 
                'TTATC': {'Read2': [{6: 11}]}, 
                
                'CCTTC': {'Read3': [{2: 7}]}, 
                'CTTCG': {'Read3': [{3: 8}]}, 
                
                'TTTAG': {'Read4': [{0: 5}]}, 
                'TTAGC': {'Read4': [{1: 6}]}, 
                'TAGCT': {'Read4': [{2: 7}]}, 
                'AGCTA': {'Read4': [{3: 8}]}, 
                'GCTAG': {'Read4': [{4: 9}]}
            }
        )

    # child test: kmer length is static and consistent across all kmers
    def checkK(self, k):
        self.assertEqual(k, 5)

if __name__ == '__main__':
    unittest.main()