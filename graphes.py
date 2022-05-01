"""
   ___               _           
  / __|_ _ __ _ _ __| |_  ___ ___
 | (_ | '_/ _` | '_ \ ' \/ -_|_-<
  \___|_| \__,_| .__/_||_\___/__/
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
        - w przypadku wywołań dla wielu wierchołków lepiej użyć odpowiedniej metody z klasy Graph,
        lub odwołac się bezpośrednio do pola degree.
        """               
        if self.getGraph().isDirected():
            self.inputDegree = len(self.inEdges)
            self.outputDegree = len(self.outEdges)
            self.degree = self.inputDegree + self.outputDegree
        else:
            dictTab = {True: 1, False: 0}
            self.degree = sum(dictTab.get(edge.startVertex == self) + dictTab.get(edge.endVertex == self) for edge in self.allEdgesSet());
            self.inputDegree = self.degree
            self.outputDegree = self.degree
    
    def removeMe(self):
        return self.graph.removeVertex(self)
    
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
    
    def __init__(self, startVertex: Vertex, endVertex: Vertex, label: str, wage: float = 1.0):
        assert startVertex.graph == endVertex.graph
        self.label = label
        self.wage: float = wage
        self.startVertex: Vertex = startVertex
        self.endVertex: Vertex = endVertex
        self.startVertex.outEdges.update({label: self})
        self.endVertex.inEdges.update({label: self})
        
    def getGraph(self):
        assert self.startVertex.graph == self.endVertex.graph
        return self.startVertex.getGraph()
    
    def removeMe(self):
        return self.getGraph().removeEdge(self)    
    
    def opposideVertex(self, vertex: Vertex):
        """
        Zwraca wierzchołek po przeciwnej stronie krawędzi, niż ten podany w parametrze.
        Jako parametr przyjmuje referencję do wierzchołka lub jego etykietę.
        Używać w przypadku wędrówek po grafach nieskierowanych.
        """
        if vertex == self.startVertex or vertex == self.startVertex.label:
            return self.endVertex
        return self.startVertex
    
    def equals(self, another):
        if not isinstance(another, Edge):
            return False
        if self.label != another.label:
            return False
        if self.startVertex.label != another.startVertex.label or self.endVertex.label != another.endVertex.label:
            return False
        if self.wage != another.wage:
            return False
        return True
    
    def __str__(self):
        return "(" + self.label + ": " + self.startVertex.label + " -> " + self.endVertex.label + (", wage = " + str(self.wage) if self.wage != 1.0 else "") + ")"
        
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
    
    def calculateDegreeOfVertexes(self):
        """
        Aktualizuje dla wszystkich wierzchołków stopnie wejściowe i wyjściowe.
        Używać w przypadku zmian wierzhcołków lub krawędzi poza klasą, w celu utrzymania spójności danych.
        Wynik znajduje się w nowo powstałym polu każdego wierzchołka:
            "degree" dla grafu nieskierowanego (degree = inputDegree + outputDegree dla skierowanego),
            "inputDegree" i "outputDegree" dla grafu skierowanego (inputDegree = outputDegree = degree dla nieskierowanego)
        """
        for vertex in self.vertexIndex.values():
            vertex.degree: int = 0
            vertex.inputDegree: int = 0
            vertex.outputDegree: int = 0
            
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
    
    def addEdge(self, startVertex, endVertex, label: str = None, wage: float = 1.0):
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
        newEdge: Egde = Edge(startVertex, endVertex, label, wage)
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
        labels = set(startVertex.outEdges.keys()).intersection(set(endVertex.inEdges.keys()))
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
            self.addEdge(edge.startVertex.label, edge.endVertex.label, edge.label, edge.wage)
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
        """
        vertexList = self.vertexIndex.values()
        vertexLabelList = [vertex.label for vertex in vertexList]
        matrix = [[0.0 for i in vertexList] for j in vertexList] 
        for i, vertex1 in enumerate(vertexList):
            for j, vertex2 in enumerate(vertexList):
                matrix[i][j] += sum(edge.wage for edge in self.findEdges(vertex1, vertex2, True))                
        return (vertexLabelList, matrix)
    
    def loadAdjacencyMatrix(self, matrix):
        """
        Dodaje strukturę z macierzy sąsiedztwa.
        Nie ma pewności, że zostanie otrzymany ten sam graf, co przy zapisie
        (np.: w przypadku wystąpienia wielokrotnych krawędzi).
        Nie sprawdza poprawnośc zapisu.
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
                if matrix[i][j] != 0:
                    self.addEdge(vertex1, vertex2, wage=matrix[i][j])
                if (not self.isDirected()) and (j > i):
                    break        
        return self
    
    def createAdjacencyList(self):
        """
        Tworzy listę sąsiedztwa.
        """
        result = []
        for edge in self.edgeIndex.values():
            result.append((edge.label, edge.startVertex.label, edge.endVertex.label, edge.wage)) 
        return result
    
    def loadAdjacencyList(self, dataList):
        """
        Dodaje strukturę z listy sąsiedztwa.
        Nie sprawdza poprawnośc zapisu.
        """
        for record in dataList:
            vertex1 = self.getOrAddVertex(record[1])
            vertex2 = self.getOrAddVertex(record[2])
            self.addEdge(vertex1, vertex2, label=record[0], wage=record[3])
        return self
    
    def createIncidenceMatrix(self):
        """
        Tworzy macierz incydencji.
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
        """
        if isinstance(data, tuple):
            edgeLabelList = data[0]
            vertexLabelList = data[1]
            matrix = data[2]
        else:
            matrix = data
            edgeLabelList = ["e" + str(i) for i in range(len(matrix))]
            vertexLabelList = ["v" + str(i) for i in range(len(matrix[0]))]
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
    assert g.addEdge("v3", "v1", wage = 1.1).label == "e3"
    assert g.addEdge("v2", "v1", wage = 1).label == "e4"
    assert g.equals(g)
    print(g.createAdjacencyMatrix())
    print(g.createAdjacencyList())
    print(g.createIncidenceMatrix())
    assert str(g) != None
    print(g)
    assert g.getEdge("e1").opposideVertex("v1").label == "v2"
    assert g.getEdge("e1").opposideVertex("v2").label == "v1"
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
    assert g.getEdge("e1").opposideVertex("v1").label == "v2"
    assert g.getEdge("e1").opposideVertex("v2").label == "v1"
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
    g = Graph(True)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
    
    g1 = Graph(True).loadAdjacencyMatrix(g.createAdjacencyMatrix())
    g2 = Graph(True).loadAdjacencyMatrix(g1.createAdjacencyMatrix())
    assert g1.equals(g2)
    assert g.equals(g2)
    
    g1 = Graph(True).loadAdjacencyList(g.createAdjacencyList())
    g2 = Graph(True).loadAdjacencyList(g1.createAdjacencyList())
    assert g1.equals(g2)
    assert g.equals(g2)
    
    g1 = Graph(True).loadIncidenceMatrix(g.createIncidenceMatrix())
    g2 = Graph(True).loadIncidenceMatrix(g1.createIncidenceMatrix())
    assert g1.equals(g2)
    assert g.equals(g2)
    
    
def test():
    print("Testing...")
    
    testDirectionalGraph()
    testUndirectionalGraph()
    testTakeDownDirectional()
    testTakeDownUndirectional()
    testLoaders()
    
    print("Done.")

def generateDocumentation(moduleName: str = "graphes"):
    try:
        from sys import platform
        if platform == "linux" or platform == "linux2":            
            from os import system as shell
            shell("pydoc3 -w '" + moduleName + "'")    
            shell("pydoc3 '" + moduleName + "' | head -n -5 > '" + moduleName + "_documentation.txt'")  
            return True
        return False
    except:
        return False

# __  __      _      
# |  \/  |__ _(_)_ _  
# | |\/| / _` | | ' \ 
# |_|  |_\__,_|_|_||_|
                            
if __name__ == "__main__":
    test()
    generateDocumentation()
