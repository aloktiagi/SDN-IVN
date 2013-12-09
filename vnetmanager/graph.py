#!/usr/bin/python
from pprint import pprint
def dijkstra(start,target):
    graph = {
       's2' : [('s1',1)],
       's3' : [('s1', 1)],
       's4' : [('s1', 1)],
       's1' : [('s2', 1), ('s3', 1), ('s4', 1)],
       }

    inf = 0
    for u in graph:
        for v ,w in graph[u]:
           inf = inf + w
    dist = dict([(u,inf) for u in graph])
    prev = dict([(u,None) for u in graph])
    q = graph.keys()
    dist[start] = 0
    #helper function
    def x(v):
        return dist[v]
    #
    while q != []:
        u = min(q, key=x)
        q.remove(u)
        for v,w in graph[u]:
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    #"way"
    trav = []
    temp = target
    while temp != start:
        trav.append(prev[temp])
        temp = prev[temp]
    trav.reverse()
    trav.append(target)
    return trav
'''
graph = {
    'S2' : [('S1',1)],
    'S3' : [('S2', 1)],
    'S4' : [('S3', 1)],
    'S1' : [('S2', 1), ('S3', 1), ('S4', 1)],
    }
'''
#pprint(graph)
#print
#traverse, dist = dijkstra(graph,'S2','S4')
#print traverse
#print "Distance:",dist
