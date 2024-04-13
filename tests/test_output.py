import unittest
import pandas as pd
import os
import sys
import shutil

sys.path.insert(0, "../src/components")
from output import Output


class TestOutput(unittest.TestCase):
    # create directory for temp output.aln file
    def setUp(self):
        self.outputInstance = Output()

    def testCeateOutput(self):
        # os management for creating and checking output.aln file
        originalCwd = os.getcwd()
        os.chdir(os.path.join(originalCwd, "../src"))
        self.outputInstance.createOutput()
        os.chdir(originalCwd)

        rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        outputFilePath = os.path.join(rootDir, "src/data/output/output.aln")
        self.assertTrue(os.path.exists(outputFilePath))

        numRows = 9  # hard coded for the following argument set (py main.py -k 5 --readsFile DummyReads.fasta)
        outputDf = pd.read_csv(outputFilePath)
        self.assertEqual(len(outputDf), numRows)


if __name__ == "__main__":
    unittest.main()
