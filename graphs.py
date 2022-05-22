import random
from math import inf

"""
   ___               _           
  / __|_ _ __ _ _ __| |_  ___
 | (_ | '_/ _` | '_ \ ' \(_-<
  \___|_| \__,_| .__/_||_/__/
               |_|   
"""


class Vertex:
    """
     __   __       _           
     \ \ / /__ _ _| |_ _____ __
      \ V / -_) '_|  _/ -_) \ /
       \_/\___|_|  \__\___/_\_\                    
    """

    def __init__(self, label: str, graph):
        self.label: str = label
        self.graph = graph
        self.inEdges = {}
        self.degree: int = 0
        self.inputDegree: int = 0
        self.outputDegree: int = 0
        if self.graph.isDirected():
            self.outEdges = {}
        else:
            self.outEdges = self.inEdges

    def allEdgesSet(self):
        return set(self.inEdges.values()).union(self.outEdges.values())

    def allEdgesList(self):
        return list(self.inEdges.values()) + list(self.outEdges.values())

    def calcDegree(self):
        """
        Oblicza na nowo stopień wierzchołka. 
        Niezalecane dla skierowanych
        - w przypadku wywołań dla wielu wierchołków lepiej użyć metody calculateDegreeOfVertexes() z klasy Graph,
        lub odwołac się bezpośrednio do pola degree.
        """
        if self.getGraph().isDirected():
            self.inputDegree = len(self.inEdges)
            self.outputDegree = len(self.outEdges)
            self.degree = self.inputDegree + self.outputDegree
        else:
            dictTab = {True: 1, False: 0}
            self.degree = sum(dictTab.get(edge.startVertex == self) + dictTab.get(edge.endVertex == self) for edge in
                              self.allEdgesSet());
            self.inputDegree = self.degree
            self.outputDegree = self.degree

    def removeMe(self):
        return self.graph.removeVertex(self)

    def adjacentVertices(self):
        """
        Zwraca listę wierzchołków przyległych.
        Tylko dla grafów nieskierowanych.
        """
        adjacencies = []  # lista przyległych wierzchołków
        for e in self.inEdges.values():
            opposite = e.oppositeVertex(self)
            adjacencies.append(opposite)
        return adjacencies

    def getGraph(self):
        return self.graph

    def equals(self, another):
        if not isinstance(another, Vertex):
            return False
        if self.label != another.label:
            return False
        if len(self.inEdges) != len(another.inEdges) or len(self.outEdges) != len(another.outEdges):
            return False
        for edge in self.inEdges.values():
            if another.inEdges.get(edge.label, None) == None:
                return False
        for edge in self.outEdges.values():
            if another.outEdges.get(edge.label, None) == None:
                return False
        return True

    def getOutEdges(self):
        return self.outEdges

    def getInEdges(self):
        return self.inEdges

    def getLabel(self):
        return self.label

    def __str__(self):
        result = "[" + self.label + ": "
        cont = ""
        for edge in self.outEdges.values():
            cont += edge.label + ", "
        if len(self.outEdges) != 0:
            cont = cont[:-2]

        if self.graph.isDirected():
            result += "in = ("
            for edge in self.inEdges.values():
                result += edge.label + ", "
            if len(self.inEdges) != 0:
                result = result[:-2]
            result += "), out = (" + cont + ")"
        else:
            result += cont
        return result + "]"

class Edge:
    """
      ___    _          
     | __|__| |__ _ ___ 
     | _|/ _` / _` / -_)
     |___\__,_\__, \___|
              |___/    
    """

    def __init__(self, startVertex: Vertex, endVertex: Vertex, label: str, weight: float = 1.0):
        assert startVertex.graph == endVertex.graph
        self.label = label
        self.weight: float = weight
        self.startVertex: Vertex = startVertex
        self.endVertex: Vertex = endVertex
        self.startVertex.outEdges.update({label: self})
        self.endVertex.inEdges.update({label: self})

    def getGraph(self):
        assert self.startVertex.graph == self.endVertex.graph
        return self.startVertex.getGraph()

    def removeMe(self):
        return self.getGraph().removeEdge(self)

    def getLabel(self):
        return self.label

    def oppositeVertex(self, vertex: Vertex):
        """
        Zwraca wierzchołek po przeciwnej stronie krawędzi, niż ten podany w parametrze.
        Jako parametr przyjmuje referencję do wierzchołka lub jego etykietę.
        Używać w przypadku wędrówek po grafach nieskierowanych.
        """
        if vertex == self.startVertex or vertex == self.startVertex.label:
            return self.endVertex
        return self.startVertex

    def switchDirection(self):
        """
        Odwraca zwrot krawędzi.
        """
        self.startVertex.outEdges.pop(self.label)
        self.startVertex.outputDegree -= 1
        self.endVertex.inEdges.pop(self.label)
        self.startVertex.inputDegree -= 1

        temp = self.endVertex
        self.endVertex = self.startVertex
        self.startVertex = temp

        self.startVertex.outEdges.update({self.label: self})
        self.startVertex.outputDegree += 1
        self.endVertex.inEdges.update({self.label: self})
        self.startVertex.inputDegree += 1

        return self

    def equals(self, another):
        if not isinstance(another, Edge):
            return False
        if self.label != another.label:
            return False
        if self.getGraph().isDirected() and (self.startVertex.label != another.startVertex.label or self.endVertex.label != another.endVertex.label):
            return False
        if (not self.getGraph().isDirected()) and (self.startVertex.label != another.startVertex.label or self.endVertex.label != another.endVertex.label) and (self.startVertex.label != another.endVertex.label or self.endVertex.label != another.startVertex.label):
            return False
        if self.weight != another.weight:
            return False
        return True

    def __str__(self):
        return "(" + self.label + ": " + self.startVertex.label + {True: " -> ", False: " <-> "}[self.getGraph().isDirected()] + self.endVertex.label + (", weight = " + str(self.weight) if self.weight != 1.0 else "") + ")"



