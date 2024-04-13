import pandas as pd
import numpy as np
import os
import time
import json
import argparse
import logging


from components.deBruijnGraph import DeBruijnGraph
from components.readsToKmers import ReadsToKmers
from components.createContigs import CreateContigs
from components.searchString import SearchString
from components.output import Output
from components.readsInContigs import numberOfReadsInContigs

logging.basicConfig(
    filename="data/logs/app.log", filemode="w", format="%(message)s", level=logging.INFO
)


def importData(queryFile, readsFile):
    query = ""
    reads = ""
    queryData = []
    readsData = []
    # os management for testing
    script_dir = os.path.dirname(__file__)  # get the directory of the current script
    queryFile = os.path.join(script_dir, queryFile)
    readsFile = os.path.join(script_dir, readsFile)

    # Import Query File Data
    with open(queryFile, "r") as inputQueryFile:
        query = inputQueryFile.readlines()
        for index, line in enumerate(query):
            # identify the line that has the id
            if ">" == line[0]:
                # get the query string and the id, then place into queryData
                queryString = query[index + 1]
                queryData.append(
                    {
                        "id": line.lstrip(">").rstrip("\n"),
                        "sequence": queryString.rstrip("\n"),
                    }
                )

    # Import Reads File Data
    with open(readsFile, "r") as inputReadsFile:
        reads = inputReadsFile.readlines()
        for index, line in enumerate(reads):
            # identify the lines that contain the reads id's
            if ">" == line[0]:
                # get the actual read from the proceeding line, then append read and its ID to readsData
                readString = reads[index + 1]
                readsData.append(
                    {
                        "id": line.lstrip(">").rstrip("\n"),
                        "sequence": readString.rstrip("\n"),
                    }
                )

    # convert queryData to dataframe and add a length column that is the length of the query string
    dfQueryData = pd.DataFrame(queryData)
    dfQueryData["length"] = dfQueryData["sequence"].str.len()

    # convert readsData to dataframe and add a length column that is the length of each read string
    dfReadsData = pd.DataFrame(readsData)
    dfReadsData["length"] = dfReadsData["sequence"].str.len()

    return dfQueryData, dfReadsData


def main():
    logging.info("Main: ")
    # arg setup and management
    parser = argparse.ArgumentParser(description="De Novo Genome Assembler")
    parser.add_argument("-k", type=int, help="Size of k", required=True)
    parser.add_argument(
        "--graph", type=bool, default=False, help="boolean: Show graph or not"
    )
    parser.add_argument(
        "--readsFile",
        type=str,
        default=None,
        help="Reads file for testing the number of reads in all contigs",
    )

    args = parser.parse_args()

    k = args.k
    showGraphArg = args.graph
    readsFile = args.readsFile
    dataDir = "./data"
    readsFileLocation = os.path.join(dataDir, readsFile)
    queryData, readsData = importData("./data/QUERY.fasta", readsFileLocation)
    logging.info(f"Number of reads from {readsFile}: {len(readsData)}")
    print(f"User defined k: {k}\n")
    logging.info(f"User defined size of k-mer: {k}\n")
    minR = readsData["length"].idxmin()
    maxR = readsData["length"].idxmax()
    minlen = readsData.loc[minR]
    maxlen = readsData.loc[maxR]

    logging.info(f"Shortest read: {minlen}\n")
    logging.info(f"Longest read: {maxlen}\n")

    rtkStart = time.time()
    readsToKmersInstance = ReadsToKmers(readsData=readsData, k=k)
    readsKmerPool, k = readsToKmersInstance.extractKmers()
    rtkStop = time.time()
    print(f"ReadsToKmer completed in: {rtkStop-rtkStart}\n")
    logging.info(f"ReadsToKmer completed in: {rtkStop-rtkStart}\n")

    dbgStart = time.time()
    debruijnGraphInstance = DeBruijnGraph(
        kmerPool=readsKmerPool, k=k, showGraphArg=showGraphArg
    )
    nodes, edges = debruijnGraphInstance.constructGraph()
    dbgStop = time.time()
    print(f"DeBruijnGraph completed in: {dbgStop-dbgStart}\n")
    logging.info(f"DeBruijnGraph completed in: {dbgStop-dbgStart}\n")

    ccStart = time.time()
    createContigsInstance = CreateContigs(graph=edges)
    contigs, allPaths = createContigsInstance.createContigs()
    ccStop = time.time()
    print(f"Create Contigs completed in: {ccStop-ccStart}\n")
    logging.info(f"Create Contigs completed in: {ccStop-ccStart}\n")

    ssStart = time.time()
    searchStringInstance = SearchString(
        queryData=queryData, contigs=contigs, readsKmerPool=readsKmerPool, k=k
    )
    contigsInfo, contig, readsInContig = searchStringInstance.searchString()
    with open("data/logs/contigsInfo.json", "w") as file:
        json.dump(contigsInfo, file)
    ssEnd = time.time()
    print(f"Search String completed in: {ssEnd-ssStart}\n")
    logging.info(f"Search String completed in: {ssEnd-ssStart}\n")

    # numberOfReadsInContigs(readsFile=readsFile) #utility function to get the number of reads that exist in each contig

    oStart = time.time()
    outputInstance = Output()
    outputInstance.createOutput()
    oEnd = time.time()
    print(f"Output file creation completed in: {oEnd-oStart}\n")
    logging.info(f"Output file creation completed in: {oEnd-oStart}\n")


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()

    logging.info(f"Total Runtime: {end-start}\n")
    print(f"\nTotal Runtime: {end-start}\n")
