import unittest
import sys
# add parent directory to python path
sys.path.insert(0, '../')
from src.main import main
import unittest
import sys
import os
import main

class TestImportData(unittest.TestCase):
    def test_file_not_found(self):
        queryFile = "nonexistent_file.txt"
        readsFile = "reads.txt"
        with self.assertRaises(FileNotFoundError):
            main.importData(queryFile, readsFile)

    def test_empty_file(self):
        queryFile = "empty_file.txt"
        readsFile = "reads.txt"
        # Create an empty file
        open(queryFile, 'w').close()
        with self.assertRaises(ValueError):
            main.importData(queryFile, readsFile)
        # Remove the empty file
        os.remove(queryFile)

    def test_fasta_file(self):
        queryFile = "query.fasta"
        readsFile = "reads.txt"
        # Create a .fasta file
        with open(queryFile, 'w') as file:
            file.write(">sequence1\n")
            file.write("ATCGATCG\n")
            file.write(">sequence2\n")
            file.write("GCTAGCTA\n")
        # Test the importData function
        main.importData(queryFile, readsFile)
        # Remove the .fasta file
        os.remove(queryFile)

if __name__ == '__main__':
    unittest.main()