class Graph:
    """
       ___               _    
      / __|_ _ __ _ _ __| |_  
     | (_ | '_/ _` | '_ \ ' \ 
      \___|_| \__,_| .__/_||_|
                   |_|      
    """

    def __init__(self, directed: bool = False):
        self.vertexIndex = {}
        self.edgeIndex = {}
        self.__vertexProposalNameNumber: int = 0
        self.__edgeProposalNameNumber: int = 0
        self.__directed = directed
        self.__numberOfVertexes: int = 0

    def isDirected(self):
        return self.__directed

    def proposalVertexName(self):
        while True:
            self.__vertexProposalNameNumber = self.__vertexProposalNameNumber + 1
            name: str = "v" + str(self.__vertexProposalNameNumber)
            if self.vertexIndex.get(name, None) == None:
                return name

    def proposalEdgeName(self):
        while True:
            self.__edgeProposalNameNumber = self.__edgeProposalNameNumber + 1
            name: str = "e" + str(self.__edgeProposalNameNumber)
            if self.edgeIndex.get(name, None) == None:
                return name

    def getVertex(self, label: str):
        """
        Zwraca referencję do wierzchołka na podstawie etykiety.
        Jeżeli wierzchołek nie istnieje, zwraca None.
        """
        return self.vertexIndex.get(label, None)

    def addVertex(self, label: str = None):
        """
        Dodaje nowy wierzchołek.
        Jeżeli istnieje wierzchołek o zadanej nazwie, wyrzuca wyjątek.
        """
        if label == None:
            label = self.proposalVertexName()
        newVertex: Vertex = Vertex(label, self)
        if self.getVertex(label) != None:
            raise Exception("Vertex currently exists", label)
        self.vertexIndex.update({label: newVertex})
        self.__numberOfVertexes += 1
        return newVertex

    def getOrAddVertex(self, label: str):
        """
        Zwraca wierzchołek o podanej nazwie, a jeśli nie istnieje, to zostaje dodany.
        """
        vertex = self.getVertex(label)
        if vertex == None:
            vertex = self.addVertex(label)
        return vertex

    def removeVertex(self, vertex):
        """
        Usuwa wierzhołek. 
        Przyjmuje etykietę wierzchołka, lub referencję do niego.
        """
        if isinstance(vertex, str):
            vertex = self.getVertex(vertex)
            if vertex == None:
                return False
        for label in set(vertex.inEdges.keys()).union(set(vertex.outEdges.keys())):
            self.removeEdge(label)
        self.vertexIndex.pop(vertex.label)
        del vertex
        return True

    def getNumberOfVertexes(self):
        return self.__numberOfVertexes

    def calculateDegreeOfVertexes(self):
        """
        Aktualizuje dla wszystkich wierzchołków stopnie wejściowe i wyjściowe.
        Używać w przypadku zmian wierzhcołków lub krawędzi poza klasą, w celu utrzymania spójności danych.
        Wynik znajduje się w nowo powstałym polu każdego wierzchołka:
            "degree" dla grafu nieskierowanego (degree = inputDegree + outputDegree dla skierowanego),
            "inputDegree" i "outputDegree" dla grafu skierowanego (inputDegree = outputDegree = degree dla nieskierowanego)
        """
        for vertex in self.vertexIndex.values():
            vertex.degree = 0
            vertex.inputDegree = 0
            vertex.outputDegree = 0

        for edge in self.edgeIndex.values():
            edge.startVertex.degree += 1
            edge.endVertex.degree += 1

        if self.isDirected():
            for edge in self.edgeIndex.values():
                edge.startVertex.outputDegree += 1
                edge.endVertex.inputDegree += 1
        else:
            for vertex in self.vertexIndex.values():
                vertex.inputDegree = vertex.degree
                vertex.outputDegree = vertex.degree

    def getEdge(self, label: str):
        """
        Zwraca referencję do krawędzi na podstawie etykiety.
        Jeżeli krawędź nie istnieje, zwraca None.
        """
        return self.edgeIndex.get(label, None)

    def addEdge(self, startVertex, endVertex, label: str = None, weight: float = 1.0):
        """
        Tworzy nową krawędź.
        Jako parametry przyjmuje referencje do wierzchołków, lub ich etykiety.
        """
        if label == None:
            label = self.proposalEdgeName()
        if self.getEdge(label) != None:
            raise Exception("Edge currently exists", label)
        if isinstance(startVertex, str):
            startVertex = self.getVertex(startVertex)
        if isinstance(endVertex, str):
            endVertex = self.getVertex(endVertex)
        if startVertex == None or endVertex == None:
            raise Exception("Vertex not found", startVertex, endVertex)
        newEdge: Edge = Edge(startVertex, endVertex, label, weight)
        self.edgeIndex.update({label: newEdge})
        startVertex.degree += 1
        endVertex.degree += 1
        startVertex.outputDegree += 1
        endVertex.inputDegree += 1
        return newEdge

    def removeEdge(self, edge):
        """
        Usuwa krawędź. 
        Przyjmuje etykietę krawędzi, lub referencję do niej.
        """
        if isinstance(edge, str):
            edge = self.getEdge(edge)
            if edge == None:
                return False
        edge.startVertex.outEdges.pop(edge.label)
        edge.endVertex.inEdges.pop(edge.label)
        self.edgeIndex.pop(edge.label)
        edge.startVertex.degree -= 1
        edge.endVertex.degree -= 1
        edge.startVertex.outputDegree -= 1
        edge.endVertex.inputDegree -= 1
        del edge
        return True

    def removeDuplicatedEdges(self):
        """
        Usuwa nadmiarowe krawędzie, jeżeli między dwoma wierzchołkami 
        jest więcej niż jedna w tym samym kierunku.
        """
        for vertex in self.vertexIndex.values():
            adjacent = set(edge.endVertex for edge in vertex.outEdges.values())
            for edge in set(vertex.outEdges.values()):
                if edge.endVertex in adjacent:
                    adjacent.remove(edge.endVertex)
                else:
                    edge.removeMe()

    def findEdges(self, startVertex, endVertex, oneElementList: bool = False):
        """
        Znajduje wszystkie krawędzie pomiędzy dwoma wierzchołkami.
        Zwraca listę, lub element /None (w zależności od parametru)
        """
        if isinstance(startVertex, str):
            startVertex = self.getVertex(startVertex)
        if isinstance(endVertex, str):
            endVertex = self.getVertex(endVertex)
        if startVertex == None or endVertex == None:
            raise Exception("Vertex not found", startVertex, endVertex)
        edges = set(startVertex.outEdges.values()).intersection(set(endVertex.inEdges.values()))
        labels = {edge.label for edge in edges if edge.startVertex == startVertex and edge.endVertex == endVertex} if self.isDirected() else {edge.label for edge in edges if (edge.startVertex == startVertex and edge.endVertex == endVertex) or (edge.startVertex == endVertex and edge.endVertex == startVertex)}
        #labels = set(startVertex.outEdges.keys()).intersection(set(endVertex.inEdges.keys()))
        result = [self.getEdge(label) for label in labels]
        if not oneElementList:
            if len(result) == 1:
                return result[0]
            elif len(result) == 0:
                return None
        return result

    def addCompositional(self, another):
        """
        Łączy dwa grafy w jeden (dodaje nowe spójne składowe).
        """
        for label in another.vertexIndex:
            self.addVertex(label)
        for edge in another.edgeIndex.values():
            self.addEdge(edge.startVertex.label, edge.endVertex.label, edge.label, edge.weight)
        return self

    def copy(self):
        """
        Tworzy czystą kopię strukturalną grafu.
        """
        return Graph(self.isDirected()).addCompositional(self)

    def equals(self, another):
        """
        Porównuje strukturalnie dwa grafy.
        """
        if not isinstance(another, Graph):
            return False
        if self.isDirected() != another.isDirected():
            return False
        if len(self.edgeIndex) != len(another.edgeIndex):
            return False
        if len(self.vertexIndex) != len(another.vertexIndex):
            return False
        for vertex in self.vertexIndex.values():
            if not vertex.equals(another.getVertex(vertex.label)):
                return False
        for edge in self.edgeIndex.values():
            if not edge.equals(another.getEdge(edge.label)):
                return False
        return True

    def takeVertexesDown(self, vertexA, vertexB, newLabel: str = None):
        """
        Ściąga dwa wierzchołki w jeden. Usuwa krawędzie pomiędzy tymi wierzchołkami. 
        Zwraca nowy wierzchołek.
        """
        if isinstance(vertexA, str):
            vertexA = self.getVertex(vertexA)
        if isinstance(vertexB, str):
            vertexB = self.getVertex(vertexB)
        if vertexA == None or vertexB == None:
            raise Exception("Invalid vertex", vertexA, vertexB)
        newVertex = self.addVertex(newLabel)
        for edge in set(self.findEdges(vertexA, vertexB, True)).union(set(self.findEdges(vertexB, vertexA, True))):
            edge.removeMe()
        if self.isDirected():
            newVertex.inEdges.update(vertexA.inEdges)
            newVertex.inEdges.update(vertexB.inEdges)
        newVertex.outEdges.update(vertexA.outEdges)
        newVertex.outEdges.update(vertexB.outEdges)
        for edge in set(newVertex.inEdges.values()).union(set(newVertex.outEdges.values())):
            if edge.startVertex == vertexA or edge.startVertex == vertexB:
                edge.startVertex = newVertex
            if edge.endVertex == vertexA or edge.endVertex == vertexB:
                edge.endVertex = newVertex

        self.vertexIndex.pop(vertexA.label, None)
        self.vertexIndex.pop(vertexB.label, None)
        del vertexA
        del vertexB
        newVertex.calcDegree()
        return newVertex

    def takeEdgeDown(self, edge, newVertexLabel: str):
        """
        Ściąga krawędź. Usuwa wszystkie pozostałe krawędzie między wierzchołkami tej krawędzi.
        Zwraca nowy wierzchołek.
        """
        if isinstance(edge, str):
            edge = self.getEdge(edge)
        if edge == None:
            raise Exception("Invalid edge", edge)
        return self.takeVertexesDown(edge.startVertex, edge.endVertex, newVertexLabel)

    def __str__(self):
        """
        Konwertuje graf na czytelną reprezentację tekstową.
        """
        result = ""
        for vertex in self.vertexIndex.values():
            result += str(vertex) + ", "
        if len(self.vertexIndex) != 0:
            result = result[:-2]
        result += "; "
        for edge in self.edgeIndex.values():
            result += str(edge) + ", "
        if len(self.edgeIndex) != 0:
            result = result[:-2]
        return "{" + result + "}"

    def createAdjacencyMatrix(self):
        """
        Tworzy macierz sąsiedztwa.
        Zwraca krotkę: (lista wierzchołków, macierz)
        """
        vertexList = self.vertexIndex.values()
        vertexLabelList = [vertex.label for vertex in vertexList]
        matrix = [[0.0 for i in vertexList] for j in vertexList]
        for i, vertex1 in enumerate(vertexList):
            for j, vertex2 in enumerate(vertexList):
                matrix[i][j] += sum(edge.weight for edge in self.findEdges(vertex1, vertex2, True))
        return (vertexLabelList, matrix)

    def loadAdjacencyMatrix(self, matrix):
        """
        Dodaje strukturę z macierzy sąsiedztwa.
        Nie ma pewności, że zostanie otrzymany ten sam graf, co przy zapisie
        (np.: w przypadku wystąpienia wielokrotnych krawędzi).
        Nie sprawdza poprawnośc zapisu.
        Przyjmuje krotkę wygenerowaną przez createAdjacencyMatrix(),
        lub samą macierz (drugi element krotki)
        """
        if isinstance(matrix, tuple):
            labels = matrix[0]
            matrix = matrix[1]
        else:
            labels = [self.proposalVertexName() for i in range(len(matrix))]

        for label in labels:
            self.addVertex(label)
        for i, vertex1 in enumerate(self.vertexIndex.values()):
            for j, vertex2 in enumerate(self.vertexIndex.values()):
                if (not self.isDirected()) and (j > i):
                    break
                if matrix[i][j] != 0:
                    self.addEdge(vertex1, vertex2, weight=matrix[i][j])
        return self

    def createAdjacencyList(self):
        """
        Tworzy listę sąsiedztwa.
        """
        result = []
        for v in self.vertexIndex.values():
            edges = v.getOutEdges()
            adjacencies = []  # lista przyległych wierzchołków
            for e in edges.values():
                opposite = e.oppositeVertex(v)
                adjacencies.append(opposite.getLabel())
            result.append((v.getLabel(), adjacencies))
        return result

    def loadAdjacencyList(self, dataList):
        """
        Dodaje strukturę z listy sąsiedztwa.
        Nie sprawdza poprawnośc zapisu.
        Przyjmuje listę w formacie wygenerowanycm przez createAdjacencyList().
        """

        for i in dataList:
            outVertex = self.getOrAddVertex(i[0])
            for v in i[1]:
                inVertex = self.getOrAddVertex(v)
                if self.isDirected() or outVertex.label > inVertex.label:
                    self.addEdge(outVertex, inVertex)

        return self

    def createIncidenceMatrix(self):
        """
        Tworzy macierz incydencji.
        Zwraca krotkę: (lista krawędzi, lista wierzchołków, macierz).
        """
        vertexList = self.vertexIndex.values()
        vertexLabelList = [vertex.label for vertex in vertexList]
        edgeList = self.edgeIndex.values()
        edgeLabelList = [edge.label for edge in edgeList]
        matrix = [{label: 0 for label in vertexLabelList} for j in edgeList]
        negV: int = -1 if self.isDirected() else 1
        for i, edge in enumerate(edgeList):
            matrix[i].update({edge.startVertex.label: 1, edge.endVertex.label: negV})
        resultMatrix = [list(col.values()) for col in matrix]
        return (edgeLabelList, vertexLabelList, resultMatrix)

    def loadIncidenceMatrix(self, data):
        """
        Dodaje strukturę z macierzy incydencji.
        Nie sprawdza poprawnośc zapisu.
        Przyjmuje krotkę wygenerowaną przez createIncidenceMatrix(),
        lub samą macierz (trzeci element krotki).
        """
        if isinstance(data, tuple):
            edgeLabelList = data[0]
            vertexLabelList = data[1]
            matrix = data[2]
        else:
            matrix = data
            edgeLabelList = [self.proposalEdgeName() for i in range(len(matrix))]
            vertexLabelList = [self.proposalVertexName() for i in range(len(matrix[0]))]
        vertexList = [self.addVertex(label) for label in vertexLabelList]
        negV: int = -1 if self.isDirected() else 1
        for i, col in enumerate(matrix):
            startVertex = None
            endVertex = None
            for j, cell in enumerate(col):
                if startVertex == None and cell == 1:
                    startVertex = vertexList[j]
                if endVertex == None and cell == negV:
                    endVertex = vertexList[j]
            self.addEdge(startVertex, endVertex, edgeLabelList[i]);
        return self

    def printAdjacencyList(self):
        adjList = self.createAdjacencyList()
        outStr = ""
        for i in adjList:
            outStr += i[0] + ": "
            for j in i[1]:
                outStr += j + " "
            outStr += "\n"

        print(outStr)
        return outStr

    def printAdjacencyMatrix(self):
        adjMatrix = self.createAdjacencyMatrix()
        outStr = ""
        for nr, i in enumerate(adjMatrix[1]):
            outStr += "v" + str(nr + 1) + ": "
            for j in i:
                outStr += str(int(j)) + " "
            outStr += "\n"
        print(outStr)
        return outStr

    def printIncidenceMatrix(self):
        inMatrix = self.createIncidenceMatrix()
        edges = inMatrix[0]
        vertices = inMatrix[1]
        matrix = inMatrix[2]
        outStr = "   "
        for v in vertices:
            outStr += v + " "
        outStr += "\n"
        for i in range(len(edges)):
            outStr += edges[i] + " "
            for j in range(len(vertices)):
                outStr += str(matrix[i][j]) + "  "
            outStr += "\n"

        print(outStr)
        return outStr

    def getVertexIndex(self):
        return self.vertexIndex

    @staticmethod
    def generateRandomGraph(n, l, directed: bool = False):
        """
        Generuje losowy graf, gdzie
        n - liczba wierzchołków grafu
        l - liczba krawędzi grafu
        """
        g = Graph(directed)
        for _ in range(n):
            g.addVertex()

        vertexList = g.vertexIndex.values()
        vertexLabelList = [vertex.label for vertex in vertexList]

        for _ in range(l):
            vertexLabelListCopy = vertexLabelList.copy()
            v1 = vertexLabelListCopy.pop(random.randrange(len(vertexLabelList)))
            v2 = random.choice(vertexLabelListCopy)
            g.addEdge(v1, v2)

        return g

    @staticmethod
    def generateRandomGraphProbability(n, p, directed: bool = False):
        """
        Generuje losowy graf, gdzie
        n - liczba wierzchołków grafu
        p - prawdopodobieństwo, że pomiędzy dwoma wierzchołkami istnieje krawędź

        """
        if p < 0. or p > 1.:
            return None

        g = Graph(directed)
        for _ in range(n):
            g.addVertex()

        vertexList = g.vertexIndex.values()
        vertexLabelList = [vertex.label for vertex in vertexList]

        for _ in range(n):
            currentVertex = vertexLabelList.pop(0)
            for label in vertexLabelList:
                if random.random() < p:
                    g.addEdge(currentVertex, label)

        return g

    def components(self):
        """
        Algorytm oznaczający spójne składowe.
        Zwraca listę krotek (nr skladowej, wierzcholek)
        """
        nr = 0  # nr spójnej składowej

        vertices = self.vertexIndex.values()

        comp = []
        for v in vertices:
            comp.append([-1, v])  # wszystkie wierzchołki są nieodwiedzone

        for v in comp:
            if v[0] == -1:
                nr += 1
                v[0] = nr  # oznaczamy v jako odwiedzony i należący do spójnej składowej nr
                comp = Graph.components_R(nr, v[1], self, comp)

        thegreatestcompList = []

        comp_nums = [i[0] for i in comp]
        thegreatestcomp = max(set(comp_nums), key=comp_nums.count)

        for i in comp:
            if i[0] == thegreatestcomp:
                thegreatestcompList.append(i[1].getLabel())

        return comp, thegreatestcompList

    @staticmethod
    def components_R(nr, v, g, comp):
        """
        Rekursywne przeszukiwanie w głąb
        """
        for u in v.adjacentVertices():  # przeglądamy sąsiadów
            try:
                idx = comp.index([-1, u])
                if comp[idx][0] == -1:
                    comp[idx][0] = nr
                    Graph.components_R(nr, comp[idx][1], g, comp)
            except ValueError:
                continue

        return comp
    
    def DijkstraDistance(self, startVertex):
        """
        Funkcja oblicza odległości wierzchołków od zadanego wierzchołka.
        Zwraca wyniki w postaci słownika, w którym klucz to etykieta wierzchołka, 
        a wartość to odległość od wierzchołka startowego.
        Dodaje także do wierzchołków pole distance, które zawiera te wartości.
        Algorytm wysypie się dla ujemnych krawędzi, oraz nie wykryje (zawiesi się)
        dla ujemnych pętli.
        Jest to klasyczny algorytm Dijkstry.
        """
        
        if isinstance(startVertex, str):
            startVertex = self.getVertex(startVertex)
        
        Q = set(self.vertexIndex.values())
        
        for vertex in Q:
            vertex.distance = inf
            vertex.arrivedFrom = None        
                
        startVertex.distance = 0.0
        
        while len(Q) > 0:
            uv = min(vertex.distance for vertex in Q)
            u = [vertex for vertex in Q if vertex.distance == uv][0]
            Q.remove(u)
            
            for edge in u.outEdges.values():
                alt = u.distance + edge.weight
                v = edge.oppositeVertex(u)
                if alt < v.distance:
                    v.distance = alt
                    v.arrivedFrom = edge
          
        return {vertex.label: vertex.distance for vertex in self.vertexIndex.values()}
        
    def ShortestDistance(self, startVertex):
        """
        Funkcja oblicza odległości wierzchołków od zadanego wierzchołka.
        Zwraca wyniki w postaci słownika, w którym klucz to etykieta wierzchołka, 
        a wartość to odległość od wierzchołka startowego.
        Dodaje także do wierzchołków pole distance, które zawiera te wartości.
        Algorytm nie wysypie się dla ujemnych krawędzi, oraz wykryje (wyrzuci błąd)
        dla ujemnych pętli.
        Jest to Bellman-Ford na sterydach.
        """
        if isinstance(startVertex, str):
            startVertex = self.getVertex(startVertex)

        for vertex in self.vertexIndex.values():
            vertex.distance = inf
            vertex.arrivedFrom = None

        maxIter = len(self.edgeIndex) * len(self.vertexIndex) + 1
        it = 0

        def recurency(currentVertex, currentDistance, arrivedFrom):
            if currentDistance < currentVertex.distance:
                nonlocal it
                it += 1
                if it >= maxIter:
                    return
                currentVertex.distance = currentDistance
                currentVertex.arrivedFrom = arrivedFrom
                for edge in currentVertex.outEdges.values():
                    recurency(edge.oppositeVertex(currentVertex), currentDistance + edge.weight, edge)

        recurency(startVertex, 0.0, None)
        if it >= maxIter:
            raise Exception("Shortest path error: probably a negative loop")

        return {vertex.label: vertex.distance for vertex in self.vertexIndex.values()}

    def getWayTo(self, destVertex):
        """
        Zwraca najkrótszą ścieżkę na podstawie atrybutów arrivedFrom.
        Wymagane wcześniejsze uruchomienie funkcji DijkstraDistance lub ShortestDistance.
        """
        result = []
        if isinstance(destVertex, str):
            destVertex = self.getVertex(destVertex)
        currentVertex = destVertex
        while currentVertex.arrivedFrom != None:
            result.append(currentVertex.arrivedFrom)
            currentVertex = currentVertex.arrivedFrom.oppositeVertex(currentVertex)
        return result

    def minimalSpanningTree(self, initialVertex=None):
        """
        Algorytm do generowania drzewa rozpinającego.
        """
        for vertex in self.vertexIndex.values():
            vertex.IWasHere = False

        if initialVertex == None:
            currentVertex = self.getVertex(min(self.vertexIndex))
        elif isinstance(initialVertex, str):
            currentVertex = self.getVertex(initialVertex)
        else:
            currentVertex = initialVertex
        usedVerticles = {currentVertex}
        currentVertex.IWasHere = True
        resultEdges = set()
        while len(usedVerticles) < len(self.vertexIndex) and len(resultEdges) < len(self.vertexIndex) - 1:
            edgeSet = set()
            for vertex in usedVerticles:
                edgeSet = edgeSet.union(set(edge for edge in vertex.outEdges.values() if not edge.oppositeVertex(vertex).IWasHere))
            minWeight = min(edge.weight for edge in edgeSet)
            minEdge = [edge for edge in edgeSet if edge.weight == minWeight][0]
            minEdge.startVertex.IWasHere = True
            minEdge.endVertex.IWasHere = True
            usedVerticles.add(minEdge.startVertex)
            usedVerticles.add(minEdge.endVertex)
            resultEdges.add(minEdge)

        return resultEdges

    def Kosaraju(self):
        vertices = self.vertexIndex.values()

        d = [[-1, i] for i in vertices]  # czas odwiedzenia wierzchołka
        f = [[-1, i] for i in vertices]  # czas przetworzenia wierzchołka

        t = 0
        for i in d:
            if i[0] == -1:
                Graph.DFSvisit(i[1], self, d, f, t)
        G_t = self.transpose()
        nr = 0
        comp = [[-1, v] for v in vertices]  # wszystkie wierzchołki są nieodwiedzone

        f.sort(key=lambda y: y[0], reverse=True)
        for i in f:
            idx = Graph.idxOfVertexInTuple(comp, i[1])
            if comp[idx][0] == -1:
                nr = nr + 1
                comp[idx][0] = nr
                Graph.components_R(nr, i[1], G_t, comp)
        return comp

    @staticmethod
    def DFSvisit(v, G, d, f, t):
        t = t + 1
        idx = Graph.idxOfVertexInTuple(d, v)
        d[idx][0] = t
        for i in v.adjacentVertices():
            idx = Graph.idxOfVertexInTuple(d, i)
            if d[idx][1] == -1:
                Graph.DFSvisit(d[idx][0], G, d, f, t)

        t = t + 1
        idx = Graph.idxOfVertexInTuple(f, v)
        f[idx][0] = t

    @staticmethod
    def idxOfVertexInTuple(t, v: Vertex):
        """
        Funkcja zwraca indeks szukanego wierzchołka w liście krotek
        [(wartosc, wierzcholek)...]
        t - lista krotek
        v - obiekt klasy Vertex
        """
        temp = [i[1] for i in t]
        try:
            output = temp.index(v)
        except ValueError:
            for idx, i in enumerate(t):
                if i[1].getLabel() == v.getLabel():
                    return idx

        return output

    def transpose(self):
        """
        Metoda zwraca kopię transponowaną kopię grafu.
        """
        transpozed = self.copy()
        for v in transpozed.edgeIndex.values():
            v.switchDirection()
        return transpozed

    def distanceMatrix(self):
        """
        Metoda zwraca tablice odleglosci
        """
        distanceMatrix = []

        for vertex in self.vertexIndex.values():
            pathCosts = self.DijkstraDistance(vertex)
            distanceMatrix.append(list(pathCosts.values()))
        return distanceMatrix


