import unittest
import pandas as pd
import os
import sys

# os management for testing
mainDir = os.path.dirname(os.path.abspath("../src/main.py"))
sys.path.append(mainDir)
os.chdir(mainDir)

from main import importData


class TestImportData(unittest.TestCase):

    def setUp(self):
        # os management for locating files needed for testing
        self.queryFile = os.path.join(
            os.path.dirname(__file__), "../src/data/QUERY.fasta"
        )
        self.readsFile = os.path.join(
            os.path.dirname(__file__), "../src/data/DummyReads.fasta"
        )

    def testImportData(self):
        dfQueryData, dfReadsData = importData(self.queryFile, self.readsFile)

        # verify query and reads data are in pd dataframes
        self.assertIsInstance(dfQueryData, pd.DataFrame)
        self.assertIsInstance(dfReadsData, pd.DataFrame)

        # verify columns of dataframes
        self.assertEqual(list(dfQueryData.columns), ["id", "sequence", "length"])
        self.assertEqual(list(dfReadsData.columns), ["id", "sequence", "length"])


if __name__ == "__main__":
    unittest.main()
