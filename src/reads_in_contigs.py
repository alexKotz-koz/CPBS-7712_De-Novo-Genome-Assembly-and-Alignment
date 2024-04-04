import subprocess
import os

def numberOfReadsInContigs(readsFile):
    data = 'data/'
    if readsFile == None:
        readsFile = 'READS_Subset.fasta'
    reads = os.path.join(data, readsFile)
    # Open the contigs file
    with open('contigs.txt', 'r') as contigs_file:
        contigs = contigs_file.readlines()
    total = []
    # For each contig, count the number of matching reads
    for i, contig in enumerate(contigs):
        contig = contig.strip()  # Remove newline characters
        
        # Use grep to count the number of matching reads
        command = f"grep -c '{contig}' {reads}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result = int(result.stdout.strip())
        
        total.append(result)

        # Print the number of reads for this contig
    print(f"{sum(total)} reads in {len(total)} contigs")