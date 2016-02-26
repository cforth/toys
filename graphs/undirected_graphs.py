#!usr/bin/env python3
## Undirected Graphs Representation

class Graph(object):
    """利用邻接列表表示无向图
    """
    def __init__(self, vertical):
        self.__verticals = vertical
        self.__edges = 0
        self.__adjacency = [[] for v in range(vertical)]
        
    def get_verticals(self):
        return self.__verticals
    
    def get_edges(self):
        return self.__edges
        
    def add_edge(self, vertical_start, vertical_end):
        self.__adjacency[vertical_start].append(vertical_end)
        self.__adjacency[vertical_end].append(vertical_start)
        self.__edges += 1
        
    def get_adjacency(self, vetical):
        return self.__adjacency[vetical]

    def print_adjacency(self):
        print(self.__adjacency)


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

    print(mygraph.get_adjacency(3))
    mygraph.print_adjacency()

if __name__ == '__main__':
    main()
