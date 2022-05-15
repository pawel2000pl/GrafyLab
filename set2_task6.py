from graphs2 import *

if __name__ == "__main__":
    # Testing for Hamiltonian Graph
    g = Graph(False)
    g != None
    g.addVertex("1")
    g.addVertex("2")
    g.addVertex("3")
    g.addVertex("4")
    g.addVertex("5")
    g.addVertex("6")
    g.addVertex("7")
    g.addVertex("8")
    g.addEdge("1", "2")
    g.addEdge("1", "4")
    g.addEdge("1", "5")
    g.addEdge("2", "3")
    g.addEdge("2", "5")
    g.addEdge("2", "6")
    g.addEdge("3", "4")
    g.addEdge("3", "7")
    g.addEdge("4", "6")
    g.addEdge("4", "7")
    g.addEdge("5", "8")
    g.addEdge("6", "8")
    g.addEdge("7", "8")
    print("Graph no. 1")

    graph = prepareGraphForHamilton(g.createAdjacencyList())
    result = hamiltonCycle(list(graph))
    print("Hamilton cycle :", result)
    drawCircularGraph(g, 4, "Hamilton1.png")

    # Testing for Non-Hamiltonian graph
    g2 = Graph(False)
    g2 != None
    g2.addVertex("1")
    g2.addVertex("2")
    g2.addVertex("3")
    g2.addVertex("4")
    g2.addVertex("5")
    g2.addEdge("1", "2")
    g2.addEdge("2", "3")
    g2.addEdge("3", "4")
    g2.addEdge("4", "1")
    g2.addEdge("2", "4")
    g2.addEdge("2", "5")
    g2.addEdge("4", "5")
    g2.addEdge("1", "5")
    drawCircularGraph(g2, 4, "Non-Hamilton2.png")

    print("Graph no. 2")
    graph2 = prepareGraphForHamilton(g2.createAdjacencyList())
    result2 = hamiltonCycle(graph2)
    print("Hamilton cycle :", result2)

    g3 = Graph(False)
    g3 != None
    g3.addVertex("1")
    g3.addVertex("2")
    g3.addVertex("3")
    g3.addVertex("4")
    g3.addVertex("5")
    g3.addVertex("6")
    g3.addVertex("7")
    g3.addVertex("8")
    g3.addVertex("9")
    g3.addEdge("1", "2")
    g3.addEdge("1", "4")
    g3.addEdge("1", "5")
    g3.addEdge("2", "3")
    g3.addEdge("2", "5")
    g3.addEdge("2", "6")
    g3.addEdge("3", "4")
    g3.addEdge("3", "7")
    g3.addEdge("4", "6")
    g3.addEdge("7", "8")
    g3.addEdge("8", "1")
    g3.addEdge("9", "5")
    g3.addEdge("9", "6")
    drawCircularGraph(g3, 4, "Hamilton3.png")

    print("Graph no. 3")
    graph3 = prepareGraphForHamilton(g3.createAdjacencyList())
    result3 = hamiltonCycle(graph3)
    print("Hamilton cycle :", result3)

    # g4 = Graph(False)
    # g4 != None
    # g4.addVertex("1")
    # g4.addVertex("2")
    # g4.addVertex("3")
    # g4.addVertex("4")
    # g4.addVertex("5")
    # g4.addVertex("6")
    # g4.addVertex("7")
    # g4.addVertex("8")
    # g4.addEdge("", "")

