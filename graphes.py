
class Vertex:
    
    def __init__(self, label: str, graph):
        self.label = label
        self.graph = graph
        self.inEdges = {}
        if self.graph.directed:
            self.outEdges = {}
        else:
            self.outEdges = self.inEdges
        
    def removeMe(self):
        self.graph.remove(self)
    
    
class Edge:
    
    def __init__(self, startVertex: Vertex, endVertex: Vertex, label: str, wage: float = 1.0):
        assert startVertex.graph == endVertex.graph
        self.label = label
        self.wage: float = 1.0
        self.startVertex: Vertex = startVertex
        self.endVertex: Vertex = endVertex
        self.startVertex.outEdges.update({label: self})
        self.endVertex.inEdges.update({label: self})
        
    def removeMe(self):
        self.startVertex.graph.remove(self)
        

class Graph:
    
    def __init__(self, directed: bool = False):
        self.vertexIndex = {}
        self.edgeIndex = {}
        self.__vertexProposalNameNumber: int = 0
        self.__edgeProposalNameNumber: int = 0
        self.directed = directed
        
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
    
    

def directionalGraphTest():
    
    g = Graph(True)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
    assert g.addEdge("v2", "v1").label == "e4"
    assert g.findEdges("v2", "v3").label == "e2"
    assert g.findEdges("v3", "v2") == None
    assert g.getVertex("v1").inEdges != g.getVertex("v1").outEdges
    assert len(g.getVertex("v1").outEdges) == 1
    assert len(g.getVertex("v1").inEdges) == 2
    assert len(g.vertexIndex) == 3
    assert len(g.edgeIndex) == 4
    assert g.removeVertex("v1")
    assert len(g.vertexIndex) == 2
    assert len(g.edgeIndex) == 1
    
def undirectionalGraphTest():
    
    g = Graph(False)
    assert g != None
    assert g.addVertex(g.proposalVertexName()).label == "v1"
    assert g.addVertex(g.proposalVertexName()).label == "v2"
    assert g.addVertex(g.proposalVertexName()).label == "v3"
    assert g.addEdge("v1", "v2").label == "e1"
    assert g.addEdge("v2", "v3").label == "e2"
    assert g.addEdge("v3", "v1").label == "e3"
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
        
    
def test():
    print("Testing...")
    
    directionalGraphTest()
    undirectionalGraphTest()
    
    print("Done.")
    
        
if __name__ == "__main__":
    test()
