import unittest
import sys
sys.path.insert(0, '../src/components')
from deBruijnGraph import DeBruijnGraph

class TestDeBruijnGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.showGraphArg = False
        self.kmerPool = {
                'ACGTACGTA': {2: [{0: 9}], 3: [{0: 9}]}, 
                'CGTACGTAC': {2: [{1: 10}], 3: [{1: 10}]},
                'GCACGTACG': {1: [{0:9}]},
                'CACGTACGT': {1: [{1:10}]},
                'ACGTACGTT': {1: [{2:11}]},
                'CGTACGTTT': {1: [{3:12}]},
            }
        self.k = 9
        self.dbg = DeBruijnGraph(self.kmerPool, self.k, self.showGraphArg) 
    
    def testGetPrefixSuffix(self):
        kmer = 'ACGTACGTA'
        prefix, suffix = self.dbg.getPrefixSuffix(kmer)
        self.assertEqual(prefix, 'ACGTACGT')
        self.assertEqual(suffix, 'CGTACGTA')
        self.assertEqual(self.k-1, len(prefix))
        self.assertEqual(self.k-1, len(suffix))
    def testPresenceInGraph(self):
        nodes, edges = self.dbg.constructGraph()
        for kmer in self.kmerPool:
            prefix, suffix = self.dbg.getPrefixSuffix(kmer)
            self.assertIn((prefix, suffix), edges)

if __name__ == '__main__':
    unittest.main()