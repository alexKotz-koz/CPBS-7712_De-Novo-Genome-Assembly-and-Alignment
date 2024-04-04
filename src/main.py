import pandas as pd
import numpy as np
import os
import time
import sys
import argparse

from components.deBruijnGraph import DeBruijnGraph
from components.readsToKmers import ReadsToKmers
from components.createContigs import CreateContigs
from components.searchString import SearchString
from reads_in_contigs import numberOfReadsInContigs

def importData(queryFile, readsFile):
    query = ""
    reads = ""
    queryData = []
    readsData = []
    script_dir = os.path.dirname(__file__)  # get the directory of the current script
    queryFile = os.path.join(script_dir, queryFile)
    readsFile = os.path.join(script_dir, readsFile)
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


def main():

    parser = argparse.ArgumentParser(description="De Novo Genome Assembler")
    parser.add_argument('-k', type=int, help='Size of k', required=True)
    parser.add_argument('--graph', type=bool, default=False, help='boolean: Show graph or not')
    parser.add_argument('--readsFile', type=str, default=None,help='Reads file for testing the number of reads in all contigs')

    args = parser.parse_args()

    k = args.k
    showGraphArg = args.graph
    readsFile = args.readsFile

    queryData, readsData = importData("./data/chatgptTestData/QUERY copy.fasta", './data/READS_Subset.fasta')
    print(f"User defined k: {k}\n")
    minR = readsData['length'].idxmin()
    maxR = readsData['length'].idxmax()
    minlen = readsData.loc[minR]
    maxlen = readsData.loc[maxR]
    print(minlen)
    print(maxlen)
    rtkStart = time.time()
    readsToKmersInstance = ReadsToKmers(readsData=readsData, k=k)
    kmerPool, k = readsToKmersInstance.extractKmers()
    rtkStop = time.time()
    print(f"ReadsToKmer completed in: {rtkStop-rtkStart}\n")

    dbgStart = time.time()
    debruijnGraphInstance = DeBruijnGraph(kmerPool=kmerPool, k=k, showGraphArg=showGraphArg)
    nodes, edges = debruijnGraphInstance.constructGraph()
    dbgStop = time.time()
    print(f"DeBruijnGraph completed in: {dbgStop-dbgStart}\n")
    #print("In Main after DBG, nodes: ", nodes)
    #print("In Main after DBG, edges: ", edges)

    ccStart = time.time()
    createContigsInstance = CreateContigs(graph=edges)
    createContigsInstance.createContigs()
    ccStop = time.time()
    print(f"Create Contigs completed in: {ccStop-ccStart}\n")

    numberOfReadsInContigs(readsFile=readsFile)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"\nTotal Runtime:{end-start}\n")
