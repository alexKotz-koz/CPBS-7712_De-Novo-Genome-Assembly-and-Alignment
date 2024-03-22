import pandas as pd
import numpy as np
import os
import time
import sys

from components.deBruijnGraph import DeBruijnGraph
from components.readsToKmers import ReadsToKmers
from components.createContigs import CreateContigs

def importData(queryFile, readsFile):
    query = ""
    reads = ""
    queryData = []
    readsData = []

    # Import Query File Data
    with open(queryFile, "r") as inputQueryFile:
        query = inputQueryFile.readlines()
        for index,line in enumerate(query):
            # identify the line that has the id
            if ">" == line[0]:
                # get the query string and the id, then place into queryData
                queryString = query[index+1]
                queryData.append({"id":line.lstrip('>').rstrip('\n'), "query": queryString.rstrip('\n')})
    
    #Import Reads File Data
    with open(readsFile, "r") as inputReadsFile:
        reads = inputReadsFile.readlines()
        for index,line in enumerate(reads):
            # identify the lines that contain the reads id's
            if ">" == line[0]:
                # get the actual read from the proceeding line, then append read and its ID to readsData
                readString = reads[index+1]
                readsData.append({"id":line.lstrip('>').rstrip('\n'), "read": readString.rstrip('\n')})
    
    #convert queryData to dataframe and add a length column that is the length of the query string
    dfQueryData = pd.DataFrame(queryData)
    dfQueryData['length'] = dfQueryData['query'].str.len()
    
    #convert readsData to dataframe and add a length column that is the length of each read string
    dfReadsData = pd.DataFrame(readsData)
    dfReadsData['length'] = dfReadsData['read'].str.len()


    return dfQueryData, dfReadsData


def main(showGraphArg=None):
    queryData, readsData = importData("./data/chatgptTestData/QUERY copy.fasta", './data/chatgptTestData/READS.fasta')

    minR = readsData['length'].idxmin()
    maxR = readsData['length'].idxmax()
    minlen = readsData.loc[minR]
    maxlen = readsData.loc[maxR]
    #print(minlen)
    #print(maxlen)
    #print(readsData.head())

    readsToKmersInstance = ReadsToKmers(readsData=readsData)
    #kmerPool = kmer table from reads
    #k = size of the kmers
    kmerPool, k = readsToKmersInstance.extractKmers()

    debruijnGraphInstance = DeBruijnGraph(readsData=readsData, queryData=queryData, kmerPool=kmerPool, k=k, showGraphArg=showGraphArg)
    nodes, edges = debruijnGraphInstance.constructGraph()

    createContigsInstance = CreateContigs(graph=edges)
    createContigsInstance.createContigs()

if __name__ == "__main__":
    start = time.time()
    arg1 = sys.argv[1] if len(sys.argv) > 1 else ''
    main(arg1)
    end = time.time()
    print(f"Total Runtime:{end-start}")
