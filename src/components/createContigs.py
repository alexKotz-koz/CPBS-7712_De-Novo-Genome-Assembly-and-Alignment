import pandas as pd
class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.finalGraph = []
        self.allPaths = []

    # Input: edge list from readsToKmers
    # Output: a list of all start nodes (nodes that only have outgoing edges)
    def findStartNodes(self, inputGraph):
        ## TODO: Will need to optimize for larger dataset
        #calculate the in and out degrees for 
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
        return startNodes

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode):
        path = []
        # start the path with the start node returned from findStartNodes
        target = startNode
        # make a copy of the graph to manipulate during the path walk
        tempGraph = self.graph.copy()
        df = pd.DataFrame(tempGraph)
        with open('test.csv', 'w') as file:
            df.to_csv(file)
                
        

        
        while True:
            # for each edge in the graph copy
            for i, edge in enumerate(tempGraph):
                '''if i+1<len(tempGraph) and edge[0] == tempGraph[i+2][0]:  
                    print(f"split in path @: {i} \n split @: {edge} and {tempGraph[i+1]}")'''
                '''
                if edge[0] == edge[1]:
                    print(f"self repeating loop @: {i} \n edge:{edge}")
                    print(F"current path is: {path}")
                    break
                '''
                #print(tempGraph[edge])
                # if the source node in the edge is equal to the last node seen (target)
                if edge[0] == target:
                    # add the edge to the path
                    
                    path.append({edge:tempGraph[edge]})
                    #path.append(edge)
                    # new target is the target node of the current edge (second position of the edge tuple)
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
        startNodes = self.findStartNodes(inputGraph)
        contigs = []
        contigIndexTable = {}
        #print(inputGraph)
        
        # using the list of starting nodes returned from findStartNodes, follow all paths through the graph. followPath() will add the path to a global object "allPaths"
        for node in startNodes:
            self.followPath(startNode=node)
        '''for path in self.allPaths:
            print(path)
            print("\n")'''
        '''for path in self.allPaths:
            print(path)
            print("\n")'''    
        #print("all paths len: ", len(self.allPaths))
        # for each of the paths (list of edges) in the global allPaths object
        for path in self.allPaths:
            contig = []
            contigStr = ""
            contigMetadata = []
            kmers = []
            # for each edge in the current path
            for ei,edge in enumerate(path):
                print(ei)
                # for each node in the edge
                for nodes in edge.keys():
                    metadata = path[ei]
                    for ni, node in enumerate(nodes):
                        if len(contig) == 0:
                            contig.append(node)
                            contigStr = node
                            print('first node: ', node)
                        else:
                            contig.append(node[-1])
                            print("node: ", node)
                            print("contigSTR pre: ", contigStr)
                            print("node last char: ", node[-1])
                            contigStr += node[-1]

                            print("contigStr post: ", contigStr)
                            print("\n\n")
                            
                        if ni == 0:
                            kmer = node + nodes[1][-1]
                            
                        if ni == 1:
                            if kmer not in contigStr:
                                print("NOT in contig")
                            else:
                                print("KMER in CONTIG")
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