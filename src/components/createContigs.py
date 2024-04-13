import json
import logging
import time
from collections import defaultdict, deque
import multiprocessing

class CreateContigs:
    def __init__(self, graph):
        self.graph = graph
        self.edgesCount = defaultdict(lambda: [0, 0])  # [incoming, outgoing]
        self.allPaths = []

    # Input: edge list from readsToKmers
    # Output: a list of all start nodes (nodes that only have outgoing edges)
    def findStartNodes(self):
        startNodes = []
        for node, edges in self.graph.items():
            self.edgesCount[node][1] += len(edges)
            for edge in edges:
                self.edgesCount[edge][0] += 1

        startNodes = [node for node, counts in self.edgesCount.items() if counts[0] == 0]
        return self.edgesCount, startNodes

    def checkIfLastNode(self, currentNode):
            # if the currentNode is not in the graph or the # of outgoing edges for the current node is 0, return True
            return currentNode not in self.graph or self.edgesCount[currentNode][1] == 0
        
    def lookForChildren(self, currentNode):
        if len(self.graph[currentNode]) > 1:
            return True, self.graph[currentNode]
        else:
            return False, []

    def followSubPath(self, startNode, originalPath):
        #logging.info(f"Entering followSubPath with startNode: {startNode}")

        stack = deque([(startNode, originalPath + [startNode])])
        while stack:
            currentNode, path = stack.pop()
            if self.checkIfLastNode(currentNode=currentNode):
                yield path # pause followSubPath execution, redirect control to followPath for consumption of yielded path
                continue
            children = self.graph.get(currentNode, [])
            for child in children:     
                # Does not cover case (two loops start and stop at the same node)
                #if path.count(child) < 2: #handles one loop
                if child not in path: #collapses loop
                    newPath = path + [child]  # create a new copy of path inside the loop
                    if self.checkIfLastNode(currentNode=child):
                        yield newPath # pause followSubPath execution, redirect control to followPath for consumption of yielded newPath
                    else:
                        stack.append((child, newPath))

    # Input: start node and graph (edge list)
    # Output: allPaths object that contains all possible paths through the graph
    def followPath(self, startNode, visited=None):
        if visited is None:
            visited = deque([])
        unfinishedPaths = deque([])
        stack = deque([startNode])
        while stack:
            currentNode = stack.pop()
            if type(currentNode) == list:  # handling case of second iteration on.
                currentNode = currentNode[0]
            if currentNode not in visited:
                visited.append(currentNode)
                isLastNode = self.checkIfLastNode(currentNode=currentNode)
                if isLastNode == True:
                    yield visited       
                else:
                    hasChildren, children = self.lookForChildren(currentNode=currentNode)
                    if hasChildren == False:
                        if self.graph[currentNode][0] not in visited:
                            stack.extend(self.graph[currentNode])
                    if hasChildren:
                        unfinishedPaths.append((visited, children))
        #print(f"createContigs...Number of Unfinished Paths after first pass:{len(unfinishedPaths)}\n")
        for path, children in unfinishedPaths:
            originalPath = list(path)
            for child in children:
                for finishedPath in self.followSubPath(child, originalPath=originalPath):
                    yield finishedPath
            
    # Input: graph (edge list)
    # Output: contiguous sequences
    def createContigs(self):
        edgesCount, startNodes = self.findStartNodes()
        incoming = sum(1 for counts in edgesCount.values() if counts[0] == 0)
        outgoing = sum(1 for counts in edgesCount.values() if counts[1] == 0)
        try:
            with open('data/logs/edgesCount.json', 'w') as file:
                json.dump(edgesCount, file)
        except FileNotFoundError:
            print("File or directory not found")
        logging.info(f"Number of start nodes: {incoming}")
        logging.info(f"Number of end nodes: {outgoing}")

        contigs = []

        walkStart = time.time()
        for node in startNodes:
            #print(f"createContigs...starting path @: {node}")
            for path in self.followPath(node):
                self.allPaths.append(path)
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


        with open("data/logs/contigs.txt", "w") as file:
            for contig in contigs:
                #print(contig)
                file.write(contig + "\n")

        try:
            avgLen = sum(len(contig) for contig in contigs) / len(contigs)
            logging.info(f"Average contig length: {avgLen}")
        except ZeroDivisionError:
            print("Length of contigs is 0, cannot calculate avg length of contig")
        logging.info(f"Total number of contigs: {[len(contigs)]}")
        
        logging.info(f"Minimum contig length: {len(min(contigs, key=len))}")
        logging.info(f"Maximum contig length: {len(max(contigs, key=len))}")
        return contigs, self.allPaths