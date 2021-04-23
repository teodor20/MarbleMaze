import servosPigpio
import path
import imageProcessing

#Get the maze from a photo /home/pi/Desktop/image.jpg
maze, ballPosition = imageProcessing.getMaze()
print(maze)


############### Resolve the maze #############
start = ballPosition
print("Ball Position: ",  ballPosition)

end = (22, 22)
the_path = []
best_path = path.getPath(maze, ballPosition, end)
print(best_path)

###################################################


############### Move the maze ################

#servosPigpio.start(best_path)

##############################################