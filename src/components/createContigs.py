import pandas as pd
from itertools import dropwhile
class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.finalGraph = []
        self.allPaths = []

    # Input: edge list from readsToKmers
    # Output: a list of all start nodes (nodes that only have outgoing edges)
    def findStartNodes(self, inputGraph):
        ## TODO: Will need to optimize for larger dataset
        #calculate the in and out degrees for each node
        edgesCount = {}
        startNodes = []
        for edge in inputGraph.items():
            #print('edge', edge)
            #print('edge[0]: ',edge[0])
            
            #print('edge[1]: ', edge[1])
            # first node in the tuple has an outgoing edge
            if edge[0] in edgesCount:
                edgesCount[edge[0]][1] += 1
            else:
                edgesCount[edge[0]] = [0,1] #[incoming, outgoing]
            
            for suffix in edge[1]:
                #print('suffix: ', suffix)
                if suffix in edgesCount:
                    edgesCount[suffix][0] += 1
                else:
                    edgesCount[suffix] = [1,0]
            
        
        for edge in edgesCount.items():
            if edge[1][0] == 0:
                startNodes.append(edge[0])
            
            
        #print("edgecount: ", edgesCount)
        # Initialize a list to store the start edges

        '''# Iterate over the edges
        for edge in inputGraph:
            # If the first node in the edge is not in edges_count or has zero incoming edges
            if edge[0] not in edgesCount or edgesCount[edge[0]][0] == 0:
                # Add the edge to the start_edges list
                startEdges.append(edge)'''


        '''
        #This is for start node identification via sets

        sourceNodes = set()
        targetNodes = set()
        # get source and target nodes for each edge to find all nodes that only have outgoing edges
        for edge in inputGraph:
            sourceNodes.add(edge[0])
            targetNodes.add(edge[1])

        #print("in findStartNodes, source: ", sourceNodes)
        #print("in findStartNodes, target: ", targetNodes)
        # start nodes only exist in the source nodes, so subtracting the two sets return the start nodes
        startNodes = sourceNodes-targetNodes
        #print('start nodes: ', startNodes)
        '''
        return edgesCount, startNodes

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode):
        path = []
        target = startNode
        tempGraph = self.graph.copy()
        #print(tempGraph)
        
        while True:
            #In this code, dropwhile() skips items from the dictionary iterator until it reaches the start_key.
            for edge in tempGraph.items():                
                prefix = edge[0]
                suffixes = edge[1]

                if prefix == target:
                    ## TO COVER OTHER CASES ADD MORE IF/ELSE STATEMENTS FOR SIZE OF SUFFIXES
                    if len(suffixes) == 1:
                        path.append({prefix:suffixes[0]})
                        target = suffixes[0]
                        del tempGraph[prefix]
                    #if len(suffixes) >= 1:   
                    #    print("here")                 
                    #    for i, v in enumerate(suffixes):
                    #        path.append({prefix:suffixes[i]})
                    #    target = suffixes[0]
                    #    del tempGraph[prefix]
                    else:
                        del tempGraph[prefix]
    
                    break
            # break when no more edges are available (no more edges that have an outgoing edge)
            else:
                break
        self.allPaths.append(path)
    

    # Input: graph (edge list)
    # Output: contiguous sequences
    def createContigs(self):
        inputGraph = self.graph

        edgesCount, startNodes = self.findStartNodes(inputGraph)
        print("Number of starting nodes: ", len(startNodes))

        contigs = []
        contigIndexTable = {}
        #print(inputGraph)

        for node in startNodes:
            self.followPath(node)
        
        '''for node in edgesCount:
            if edgesCount[node][0] == 0:
                self.followPath(startEdge=node)
                print(node)'''

        for path in self.allPaths:
            contig = []
            contigStr = ""
            contigMetadata = []
            kmers = []
            #print(path)
            for ei,edge in enumerate(path):
                #print(edge)
                for nodes in edge.items():
                    #print(nodes)
                    metadata = path[ei]
                    for ni, node in enumerate(nodes):
                        if len(contig) == 0:
                            contig.append(node)
                            contigStr = node

                        else:
                            contig.append(node[-1])

                            contigStr += node[-1]
                            
                        if ni == 0:
                            kmer = node + nodes[1][-1]
                            
                        if ni == 1:
                            '''if kmer not in contigStr:
                                print("NOT in contig")
                            else:
                                print("KMER in CONTIG")'''
                            startIndex = contigStr.find(kmer)
                            stopIndex = startIndex + len(kmer)
                            contigMetadata.append({kmer: {startIndex: stopIndex}})
                        
                    break
        
            contig = ''.join(contig)
            
            contigs.append(contig)
            contigIndexTable[contig] = contigMetadata
            with open('contigs.txt', 'w') as file:
                for i in contigs:
                    file.write(i)
                    file.write("\n")
            #print(contigIndexTable)

        #print(len(inputGraph))
        '''for i, edge in enumerate(inputGraph):
        
            # if there is a split in the graph
            if i+1<len(inputGraph):
                if edge[0] == inputGraph[i+1][0]:
                    print(f"split in path at: {inputGraph[i+1]} and {edge}") 
                    if edge[0] == inputGraph[i+2][0]:
                        print(f"2 splits in path at: {inputGraph[i+1]} and {edge}")                     
            # if there is a self repeating loop
            if edge[0] == edge[1]:
                print(f"Loop in graph @: {edge}")'''


        #print('contigs: ', contigs)
        print('contigs len: ', [len(contig) for contig in contigs])
        print('number of contigs:', len(contigs))
        return contigs
        


'''
PSEUDOCODE for CONTIG CREATION:
for each node in edges:
    if any given node only exists in the first position of the edge pair (i.e. is a starting node), mark as a starting node.
    if any given node only exists in the second position of the edge pair (i.e. is an ending node), mark as an ending node.
    if any path repeats, collapse (i.e. only take one path thru the loop and break at the last node).

'''