def graphCenterFromDistanceMatrix(distanceMatrix):

    totalDistanceFromOthers = {}
    finalTotalDistance = {}

    for index, row in enumerate(distanceMatrix, start=1):  # wierzcholki liczymy od 1
        totalDistanceFromOthers[index] = sum(row)

    minVal = min(totalDistanceFromOthers.values())
    indexes_of_centre_vertices = [k for k, v in totalDistanceFromOthers.items() if v == minVal]
    for i in indexes_of_centre_vertices:
        finalTotalDistance[i] = totalDistanceFromOthers[i]

    return finalTotalDistance


def graphMiniMaxCenterFromDistanceMatrix(distanceMatrix):

    maxDistancetoFarthestVertex = {}
    finalTotalDistance = {}
    for index, row in enumerate(distanceMatrix, start=1): # wierzcholki liczymy od 1
        maxDistancetoFarthestVertex[index] = max(row)

    minVal = min(maxDistancetoFarthestVertex.values())
    indexes_of_centre_vertices = [k for k, v in maxDistancetoFarthestVertex.items() if v == minVal]
    for i in indexes_of_centre_vertices:
        finalTotalDistance[i] = minVal

    return finalTotalDistance


#  _____       _
# |_   _|__ __| |_ ___
#   | |/ -_|_-<  _(_-<
#   |_|\___/__/\__/__/                

