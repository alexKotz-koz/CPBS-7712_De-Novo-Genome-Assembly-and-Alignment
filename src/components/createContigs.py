import pandas as pd
from itertools import dropwhile
import json
import logging
import time
import os

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
        
        if currentNode not in tempGraph:
            for edge in self.edgesCount:
                if currentNode == edge:
                    if self.edgesCount[edge][1] == 0:
                        return True
        return False  # Return False if the node has unvisited neighbors
    
    def lookForChildren(self, currentNode, tempGraph):
        if len(tempGraph[currentNode]) > 1:
            return True, tempGraph[currentNode]
        else:
            return False, []
        
    def followSubPath(self, startNode, originalPath, tempGraph):
        stack = [(startNode, originalPath + [startNode])]
        allPaths = []
        while stack:
            currentNode, path = stack.pop()
            if self.checkIfLastNode(currentNode=currentNode, tempGraph=tempGraph):
                allPaths.append(path)
                continue
            children = tempGraph.get(currentNode, [])
            for childIterator, child in enumerate(children):     
                # Does not cover case (two loops start and stop at the same node)       
                if path.count(child) < 2:
                    newPath = path + [child]  # create a new copy of path inside the loop
                    if self.checkIfLastNode(currentNode=child, tempGraph=tempGraph):
                        allPaths.append(newPath)
                    else:
                        stack.append((child, newPath))
        return allPaths

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode, inputGraph, visited=None):
        if visited is None:
            visited = []
        unfinishedPaths = []
        stack = [startNode]
        tempGraph = inputGraph
        while stack:
            currentNode = stack.pop()

            if type(currentNode) == list:  # handling case of second iteration on.
                currentNode = currentNode[0]

            if currentNode not in visited:
                visited.append(currentNode) # current node added to visited
                isLastNode = self.checkIfLastNode(currentNode=currentNode, tempGraph=tempGraph)

                if isLastNode == True:
                    self.allPaths.append(visited)
                    
                else:
                    hasChildren, children = self.lookForChildren(currentNode=currentNode, tempGraph=tempGraph)

                    if hasChildren == False:
                        if tempGraph[currentNode][0] not in visited:
                            stack.extend(tempGraph[currentNode])

                    if hasChildren:
                        unfinishedPaths.append((visited, children))
        
        for path, children in unfinishedPaths:
            originalPath = path.copy()

            for child in children:
                finishedPaths = self.followSubPath(child, originalPath=originalPath, tempGraph=tempGraph)
                for path in finishedPaths:
                    self.allPaths.append(path)       

            
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
        with open('data/logs/edgesCount.json', 'w') as file:
            json.dump(edgesCount, file)
        logging.info(f"Number of start nodes: {incoming}")
        logging.info(f"Number of end nodes: {outgoing}")

        contigs = []
        contigIndexTable = {}

        walkStart = time.time()
        for node in startNodes:
            self.followPath(node, inputGraph)
            contigsFromNode = [path for path in self.allPaths if path[0] == node]
            contigIndexTable[node] = contigsFromNode
        walkEnd = time.time()
        logging.info(f"Graph traversal finished in: {walkEnd-walkStart}\n")

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

        with open('data/logs/contigIndexTable.json', 'w') as file:
            json.dump(contigIndexTable, file)

        with open("data/logs/contigs.txt", "w") as file:
            for contig in contigs:
                file.write(contig + "\n")

        try:
            avgLen = sum(len(contig) for contig in contigs) / len(contigs)
            logging.info(f"Average contig length: {avgLen}")
        except ZeroDivisionError:
            print("Length of contigs is 0, cannot calculate avg length of contig")
        logging.info(f"Total number of contigs: {[len(contigs)]}")
        
        logging.info(f"Minimum contig length: {len(min(contigs, key=len))}")
        logging.info(f"Maximum contig length: {len(max(contigs, key=len))}")

        return contigs, contigIndexTable