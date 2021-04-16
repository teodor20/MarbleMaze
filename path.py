import collections
import heapq
from typing import List


def shortestDistance(maze: List[List[int]], start: List[int], destination: List[int]):
    start, destination = tuple(start), tuple(destination)
    row, col = len(maze), len(maze[0])
    moves = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    dstr = ['u', 'r', 'l', 'd']
    # change order of properties so comparison works as intended
    Point = collections.namedtuple("Point", "distance, length, directions, coordinates")

    heap = [Point(0, 0, "", start)]
    visited = set()
    while heap:
        point = heapq.heappop(heap)
        dist = point.distance
        directions = point.directions
        node = point.coordinates

        if node in visited: continue
        if node == destination:
            return directions

        visited.add(node)

        for idx, move in enumerate(moves):
            dx, dy = move
            newX = node[0]
            newY = node[1]
            distance = dist
            newDirections = directions

            while 0 <= newX + dx < row and 0 <= newY + dy < col and maze[newX + dx][newY + dy] == 0:
                newX += dx
                newY += dy
                distance += 1
                if (newX, newY) == destination:
                    break

            if (newX, newY) not in visited:
                heapq.heappush(heap, Point(distance, len(newDirections) + 1, newDirections + dstr[idx], (newX, newY)))

    return "Impossible"

############ Create move instructions #############
def getPath(maze, start, end):
    shortest_path = shortestDistance(maze, start, end)
    instructions = []
    for letter in shortest_path:
        if letter == 'u':
            instructions.append("Up")
        elif letter == 'd':
            instructions.append("Down")
        elif letter == 'l':
            instructions.append("Left")
        elif letter == 'r':
            instructions.append("Right")

    return instructions