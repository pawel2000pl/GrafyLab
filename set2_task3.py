from graphs import *
from drawGraph import *

def task3():

    g = Graph(directed=False)
    for _ in range(11):
        g.addVertex()

    g.addEdge("v1", "v2")
    g.addEdge("v1", "v3")
    g.addEdge("v1", "v4")
    g.addEdge("v1", "v5")
    g.addEdge("v1", "v6")
    g.addEdge("v1", "v7")
    g.addEdge("v2", "v3")
    g.addEdge("v2", "v6")
    g.addEdge("v2", "v7")
    g.addEdge("v3", "v6")
    g.addEdge("v4", "v7")
    g.addEdge("v5", "v11")
    
    g.addEdge("v8", "v9")
    g.addEdge("v8", "v10")
    g.addEdge("v9", "v10")

    drawVertexes(g, 3, "set2_task3.png")

    comp, thegreatestcomp = g.components()
    print(comp)
    print(thegreatestcomp)

    def task3_randomgraph():
        g = Graph.generateRandomGraph(10, 14)
        

if __name__ == "__main__":
    task3()
    