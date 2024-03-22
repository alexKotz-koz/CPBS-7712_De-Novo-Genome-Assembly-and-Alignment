class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.finalGraph = []
        self.allPaths = []

    # Input: edge list from readsToKmers
    # Output: a list of all start nodes (nodes that only have outgoing edges)
    def findStartNodes(self, inputGraph):
        ## TODO: Will need to optimize for larger dataset
        sourceNodes = set()
        targetNodes = set()
        # get source and target nodes for each edge to find all nodes that only have outgoing edges
        for edge in inputGraph:
            sourceNodes.add(edge[0])
            targetNodes.add(edge[1])

        # start nodes only exist in the source nodes, so subtracting the two sets return the start nodes
        startNodes = sourceNodes-targetNodes
        
        return startNodes

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode):
        path = []
        # start the path with the start node returned from findStartNodes
        target = startNode
        # make a copy of the graph to manipulate during the path walk
        tempGraph = self.graph.copy()

        while True:
            # for each edge in the graph copy
            for i, edge in enumerate(tempGraph):
                # if the source node in the edge is equal to the last node seen (target)
                if edge[0] == target:
                    # add the edge to the path
                    path.append(edge)
                    # new target is the target node of the current edge (second position of the edge tuple)
                    target = edge[1]
                    # remove the edge from the graph copy
                    del tempGraph[i]
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
        
        # using the list of starting nodes returned from findStartNodes, follow all paths through the graph. followPath() will add the path to a global object "allPaths"
        for node in startNodes:
            self.followPath(startNode=node)

        for path in self.allPaths:
            print(path)
            print("\n")    

        # for each of the paths (list of edges) in the global allPaths object
        for path in self.allPaths:
            contig = []
            # for each node in the current path
            for edge in path:
                for node in edge:
                    print(node)
                    if len(contig) == 0:
                        contig.append(node)
                    else:
                        contig.append(node[-1])
            contig = ''.join(contig)
            contigs.append(contig)
        print('contigs: ', contigs)
        print('contigs len: ', [len(contig) for contig in contigs])
        return contigs
        


'''
PSEUDOCODE for CONTIG CREATION:
for each node in edges:
    if any given node only exists in the first position of the edge pair (i.e. is a starting node), mark as a starting node.
    if any given node only exists in the second position of the edge pair (i.e. is an ending node), mark as an ending node.
    if any path repeats, collapse (i.e. only take one path thru the loop and break at the last node).

'''