def testDirectionalGraph():
    g = Graph(True)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex().label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1", weight=1.1).label == "e3"
    assert g.addEdge("v2", "v1", weight=1).label == "e4"
    assert g.equals(g)
    print(g.createAdjacencyMatrix())
    print(g.createAdjacencyList())
    print(g.createIncidenceMatrix())
    assert str(g) != None
    print(g)
    assert g.getEdge("e1").oppositeVertex("v1").label == "v2"
    assert g.getEdge("e1").oppositeVertex("v2").label == "v1"
    g2 = g.copy()
    assert g.equals(g2)
    assert g2.equals(g)
    assert len(g.vertexIndex) == len(g2.vertexIndex)
    assert len(g.edgeIndex) == len(g2.edgeIndex)
    assert g.findEdges("v2", "v3").label == "e2"
    assert g.findEdges("v3", "v2") == None
    assert g.getVertex("v1").inEdges != g.getVertex("v1").outEdges
    assert len(g.getVertex("v1").outEdges) == 1
    assert len(g.getVertex("v1").inEdges) == 2
    assert len(g.vertexIndex) == 3
    assert len(g.edgeIndex) == 4
    assert g.getVertex("v1").removeMe()
    assert len(g.vertexIndex) == 2
    assert len(g.edgeIndex) == 1


