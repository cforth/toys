#!usr/bin/env python3
## Depth First Search Algorithm

from undirected_graphs import *

class DepthFirstSearch(object):
    def __init__(self, g):
        self.__graph = g
        self.__marked = [False for m in range(g.get_verticals())]
        self.__count = 0
    
    def search(self, v):
        self.__marked[v] = True
        self.__count += 1
        for vertical in self.__graph.get_adjacency(v):
            if not self.__marked[vertical]:
                self.search(vertical)
    
    def is_marked(self, vertical):
        return self.__marked[vertical]
        
    def count(self):
        return self.__count

    def marked(self):
        return self.__marked

##test
def main():
    mygraph = Graph(13)
    mygraph.add_edge(0, 1)
    mygraph.add_edge(0, 2)
    mygraph.add_edge(0, 5)
    mygraph.add_edge(0, 6)
    mygraph.add_edge(5, 3)
    mygraph.add_edge(5, 4)
    mygraph.add_edge(3, 4)
    mygraph.add_edge(4, 6)

    mygraph.add_edge(7, 8)

    mygraph.add_edge(9, 10)
    mygraph.add_edge(9, 11)
    mygraph.add_edge(11, 12)
    mygraph.add_edge(9, 12)

    mygraph.print_adjacency()
    
    dfs = DepthFirstSearch(mygraph)
    dfs.search(5)
    print(dfs.marked())

if __name__ == '__main__':
    main()
