import pandas as pd
from itertools import dropwhile
import json
class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.finalGraph = []
        self.allPaths = []
        self.edgesCount = {}
        self.count = 0
    # Input: edge list from readsToKmers
    # Output: a list of all start nodes (nodes that only have outgoing edges)
    def findStartNodes(self, inputGraph):
        ## TODO: Will need to optimize for larger dataset
        #calculate the in and out degrees for each node
        edgesCount = {}
        startNodes = []
        for edge in inputGraph.items():
            # first node in the tuple has an outgoing edge
            if edge[0] in edgesCount:
                edgesCount[edge[0]][1] += 1
            else:
                edgesCount[edge[0]] = [0,1] #[incoming, outgoing]
            
            for suffix in edge[1]:
                if suffix in edgesCount:
                    edgesCount[suffix][0] += 1
                else:
                    edgesCount[suffix] = [1,0]
            
        
        for edge in edgesCount.items():
            if edge[1][0] == 0:
                startNodes.append(edge[0])

        self.edgesCount = edgesCount
        return edgesCount, startNodes

    def checkIfLastNode(self, currentNode, tempGraph):
        #print("Checking if last node...")
        if currentNode not in tempGraph:
            for edge in self.edgesCount:
                if currentNode == edge:
                    #print(self.edgesCount[edge][1])
                    if self.edgesCount[edge][1] == 0:
                        return True
        return False  # Return False if the node has unvisited neighbors
    
    def lookForChildren(self, currentNode, tempGraph):
        if len(tempGraph[currentNode]) > 1:
            return True, tempGraph[currentNode]
        else:
            return False, []
    
    def followSubPath(self,startNode, visited, tempGraph):
        extendedPath = []
        stack = [startNode]
        print(f"FU follow path. Current unfinished path: {visited}")
        print(f"FU Start Node: {startNode}")
        while stack:
            currentNode = stack.pop()
            if type(currentNode) == list:
                currentNode = currentNode[0]
            if currentNode not in extendedPath:
                extendedPath.append(currentNode)
                print(f"Current: {extendedPath}")
                isLastNode = self.checkIfLastNode(currentNode=currentNode, tempGraph=tempGraph)
                if isLastNode:
                    
                    visited.extend(extendedPath)
                    print(F"Final Extended Path: {extendedPath}")
                    return extendedPath
                else:
                    hasChildren, children = self.lookForChildren(currentNode=currentNode, tempGraph=tempGraph)
                    if hasChildren:
                        # if either of the children are exit nodes,
                        for child in children:
                            for edge in self.edgesCount:
                                if child == edge:
                                    if self.edgesCount[edge][1] == 0:
                                        visited.extend(extendedPath)
                                        if edge == extendedPath[-1]:
                                            print(f"Sub follow path routine resulted in a child that is an exit node")
                                            return extendedPath
                                        elif edge not in extendedPath:
                                            extendedPath.append(edge)
                                            print(f"Sub follow path routine resulted in a child that is an exit node")                                            
                                            return extendedPath
                                        else:
                                            print("BUG: child in extended path, but not at the end of the path")
                            if child not in extendedPath:
                                print(f"child: {child}")
                                
                                visited.extend(extendedPath)
                                self.followSubPath(child, extendedPath, tempGraph=tempGraph)

                        print(f"Subpath has children| {currentNode}:{children}")
                        
                        #self.followSubPath(path, visited=visited.extend(extendedPath), tempGraph=tempGraph)
                    else:
                        if tempGraph[currentNode][0] not in extendedPath:
                            stack.extend(tempGraph[currentNode])


    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode, visited=None):
        if visited is None:
            visited = []
        unfinishedPaths = []
        stack = [startNode]
        tempGraph = self.graph.copy()
        print(f"Start Node: {startNode}")
        while stack:
            currentNode = stack.pop()
            #print(f"Current Node: {currentNode}")

            if type(currentNode) == list:  # handling case of second iteration on.
                currentNode = currentNode[0]

            '''if currentNode in visited:
                print("Cycle detected")
                print(currentNode)
                print(visited)
                cycleStart = visited.index(currentNode)
                cycle = visited[cycleStart:]
                print(cycleStart)
                print(cycle)'''


            if currentNode not in visited:
                visited.append(currentNode)
                isLastNode = self.checkIfLastNode(currentNode=currentNode, tempGraph=tempGraph)
                if isLastNode == True:
                    #print(f"Final Path: {visited}\n")
                    print(f"Finalized Path: {visited}")
                    return visited
                else:
                    hasChildren, children = self.lookForChildren(currentNode=currentNode, tempGraph=tempGraph)
                    if hasChildren == False:
                        print(f"Current Node has one child. Child Nodes: {tempGraph[currentNode]}")
                        if tempGraph[currentNode][0] not in visited:
                            #print(tempGraph[currentNode])
                            stack.extend(tempGraph[currentNode])
                            print(f"Add child to stack: {stack}\n")
                    if hasChildren:
                        print(f"Current Node has children. Child Nodes:{tempGraph[currentNode]}\n")
                        #print(f"split found @ {currentNode}:{tempGraph[currentNode]}")
                        #print(f"unfinishedPath: {visited}\n")
                        print("Children: ", children)
                        unfinishedPaths.append((visited, children))
        
        print(f"Number of unfinished paths: {len(unfinishedPaths)}\n")
        # Recursively call followPath for each unfinished path
        for path, children in unfinishedPaths:
            print(f"unfinished paths children: {children}")
            for child in children:
                visited = self.followSubPath(child, visited=path, tempGraph=tempGraph)
                return visited
        if self.checkIfLastNode(currentNode=visited[-1], tempGraph=tempGraph):
            return visited
        else:
            return None
        #return visited
        '''while stack:
            currentNode = stack.pop()
            if currentNode not in visited:
                visited.append(currentNode)

                ## Check if last node in the path
                isLastNode = self.checkIfLastNode(currentNode=currentNode, tempGraph=tempGraph)
                if isLastNode == True:
                    print(f"Final Path: {visited}")
                    return visited
                # add the neighboors of the currentNode to the stack (if the neighboors are not already visited)
                stack.extend([node for node in tempGraph[currentNode] if node not in visited])'''
            
    # Input: graph (edge list)
    # Output: contiguous sequences
    def createContigs(self):
        inputGraph = self.graph

        edgesCount, startNodes = self.findStartNodes(inputGraph)
        incoming = 0
        outgoing = 0
        for i in edgesCount:
            if edgesCount[i][0] == 0:
                incoming += 1
            if edgesCount[i][1] == 0:
                outgoing += 1
        '''with open('edgesCount.json', 'w') as file:
            json.dump(edgesCount, file)'''
        print(f"incoming: {incoming}")
        print(f"outgoing {outgoing}")
        
        contigs = []
        contigIndexTable = {}
        #print(inputGraph)

        for node in startNodes[:2]:
            visited = self.followPath(node)
            self.allPaths.append(visited)
            #print(visited)
        print("\nIn CREATE CONTIGS\n")
        print(f"Number of paths: {len(self.allPaths)}")

        for path in self.allPaths:
            print(f"Path in allPaths: {path}")
        

        for path in self.allPaths:
            contig = []
            contigStr = ""
            #print(f"Path: {path}")
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