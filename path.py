import collections
import heapq
from typing import List

def shortestDistance(maze: List[List[int]], start: List[int], destination: List[int]):
    start, destination = tuple(start), tuple(destination)
    row, col = len(maze), len(maze[0])
    moves = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    dstr = ['u', 'r', 'l', 'd']
    Point = collections.namedtuple("Point", "fvalue, distance, length, directions, stepDistances, coordinates")

    heap = [Point(0, 0, 0, "", "", start)]
    visited = set()
    while heap:
        point = heapq.heappop(heap)
        dist = point.distance
        directions = point.directions
        node = point.coordinates
        stepDistances = point.stepDistances

        if node in visited: continue
        if node == destination:
            conditionalPathing = False
            for step in stepDistances:
                if int(step) > 8:
                    conditionalPathing = True

            return directions, conditionalPathing

        visited.add(node)

        for idx, move in enumerate(moves):
            dx, dy = move
            newX = node[0]
            newY = node[1]
            distance = dist
            newDirections = directions
            stepDistance = 0

            while 0 <= newX + dx < row and 0 <= newY + dy < col and maze[newX + dx][newY + dy] == 0:
                newX += dx
                newY += dy
                distance += 1
                stepDistance += 1
                if (newX, newY) == destination:
                    break

            #Use Manhattan distance as heuristics
            heuristics = (abs(newX - destination[0])) + (abs(newY - destination[1]))

            #Cancluate f from distance and heuristics
            fvalue = distance + heuristics

            if (newX, newY) not in visited:
                heapq.heappush(heap, Point(fvalue, distance, len(newDirections) + 1, newDirections + dstr[idx], stepDistances + str(stepDistance), (newX, newY)))

    return "Impossible", False

# Create move instructions
def getPath(maze, start, end):
    shortestPath, conditionalPathing = shortestDistance(maze, start, end)

    if shortestPath == "Impossible":
        return "Impossible"

    instructions = []
    for letter in shortestPath:
        if letter == 'u':
            instructions.append("Up")
        elif letter == 'd':
            instructions.append("Down")
        elif letter == 'l':
            instructions.append("Left")
        elif letter == 'r':
            instructions.append("Right")

    return instructions, conditionalPathing