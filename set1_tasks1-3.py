from graphs import *
from drawGraph import *
import random 

def task1():
    g = Graph.generateRandomGraph(10, 18)
    g.removeDuplicatedEdges()
    drawVertexes(g, 3, "set1task1.png")
    g.printAdjacencyList()
    g.printAdjacencyMatrix()
    g.printIncidenceMatrix()

def task3():
    ver = random.randint(5, 15)
    edg = random.randint(10,20)
    p = random.random()
    print(f"Task3\nParameters:\nVertices = {ver}\tEdges = {edg}\tProbability = {p}")
    g1 = Graph.generateRandomGraph(ver, edg)
    g2 = Graph.generateRandomGraphProbability(ver, p)
    drawVertexes(g1, 3, "task3_g1.png")
    drawVertexes(g2, 3, "task3_g2.png")


if __name__ == "__main__":
    task1()
    task3()