def testUndirectionalGraph():
    g = Graph(False)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
    assert g.getEdge("e1").oppositeVertex("v1").label == "v2"
    assert g.getEdge("e1").oppositeVertex("v2").label == "v1"
    assert g.equals(g)
    print(g.createAdjacencyMatrix())
    print(g.createAdjacencyList())
    print(g.createIncidenceMatrix())
    assert str(g) != None
    print(g)
    g2 = g.copy()
    assert g.equals(g2)
    assert g2.equals(g)
    assert len(g.vertexIndex) == len(g2.vertexIndex)
    assert len(g.edgeIndex) == len(g2.edgeIndex)
    assert g.findEdges("v2", "v3").label == "e2"
    assert g.findEdges("v3", "v2").label == "e2"
    assert g.getVertex("v1").inEdges == g.getVertex("v1").outEdges
    try:
        g.addEdge("v2", "v1")
        assert False
    except:
        assert True
    assert g.removeVertex("v1")
    assert len(g.vertexIndex) == 2
    assert len(g.edgeIndex) == 1


def testUndirectionalGraphDrawing():
    g = Graph(False)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addVertex(g.proposalVertexName()).label == "v4"
    assert g.addVertex(g.proposalVertexName()).label == "v5"
    assert g.addVertex(g.proposalVertexName()).label == "v6"
    assert g.addVertex(g.proposalVertexName()).label == "v7"
    assert g.addVertex(g.proposalVertexName()).label == "v8"
    assert g.addVertex(g.proposalVertexName()).label == "v9"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v4").label == "e3"
    assert g.addEdge("v4", "v5").label == "e4"
    assert g.addEdge("v5", "v6").label == "e5"
    assert g.addEdge("v6", "v7").label == "e6"
    assert g.addEdge("v7", "v8").label == "e7"
    assert g.addEdge("v8", "v9").label == "e8"
    assert g.addEdge("v9", "v1").label == "e9"
    assert g.addEdge("v9", "v2").label == "e10"
    assert g.addEdge("v6", "v4").label == "e11"
    assert g.addEdge("v3", "v7").label == "e12"
    drawGraph.drawVertexes(g, 3, 'test1.png')


