import os

def import_reads(readsFileInput):
    readsData = []
    file = readsFileInput
    readsFile =f"data/{file}"
    with open(readsFile, "r") as inputReadsFile:
        reads = inputReadsFile.readlines()
        for index, line in enumerate(reads):
            # identify the lines that contain the reads id's
            if ">" == line[0]:
                # get the actual read from the proceeding line, then append read and its ID to readsData
                readString = reads[index+1]
                readsData.append(readString.rstrip('\n'))
    return readsData

def numberOfReadsInContigs(readsFile):
    if readsFile == None:
        print("No reads file provided, using default reads file")
        readsFile = 'READS_Subset.fasta'
    readsFile = (readsFile, True)
    readsData = import_reads(readsFile)
    # Open the contigs file
    with open('contigs.txt', 'r') as contigs_file:
        contigs = [line.strip() for line in contigs_file.readlines()]
    total = []
    # For each contig, count the number of matching reads
    for read in readsData:
        if read in contigs:
            total.append(1)

        # Print the number of reads for this contig
    print(f"{sum(total)} reads in {len(total)} contigs")