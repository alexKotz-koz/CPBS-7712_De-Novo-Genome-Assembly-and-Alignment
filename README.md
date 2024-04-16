# De Novo Genome Assembly and Alignment
> Goal: Find the longest contig that contains a query sequence given a set of next generation sequence reads. 

**The assignment for this homework:** _Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence._

The outline of this project is as follows:
- Read in a set of next generation sequence (NGS) reads and a query sequence.
- Break each of the NGS sequence reads into k-mers (all possible substrings of length k that are contained in a string).
- Construct a [De Bruijn Graph](https://en.wikipedia.org/wiki/De_Bruijn_graph) using the prefix and suffix of each k-mer. [Concept Overview](https://www.youtube.com/watch?v=TNYZZKrjCSk&list=PL2mpR0RYFQsBiCWVJSvVAO3OJ2t7DzoHA&index=51). 
- Construct contigs (contiguous sequences) by following all possible paths through the De Brujin Graph.
- Search each contig for the query string.
- Return the longest contig that contains the query string.

## Installation

OS X & Linux:
1. Clone or download the repository.
2. Set up miniconda environment:
    - If miniconda is not installed on the local machine, please follow the steps outlined here before continuing: [Miniconda installation](https://docs.anaconda.com/free/miniconda/)
    - Once miniconda is installed, create the conda environment by copying this command into a shell (terminal) with an active base conda environment:
        ```sh
        conda env create -f conda_env.yml
        ```
    - Then activate the new conda environment:
        ```sh
        conda activate conda_env
        ```

## Usage example
- A sample dataset has been provided for this project (READS.fasta and QUERY.fasta). These files are located in /src/data.
- If testing this project with a different set of NGS reads and a query sequence, please replace these two files in /src/data with your new READS.fasta and QUERY.fasta files and name these files accordingly. 

1. Open a terminal and navigate to /src/:
```sh
cd src
```
2. Use the following command to run the project:
```sh
python3 main.py [options]
```
Options:
- `-h, --help`: Show help menu
- `-k`: Size of k (required)
- `-readsFile`: Reads file to use for the project, assumed fasta format (required) 
- `--graph`: Show graph or not (optional)

- Note: Visualizing a large graph will take a significant amount of time to generate. Recommended to visualize a subset of the original data for reasonable execution time. 

## Requirements
- Python 3.9 or higher. 
    - This project has been tested with python 3.9 thru 3.12.
- Miniconda (see Installation section for further instructions).
- macOS or Linux based operating system.

## Note on the output files available in data/logs and data/output:
To compensate for GitHubs file size storage limit all files under the data/logs and data/output directories were generated via: 
```{sh}
python3 main.py -k 5 -readsFile DummyReads.fasta
```
