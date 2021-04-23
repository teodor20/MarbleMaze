import servosPigpio
import path
import imageProcessing
import sys

end = (22, 22)

def getBestPath():
    # Get the maze from a photo
    maze, ballPosition = imageProcessing.getMaze()
    #print(maze)
    print("Ball Position: ", ballPosition)

    # Resolve the maze
    if ballPosition == end:
        print("End reached")
        servosPigpio.stopMotors()
        sys.exit("End reached")

    best_path = path.getPath(maze, ballPosition, end)

    if best_path == "Impossible":
        print("No path")
        servosPigpio.stopMotors()
        sys.exit("No path")

    return best_path


def recursiveMovement():
    path = getBestPath()
    print(path)
    servosPigpio.start([path[0]])
    recursiveMovement()

def startMarbleMaze():
    servosPigpio.startMotors()
    recursiveMovement()

startMarbleMaze()