def testTakeDownDirectional():
    g = Graph(True)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
    assert g.addEdge("v2", "v1").label == "e4"
    assert g.getVertex("v1").degree == 3
    assert g.getVertex("v2").degree == 3
    assert g.getVertex("v3").degree == 2

    print(g)
    assert g.takeEdgeDown("e2", "newV").label == "newV"
    print(g)
    assert g.getVertex("newV") != None
    assert g.getVertex("newV").label == "newV"
    assert g.getEdge("e2") == None
    assert g.getVertex("v2") == None
    assert g.getVertex("v3") == None

    assert g.getVertex("v1").degree == 3
    assert g.getVertex("newV").degree == 3

    assert g.getEdge("e1").endVertex.label == "newV"
    assert g.getEdge("e3").startVertex.label == "newV"
    assert g.getEdge("e4").startVertex.label == "newV"

    assert g.getEdge("e1").startVertex.label != "v2"
    assert g.getEdge("e1").startVertex.label != "v3"
    assert g.getEdge("e3").startVertex.label != "v2"
    assert g.getEdge("e3").startVertex.label != "v3"
    assert g.getEdge("e4").startVertex.label != "v2"
    assert g.getEdge("e4").startVertex.label != "v3"

    assert g.getEdge("e1").endVertex.label != "v2"
    assert g.getEdge("e1").endVertex.label != "v3"
    assert g.getEdge("e3").endVertex.label != "v2"
    assert g.getEdge("e3").endVertex.label != "v3"
    assert g.getEdge("e4").endVertex.label != "v2"
    assert g.getEdge("e4").endVertex.label != "v3"

    assert g.equals(g)


