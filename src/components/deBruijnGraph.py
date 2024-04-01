import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class DeBruijnGraph:
    def __init__(self, kmerPool, k, showGraphArg):
        self.kmerPool = kmerPool
        self.k = k
        self.showGraphArg = showGraphArg

    # Input: individual kmer
    # Output: prefix and suffix of kmer
    def getPrefixSuffix(self, kmer):
        # get the length of the prefix/suffix
        length = self.k-1
        # get the first <length> characters of the kmer for the prefix
        prefix = kmer[:length]
        # get the last <length> characters of the kmer for the suffix
        suffix = kmer[-length:]
        return prefix, suffix
    
    # Input: kmerPool (contains all unique kmers found in the reads, the read id's where each kmer exists, and the position of each kmer in each read)
    # Output: nodes (a set containing all unique nodes), edges (a list containing tuples of source->target nodes)
    def constructGraph(self):
        kmerPool = self.kmerPool
        edges = {}
        edges2 = []
        edges3 = {}
        edges4 = {}
        nodes = set()
        
        # get the prefix and suffix of each kmer and add to the nodes and edges data structures
        for kmer in kmerPool:
            prefix, suffix = self.getPrefixSuffix(kmer)
            
            edges[(prefix,suffix)] = kmerPool[kmer]
            edges2.append((prefix,suffix))
            if not edges3.get(prefix):
                edges3[prefix] = [suffix]
            else:
                edges3[prefix].append(suffix)

            if prefix not in edges4:
                edges4[prefix] = [suffix]
            else:
                edges4[prefix].append(suffix)

            nodes.add(prefix)
            nodes.add(suffix)
        # logic to visualize the graph, if "True" is pass with the run command (python3 main.py True) then the graph is shown
        if self.showGraphArg == "True":
            Graph = nx.MultiDiGraph()
            for i in nodes:
                Graph.add_node(i)
                Graph.add_edges_from(edges)
            nx.draw(Graph, with_labels=True)
            plt.show()
        
        return nodes, edges3

        


        
    
        