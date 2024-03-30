import pandas as pd
from itertools import dropwhile
class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.finalGraph = []
        self.allPaths = []
        self.edgesCount = {}

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
        self.edgesCount = edgesCount
        return edgesCount, startNodes

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode):
        paths = []
        stack = [startNode]
        visited = []
        tempGraph = self.graph.copy()
        #print(tempGraph)
        while stack:
            print(f"stack: {stack}")
            
            currentNode = stack.pop()
            #print(f"current node: {currentNode}")
            if currentNode not in visited:
                visited.append(currentNode)
                #print(f"visited: {visited}")

                ## Check if last node in the path
                if currentNode not in tempGraph:
                    for edge in self.edgesCount:
                        if currentNode == edge:
                            #print(f"edge in edgesCount: {self.edgesCount[edge]}")
                            if self.edgesCount[edge][1] == 0:
                                return visited
                            

                # add the neighboors of the currentNode to the stack (if the neighboors are not already visited)
                stack.extend([node for node in tempGraph[currentNode] if node not in visited])
                print(tempGraph[currentNode])

        
    

    # Input: graph (edge list)
    # Output: contiguous sequences
    def createContigs(self):
        inputGraph = self.graph

        edgesCount, startNodes = self.findStartNodes(inputGraph)
        print("Number of starting nodes: ", len(startNodes))

        contigs = []
        contigIndexTable = {}
        #print(inputGraph)

        for node in startNodes[:3]:
            visited = self.followPath(node)
            print("\n")
            self.allPaths.append(visited)
            

        for path in self.allPaths:
            contig = []
            contigStr = ""

            for node in path:
                if len(contig) == 0:
                    contig.append(node)
                else:
                    contig.append(node[-1])
        
            contigStr = ''.join(contig)       
            contigs.append(contigStr)
        with open("contigs.txt", "w") as file:
            for contig in contigs:
                file.write(contig + "\n")

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