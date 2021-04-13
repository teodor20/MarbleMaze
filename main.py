from typing import List

import cv2
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import self as self

zoom = 20
borders = 6
images = []

def draw_matrix(filledMaze, emptyMaze, the_path = []):
    im = Image.new('RGB', (zoom * len(filledMaze[0]), zoom * len(filledMaze)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(filledMaze)):
        for j in range(len(filledMaze[i])):
            color = (255, 255, 255)
            r = 0
            if filledMaze[i][j] == 1:
                color = (0, 0, 0)
            if i == start[0] and j == start[1]:
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if emptyMaze[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=(255,0,0))
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0,0), width=5)
    draw.rectangle((0, 0, zoom * len(filledMaze[0]), zoom * len(filledMaze)), outline=(0,255,0), width=2)
    images.append(im)


#Start
img = cv2.imread('./maze.jpg')

# Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Bluring
gray = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)

# Thresholding
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

x, y, w, h = cv2.boundingRect(biggest_contour)
cropped = img[y: y + h, x: x + w]

# first mask
lower = (50, 50, 50)
upper = (255, 255, 255)

first_mask = cv2.inRange(cropped, lower, upper)
cropped[first_mask != 0] = [255, 255, 255]

# Work with cropped image
cvt = 75  # or 77
dc = 70  # or 80 if above is 77
hsv = cv2.cvtColor(cropped, cvt)
lower = (80, 80, 80)
upper = (80 + dc, 80 + dc, 80 + dc)  # upper bound for each channel

# create the mask and use it to change the colors
shadow_mask = cv2.inRange(hsv, lower, upper)
cropped[shadow_mask != 0] = [255, 255, 255]

# Resize2
w, h = (529, 529)
temp = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
cv2.imshow('Input', temp)
cv2.waitKey()

# Split into tiles
tile_height = 23;
tile_width = 23;
tiles = temp.reshape((tile_height, h // tile_height,
                      tile_width, w // tile_width, temp.shape[2])).swapaxes(1, 2)

# Create the maze in 2d array
arr = np.ones(shape=(tile_height, tile_width))

for y in range(tile_height):
    for x in range(tile_width):
        current_tile = tiles[y, x]
        ret, thresh = cv2.threshold(current_tile, 127, 255, cv2.THRESH_BINARY_INV)

        pixelValue = 0
        for i in range(0, tile_height):
            for j in range(0, tile_width):
                pixelValue += thresh[i, j][0]

        mean = pixelValue / 529
        arr[y][x] = 1 if mean > 55 else 0

print(arr)

# # Resolve the maze
# print("Resolving the maze")

def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
    visited = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dest = (destination[0], destination[1])


    def rollFrom(pos):
        # check all possible stop positions that current pos can roll to
        # and exclude those that are already in visited
        # and then keep rolling from the rest
        print("rolling from {}".format(pos))
        the_path.append(pos)
        newStops = []
        for d in dirs:
            newX = pos[0]
            newY = pos[1]
            while (True):  # rolling
                possibleNewX = newX + d[0]
                possibleNewY = newY + d[1]
                if (possibleNewX >= 0 and possibleNewX < len(maze)) and (
                        possibleNewY >= 0 and possibleNewY < len(maze[0])) and (maze[possibleNewX][possibleNewY] != 1):
                    newX = possibleNewX
                    newY = possibleNewY
                    continue
                else:
                    break
            newStop = (newX, newY)

            if newStop == dest:
                return True
            newStops.append(newStop)

        visited.append(pos)

        for newStop in newStops:
            if newStop not in visited:
                if rollFrom(newStop):
                    return True
        return False


    startPos = (start[0], start[1])
    return rollFrom(startPos)

start = 0, 0
end = 22, 22
the_path = []
hasPath(self, arr, start, end)
print(the_path)

############ Trim the path #############

good_path = the_path.copy()
for i in range(len(the_path)):
    currentPos = the_path[i]
    if (i != 0 and i != (len(the_path) - 1)):
        previousPos = the_path[i-1]
        nexPos = the_path[i+1]

        if (currentPos[0] == previousPos[0] and currentPos[0] == nexPos[0]):
            good_path.remove(currentPos)

        if (currentPos[1] == previousPos[1] and currentPos[1] == nexPos[1]):
            good_path.remove(currentPos)

print(good_path)
########################################

############ Create move instructions #############

instructions = []
for i in range(len(good_path) - 1):
    currentPos = good_path[i]
    nextPos = good_path[i + 1]

    #Checks for small frame
    if (nextPos[0] == currentPos[0] and nextPos[1] > currentPos[1]):
        instructions.append("right")
    elif (nextPos[0] == currentPos[0] and nextPos[1] < currentPos[1]):
        instructions.append("left")

    # Checks for big frame
    if (nextPos[1] == currentPos[1] and nextPos[0] > currentPos[0]):
        instructions.append("down")
    elif (nextPos[1] == currentPos[1] and nextPos[0] < currentPos[0]):
        instructions.append("up")

print(instructions)

###################################################

############ Create the GIF file #############

newMaze = np.zeros(shape=(tile_height + 2, tile_width + 2))
newMaze[start[0], start[1]] = 1

for i in range(10):
    if i % 2 == 0:
        draw_matrix(arr, newMaze, good_path)
    else:
        draw_matrix(arr, newMaze)

images[0].save('maze.gif',
               save_all=True, append_images=images[1:],
               optimize=False, duration=3, loop=0)

##############################################

############### Move the maze ################



##############################################

#     cvt = 67  # or 41
#     dc = 112
#
#     if dc < 1:
#         dc = 0
#
#     while True:
#         try:
#
#             img = cv2.cvtColor(cropped, cvt)
#             lower = (80, 80, 80)
#             upper = (80 + dc, 80 + dc, 80 + dc)
#
#             mask = cv2.inRange(img, lower, upper)
#
#             cv2.imshow('mask', cv2.resize(mask, (640, 480)))
#
#         except:
#             pass
#
#         k = cv2.waitKey(33) & 0xFF
#         if k == ord('1'):
#             cvt -= 1
#             print(cvt)
#         if k == ord('2'):
#             cvt += 1
#             print(cvt)
#         if k == ord('3'):
#             dc -= 1
#             print("dc ", dc, lower, upper)
#         if k == ord('4'):
#             dc += 1
#             print("dc ", dc, lower, upper)
#
#         if k == ord('c'): break