def testTakeDownUndirectional():
    g = Graph(False)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
    assert g.addEdge("v2", "v1").label == "e4"
    assert g.getVertex("v1").degree == 3
    assert g.getVertex("v2").degree == 3
    assert g.getVertex("v3").degree == 2

    print(g)
    assert g.takeEdgeDown("e2", "newV").label == "newV"
    print(g)
    assert g.getVertex("newV") != None
    assert g.getVertex("newV").label == "newV"
    assert g.getEdge("e2") == None
    assert g.getVertex("v2") == None
    assert g.getVertex("v3") == None

    assert g.getVertex("v1").degree == 3
    assert g.getVertex("newV").degree == 3

    assert g.getEdge("e1").endVertex.label == "newV"
    assert g.getEdge("e3").startVertex.label == "newV"
    assert g.getEdge("e4").startVertex.label == "newV"

    assert g.getEdge("e1").startVertex.label != "v2"
    assert g.getEdge("e1").startVertex.label != "v3"
    assert g.getEdge("e3").startVertex.label != "v2"
    assert g.getEdge("e3").startVertex.label != "v3"
    assert g.getEdge("e4").startVertex.label != "v2"
    assert g.getEdge("e4").startVertex.label != "v3"

    assert g.getEdge("e1").endVertex.label != "v2"
    assert g.getEdge("e1").endVertex.label != "v3"
    assert g.getEdge("e3").endVertex.label != "v2"
    assert g.getEdge("e3").endVertex.label != "v3"
    assert g.getEdge("e4").endVertex.label != "v2"
    assert g.getEdge("e4").endVertex.label != "v3"

    assert g.equals(g)


