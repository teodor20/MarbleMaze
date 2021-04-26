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

    bestPath, conditionalPathing = path.getPath(maze, ballPosition, end)

    if bestPath == "Impossible":
        print("No path")
        servosPigpio.stopMotors()
        sys.exit("No path")

    return bestPath, conditionalPathing


def move(path, conditionalPathing):
    if conditionalPathing:
        while True:
            path, _ = getBestPath()
            servosPigpio.start([path[0]])
    else:
        servosPigpio.start(path)

def startMarbleMaze():
    path, conditionalPathing = getBestPath()
    print("Conditional Pathing: ", conditionalPathing)
    print(path)

    servosPigpio.startMotors()
    move(path, conditionalPathing)

startMarbleMaze()
