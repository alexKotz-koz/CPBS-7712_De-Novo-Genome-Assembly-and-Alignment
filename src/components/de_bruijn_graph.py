import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class DeBruijnGraph:
    def __init__(self, readsData, queryData, kmerPool, k):
        self.readsData = readsData
        self.queryData = queryData
        self.kmerPool = kmerPool
        self.k = k
        print(kmerPool)
    
    def getPrefixSuffix(self, kmer):
        length = self.k-1
        prefix = kmer[:length]
        suffix = kmer[-length:]
        return prefix, suffix
        # return node
    
    def construct_graph(self):
        kmerPool = self.kmerPool
        #print(kmerPool.keys())
        k = self.k
        edges = []
        nodes = set()
        
        for kmer in kmerPool:
            prefix, suffix = self.getPrefixSuffix(kmer)
            edges.append((prefix,suffix))
            nodes.add(prefix)
            nodes.add(suffix)
        print(nodes)
        print(edges)

        Graph = nx.MultiDiGraph()
        for i in nodes:
            Graph.add_node(i)

        Graph.add_edges_from(edges)
        nx.draw(Graph, with_labels=True)
        plt.show()

        
    
        