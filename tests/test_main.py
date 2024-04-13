import unittest
import pandas as pd
import os
import sys


# Get the directory of main.py
mainDir = os.path.dirname(os.path.abspath("../src/main.py"))
# Append the directory of main.py to the system path
sys.path.append(mainDir)
os.chdir(mainDir)
from main import importData


class TestImportData(unittest.TestCase):

    def setUp(self):
        self.queryFile = os.path.join(
            os.path.dirname(__file__), "../src/data/QUERY.fasta"
        )
        self.readsFile = os.path.join(
            os.path.dirname(__file__), "../src/data/DummyReads.fasta"
        )

    def testImportData(self):
        dfQueryData, dfReadsData = importData(self.queryFile, self.readsFile)

        # Check if the function returns two dataframes
        self.assertIsInstance(dfQueryData, pd.DataFrame)
        self.assertIsInstance(dfReadsData, pd.DataFrame)

        # Check if the dataframes have the expected columns
        self.assertEqual(list(dfQueryData.columns), ["id", "sequence", "length"])
        self.assertEqual(list(dfReadsData.columns), ["id", "sequence", "length"])


if __name__ == "__main__":
    unittest.main()
