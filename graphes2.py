from graphes import *

def isSafe(graph)
def hamiltonCycle(graph, v = "v1", stack: list = None):
    if stack is None:
        stack = []

    size = len(graph)

    if v not in set(stack):
        stack.append(v)
        print(stack)

        if len(stack) == size:
            if [-1] in graph[stack[0]]:
                print(stack[0])
                stack.append(stack[0])
                return [x+1 for x in stack]
            else:
                stack.pop()
                return None

        # for v_n in graph[v]:
        #     stack_copy = stack[:]
        #     hamilton_result = hamiltonCycle(graph, v_n, stack_copy)
        #     if hamilton_result is not None:
        #         return hamilton_result



if __name__ == "__main__":
     g = Graph(False)
     g != None
     g.addVertex(g.proposalVertexName()).label == "v1"
     g.addVertex(g.proposalVertexName()).label == "v2"
     g.addVertex(g.proposalVertexName()).label == "v3"
     g.addVertex(g.proposalVertexName()).label == "v4"
     g.addVertex(g.proposalVertexName()).label == "v5"
     g.addVertex(g.proposalVertexName()).label == "v6"
     g.addVertex(g.proposalVertexName()).label == "v7"
     g.addVertex(g.proposalVertexName()).label == "v8"
     g.addEdge("v1", "v5")
     g.addEdge("v1", "v2")
     g.addEdge("v1", "v4")
     g.addEdge("v2", "v6")
     g.addEdge("v2", "v5")
     g.addEdge("v2", "v3")
     g.addEdge("v3", "v7")
     g.addEdge("v3", "v4")
     g.addEdge("v4", "v7")
     g.addEdge("v4", "v6")
     g.addEdge("v5", "v8")
     g.addEdge("v6", "v8")
     g.addEdge("v7", "v8")
     drawGraph.drawVertexes(g, 4, 'test1.png')
     print(g.createAdjacencyMatrix())
     hamiltonCycle(g.createAdjacencyMatrix())

