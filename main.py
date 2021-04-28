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
    if ballPosition == False:
        print("Marble is missing")
        servosPigpio.stopMotors()
        sys.exit("Marble is missing")

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


def move(conditionalPathing):
    if True: #Lets always use dynamic pathing for now
        while True:
            path, _ = getBestPath()
            servosPigpio.start([path[0]])
    else:
        path, _ = getBestPath()
        servosPigpio.start(path)

def startMarbleMaze():
    _, conditionalPathing = getBestPath()
    print("Conditional Pathing: ", conditionalPathing)

    servosPigpio.startMotors()
    move(conditionalPathing)

startMarbleMaze()
