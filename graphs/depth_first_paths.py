#!usr/bin/env python3
## Depth First Paths Algorithm

from undirected_graphs import *

class DepthFirstPaths(object):
    def __init__(self, graph, start):
        self.__g = graph
        self.__s = start
        self.__marked = [False for m in range(graph.get_verticals())]
        self.__edges_to = [None for e in range(graph.get_verticals())]
    
    def dfs(self, v):
        self.__marked[v] = True
        for w in self.__g.get_adjacency(v):
            if not self.__marked[w]:
                self.__edges_to[w] = v
                self.dfs(w)

    def has_path_to(self, v):
        return self.__marked[v]
        
    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = []
        x = v
        while x != self.__s:
            path.insert(0, x)
            x = self.__edges_to[x]
        path.insert(0, self.__s)
        return path

    def edges_to(self):
        return self.__edges_to
        

##test
def main():
    mygraph = Graph(6)
    mygraph.add_edge(0, 1)
    mygraph.add_edge(0, 2)
    mygraph.add_edge(0, 5)
    mygraph.add_edge(1, 2)
    mygraph.add_edge(2, 3)
    mygraph.add_edge(2, 4)
    mygraph.add_edge(3, 5)
    mygraph.add_edge(3, 4)

    mygraph.print_adjacency()
    
    dfp = DepthFirstPaths(mygraph, 0)
    dfp.dfs(0)
    print(dfp.path_to(5))
    print(dfp.path_to(2))
    print(dfp.edges_to())

if __name__ == '__main__':
    main()