def testLoaders():
    for direction in [True, False]:
        g = Graph(direction)
        assert g != None
        assert g.addVertex(g.proposalVertexName()).label == "v1"
        assert g.addVertex(g.proposalVertexName()).label == "v2"
        assert g.addVertex(g.proposalVertexName()).label == "v3"
        assert g.addEdge("v1", "v2").label == "e1"
        assert g.addEdge("v2", "v3").label == "e2"
        assert g.addEdge("v3", "v1").label == "e3"

        g1 = Graph(direction).loadAdjacencyMatrix(g.createAdjacencyMatrix())
        g2 = Graph(direction).loadAdjacencyMatrix(g1.createAdjacencyMatrix())
        assert g1.equals(g2)
        if direction:
            assert g.equals(g1)
            assert g.equals(g2)

        g1 = Graph(direction).loadAdjacencyList(g.createAdjacencyList())
        g2 = Graph(direction).loadAdjacencyList(g1.createAdjacencyList())
        assert g1.equals(g2)
        if direction:
            assert g.equals(g1)
            assert g.equals(g2)

        g1 = Graph(direction).loadIncidenceMatrix(g.createIncidenceMatrix())
        g2 = Graph(direction).loadIncidenceMatrix(g1.createIncidenceMatrix())
        assert g1.equals(g2)
        if direction:
            assert g.equals(g1)
            assert g.equals(g2)

        g1 = Graph(direction).loadAdjacencyMatrix(g.createAdjacencyMatrix()[1])
        g2 = Graph(direction).loadAdjacencyMatrix(g1.createAdjacencyMatrix()[1])
        assert g1.equals(g2)
        if direction:
            assert g.equals(g1)
            assert g.equals(g2)

        g1 = Graph(direction).loadIncidenceMatrix(g.createIncidenceMatrix()[2])
        g2 = Graph(direction).loadIncidenceMatrix(g1.createIncidenceMatrix()[2])
        assert g1.equals(g2)
        if direction:
            assert g.equals(g1)
            assert g.equals(g2)


def testTextLoaders():
    g = Graph(directed=False)
    for _ in range(6):
        g.addVertex()
    g.addEdge("v1", "v2")
    g.addEdge("v3", "v4")
    g.addEdge("v4", "v5")
    g.addEdge("v5", "v3")
    g.addEdge("v6", "v3")
    g.addEdge("v1", "v3")
    drawGraph.drawVertexes(g, 4, 'testText.png')

    g.printAdjacencyList()
    g.printAdjacencyMatrix()
    g.printIncidenceMatrix()


def testRandomGraphGenerator():
    g = Graph.generateRandomGraph(10, 15, directed=False)
    drawGraph.drawVertexes(g, 3, 'random.png')
    print("Generated graph:")
    # drawGraph.drawVertexes(g, 3, 'g.png')
    print(g)

    g2 = Graph.generateRandomGraphProbability(5, 0.5, directed=False)
    print("Generated graph:")
    print(g2)


def testComponents():
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

    g.components()


def testKosaraju():
    from drawGraph import drawDirectedGraphWithWeights
    g = Graph.generateRandomGraph(15, 15, directed=True)
    output = g.Kosaraju()

    nr = set()
    for i in output:
        nr.add(i[0])

    for i in nr:
        for j in output:
            if i == j[0]:
                print(f"Spojna skladowa nr: {i}  :   {j[1].getLabel()}")

    drawDirectedGraphWithWeights(g, 4, "Kosaraju.png")


def test():
    print("Testing...")

    testDirectionalGraph()
    testUndirectionalGraph()
    testTakeDownDirectional()
    testTakeDownUndirectional()
    testLoaders()
    testTextLoaders()
    testRandomGraphGenerator()
    testUndirectionalGraphDrawing()
    testComponents()
    testKosaraju()

    print("Done.")


def generateDocumentation(moduleName: str = "graphs"):
    try:
        print("Generating documentation...")
        from sys import platform
        from os import system as shell
        if platform == "linux" or platform == "linux2":
            shell("pydoc3 '" + moduleName + "' | head -n -5 > '" + moduleName + "_documentation.txt'")
        shell("pydoc3 -w '" + moduleName + "'")
        return False
    except:
        return False


# __  __      _
# |  \/  |__ _(_)_ _  
# | |\/| / _` | | ' \ 
# |_|  |_\__,_|_|_||_|

if __name__ == "__main__":
    import drawGraph

    test()
    generateDocumentation()
