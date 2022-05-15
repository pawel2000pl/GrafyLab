from drawGraph import drawCircularGraph
from graphs import Graph


def prepareGraphForHamilton(graph):
    for i in range(len(graph)):
        graph[i] = graph[i][1]
        for j in range(len(graph[i])):
            graph[i][j] = int(graph[i][j])

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j] -= 1
    return graph


def hamiltonCycle(graph: list, v: int = 0, stack: list = None) -> list:

    if stack is None:
        stack = []
    size = len(graph)
    if v not in set(stack):
        stack.append(v)

        if len(stack) == size:
            if stack[-1] in graph[stack[0]]:
                return [x + 1 for x in stack]
            else:
                stack.pop()
                return None

        for v_n in graph[v]:
            stack_copy = stack[:]
            hamilton_result = hamiltonCycle(graph, v_n, stack_copy)
            if hamilton_result is not None:
                return hamilton_result



