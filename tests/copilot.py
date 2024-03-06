import pandas as pd

# Test Case 1: Valid input files
queryFile = "/path/to/query.txt"
readsFile = "/path/to/reads.txt"
dfQueryData, dfReadsData = importData(queryFile, readsFile)
assert isinstance(dfQueryData, pd.DataFrame)
assert isinstance(dfReadsData, pd.DataFrame)

# Test Case 2: Empty input files
queryFile = "/path/to/empty_query.txt"
readsFile = "/path/to/empty_reads.txt"
dfQueryData, dfReadsData = importData(queryFile, readsFile)
assert dfQueryData.empty
assert dfReadsData.empty

# Test Case 3: Non-existent input files
queryFile = "/path/to/nonexistent_query.txt"
readsFile = "/path/to/nonexistent_reads.txt"
dfQueryData, dfReadsData = importData(queryFile, readsFile)
assert dfQueryData is None
assert dfReadsData is None

# Test Case 4: Invalid input files (e.g., not in FASTA format)
queryFile = "/path/to/invalid_query.txt"
readsFile = "/path/to/invalid_reads.txt"
dfQueryData, dfReadsData = importData(queryFile, readsFile)
assert dfQueryData is None
assert dfReadsData is None