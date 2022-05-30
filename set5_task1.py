from graphs import Graph, Edge, Vertex
import drawGraph
import random


def canEdgeBeAdded(left: Vertex, right: Vertex, graph: Graph):
    if left.label == 't':
        return False
    if right.label == 's':
        return False
    if graph.findEdges(left, right):
        return False
    if graph.findEdges(right, left):
        return False
    if left.equals(right):
        return False
    return True


def createRandomFlowNetwork(n: int = 3):
    """
    Tworzy i zwraca graf skierowany przedstawiajacy siec przeplywowa\n
    ma jedno ujscie i zrodlo oraz n warstw ( n >= 2 )\n
    wierzcholek reprezentujacy ujscie jest oznaczony jako t, a zrodlo jako s\n
    wszystkie wierzcholki (oprocz zrodla i ujscia) nazwane sa wedlug tej konwencji:\n
    litera L, a pozniej liczba przedstawiajaca numer warstwy do ktorej nalezy wierzcholek\n
    litera v, a pozniej liczba przedstawiajaca numer wierzcholka w danej warstwie
    """
    if(n < 2):
        raise Exception('Zbyt mala liczba warstw')
    
    network = Graph(directed=True)

    source = network.addVertex('s')

    prevLayer = [source]

    for i in range(n+1):
        numberOfVerticesInLayer = random.randint(2, n)
        currentLayer = []
        if i == n:
            currentLayer.append(network.addVertex('t'))
        else:
            for k in range(numberOfVerticesInLayer):
                currentLayer.append(network.addVertex(f'L{i+1}v{k+1}'))

        for previousLayerVertex in prevLayer:
            currentLayerVertex = random.choice(currentLayer)
            network.addEdge(previousLayerVertex, currentLayerVertex)

        if not i == n:
            for currentLayerVertex in currentLayer:
                if not currentLayerVertex.inEdges:
                    previousLayerVertex = random.choice(prevLayer)
                    network.addEdge(previousLayerVertex, currentLayerVertex)
        prevLayer = currentLayer
        
    MAX_ITER = 1000

    verticesList = list(network.vertexIndex.values())

    for _ in range(2*n):
        leftVertex = random.choice(verticesList)
        rightVertex = random.choice(verticesList)

        i = 0
        while i < MAX_ITER and not canEdgeBeAdded(leftVertex, rightVertex, network):
            leftVertex = random.choice(verticesList)
            rightVertex = random.choice(verticesList)
            i = i + 1
        
        if i == MAX_ITER:
            raise Exception('Nie udalo sie wylosowac dodatkowych 2n krawedzi')
        
        network.addEdge(leftVertex, rightVertex)
        


    for edge in network.edgeIndex.values():
        edge.weight = random.randint(1,10)

    return network




def testCreatingRandomFlowNetwork():
    flowNetwork = createRandomFlowNetwork(3)
    drawGraph.drawDirectedGraphWithWeights(flowNetwork, 5, 'flowNetwork.png')

if __name__ == '__main__':
    testCreatingRandomFlowNetwork()