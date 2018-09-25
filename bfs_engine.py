'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          bfs_no_gui.py
   By:            Qin Chen
   Last Updated:  6/10/17

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import pdb
import Queue

##############
# Data types used in this implementation: dictionary, set, list.
# Graph should be implemented as a class with addnode(), etc. 
# For simplicity, we make graph a dictionary
##############
# This graph is for 3x4 grid navigation with 3 obstacles
#graph = {'0-0': set(['1-0', '0-1']),
#         '0-1': set(['0-0', '0-2']),
#         '0-2': set(['1-2', '0-3']),
#         '0-3': set(['0-2', '1-3']),
#         '1-0': set(['0-0', '2-0']),
#         '1-2': set(['0-2', '2-2', '1-3']),
#         '1-3': set(['1-2', '0-3']),
#         '2-0': set(['1-0', '2-1']),
#         '2-1': set(['2-0', '2-2', '3-1']),
#         '2-2': set(['1-2', '2-1']),
#         '3-1': set(['2-1', '4-1']),
#         '3-3': set(['4-3']),
#         '4-0': set(['4-1']),
#         '4-1': set(['4-0', '3-1', '4-2']),
#         '4-2': set(['4-1', '4-3']),
#         '4-3': set(['4-2', '3-3'])}

# this graph has two paths from A to F
#graph = {'A': set(['B', 'C']),
#         'B': set(['A', 'E', 'D']),
#         'C': set(['A', 'F']),
#         'D': set(['B']),
#         'E': set(['B','F']),
#         'F': set(['C','E'])}

# graph used in lecture slide, but only one path from A to any node

class BFS(object):
    def __init__(self, graph):
        self.graph = graph
        return

    ######################################################
    # this function returns the shortest path for given start and goal nodes
    ######################################################
    def bfs_shortest_path(self, start, goal):
        stack = [(start, [start])]

        while stack:
            #print 'before pop, stack=', stack
            (vertex, path) = stack.pop(0)   # FIFO
            #print 'after pop stack=', stack
            print '\nvisiting node', vertex, 'path=', path

            for next in self.graph[vertex] - set(path):
                print 'next node', next
                if next == goal:
                    return path + [next]     # returns a path and continues while loop 
                else:
                    stack.append((next, path + [next]))
                    print "Stack push", next, path+[next]
        return

    ######################################################
    # this function returns all paths for given start and goal nodes
    ######################################################
    def bfs_paths(self, start, goal):
        stack = [(start, [start])] # list of tuples

        while stack:
            #print 'before pop, stack=', stack
            (vertex, path) = stack.pop(0)   # FIFO
            #print 'after pop stack=', stack
            print 'visiting node', vertex, 'path=', path
            for next in self.graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]     # returns a path and cont while loop 
                else:
                    stack.append((next, path + [next]))
                
    #########################################################
    # This function returns the shortest paths for given list of paths
    #########################################################
    def shortest(self, paths):
        dist = sys.maxint
        for index in range(len(paths)):
            d = len(paths[index])
            if d < dist:
                dist = d
                best_path = index
        return paths[best_path]

    #########################################################
    # THis function traverses the graph from given start node
    # return order of nodes visited
    #########################################################
    def bfs(self, start):
        visited_order = list()
        visited = set()
        q = list([start])

        while q:
            vertex = q.pop(0)   # FIFO queue
            if vertex not in visited:
                print("visiting ", vertex)
                visited.add(vertex)
                visited_order.append(vertex)
                print ("---visited_order", visited_order)
                q.extend(self.graph[vertex] - visited) # subtract only applies to set's            
        return visited_order

def main():
    graph = {'A': set(['B', 'C']),
         'B': set(['A', 'E', 'D']),
         'C': set(['A', 'F', 'G']),
         'D': set(['B', 'H']),
         'E': set(['B','I', 'J']),
         'F': set(['C','K']),
         'G': set(['C']),
         'H': set(['D']),
         'I': set(['E']),
         'J': set(['E']),
         'K': set(['F'])}

    graph = {'1-0': set(['0-0']), '0-0': set(['1-0', '0-1']), '0-1': set(['0-0'])}

    bfs = BFS(graph)
    #print 'graph:', graph

    start_node = '0-0'
    end_node = '1-1'

    p = bfs.bfs_shortest_path(start_node, end_node)
    print "\n++++++++++Shortest path from %s to %s: %s\n" % (start_node, end_node, p)

    # find all the paths returned by bfs_paths()
    # paths = list(bfs.bfs_paths(start_node, end_node)) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
    # print "\n==========paths from %s to %s: %s\n" % (start_node, end_node, paths)
    #print "\n----------shortest path: %s\n" % bfs.shortest(paths)

    #order holds traverse order of the all the nodes
    order = bfs.bfs(start_node)
    print "\n##########traverse order:", order

    return

if __name__ == "__main__":
    sys.exit(main())