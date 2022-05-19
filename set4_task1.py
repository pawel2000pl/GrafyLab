from graphs import Graph
from drawGraph import *
from set3_task1 import connectDanglingVertexes

# ------------------------------------------------------------------------------
# PROJ 4 TASK 1
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    g2 = Graph.generateRandomGraphProbability(7, 0.5, directed=False)
    connectDanglingVertexes(g2)
    drawDirectedGraphWithWeights(g2, 4, "test4.png", False)