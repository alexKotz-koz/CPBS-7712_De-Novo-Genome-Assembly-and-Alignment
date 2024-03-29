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
        startEdges = []
        for edge in inputGraph.items():
            print(edge)
            # first node in the tuple has an outgoing edge
            if edge[0] in edgesCount:
                edgesCount[edge[0]][1] += 1
            else:
                edgesCount[edge[0]] = [0,1] #[incoming, outgoing]
            
            # second node in the tuple has an incoming edge
            if edge[1] in edgesCount:
                edgesCount[edge[1]][0] += 1
            else:
                edgesCount[edge[1]] = [1,0]
        #print("edgecount: ", edgesCount)
        # Initialize a list to store the start edges

        # Iterate over the edges
        for edge in inputGraph:
            # If the first node in the edge is not in edges_count or has zero incoming edges
            if edge[0] not in edgesCount or edgesCount[edge[0]][0] == 0:
                # Add the edge to the start_edges list
                startEdges.append(edge)


        with open("startNodes.txt", "w") as file:
            for edge in startEdges:
                file.write(edge[0] + "\n")

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
        return edgesCount, startEdges

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startEdge):
        path = []
        target = startEdge[0]
        print(target)
        tempGraph = self.graph.copy()

        startIndex = -1
        for index, edge in enumerate(tempGraph):
            if edge == startEdge:
                startIndex = index
        
        if startIndex == -1:
            print("error finding start index for path walk")
            exit


        while True:
            
            #In this code, dropwhile() skips items from the dictionary iterator until it reaches the start_key.
            for i, edge in enumerate(tempGraph):
                #print(edge)
                
                '''if i+1<len(tempGraph) and edge[0] == tempGraph[i+2][0]:  
                    print(f"split in path @: {i} \n split @: {edge} and {tempGraph[i+1]}")'''
                '''
                if edge[0] == edge[1]:
                    print(f"self repeating loop @: {i} \n edge:{edge}")
                    print(F"current path is: {path}")
                    break
                '''
                if edge[0] == target:
                    
                    path.append({edge:tempGraph[edge]})

                    target = edge[1]
                    # remove the edge from the graph copy
                    
                    del tempGraph[edge]
                    #del tempGraph[i]
                    # exit the for loop 
                    break
            # break when no more edges are available (no more edges that have an outgoing edge)
            else:
                break
        self.allPaths.append(path)
    

    # Input: graph (edge list)
    # Output: contiguous sequences
    def createContigs(self):
        inputGraph = self.graph

        edgesCount, startEdges = self.findStartNodes(inputGraph)
        print("Number of starting nodes: ", len(startEdges))

        contigs = []
        contigIndexTable = {}
        #print(inputGraph)

        for edge in startEdges:
            self.followPath(startEdge=edge)
        
        '''for node in edgesCount:
            if edgesCount[node][0] == 0:
                self.followPath(startEdge=node)
                print(node)'''

        for path in self.allPaths:
            contig = []
            contigStr = ""
            contigMetadata = []
            kmers = []

            for ei,edge in enumerate(path):

                for nodes in edge.keys():
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