import cv2
import numpy as np
from PIL import Image, ImageDraw
import servosPigpio
import path

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
img = cv2.imread('images/maze.jpg')

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
ballPosition = 0, 0
foundMarble = False
for y in range(tile_height):
    for x in range(tile_width):
        current_tile = tiles[y, x]
        ret, thresh = cv2.threshold(current_tile, 127, 255, cv2.THRESH_BINARY_INV)

        pixelValue = 0
        for i in range(0, tile_height):
            for j in range(0, tile_width):
                pixelValue += thresh[i, j][0]

        mean = pixelValue / 529
        #arr[y][x] = 1 if mean > 55 else 0
        if (foundMarble == False) and (mean < 43) and (mean > 25):
            arr[y][x] = 0
            foundMarble = True
            ballPosition = y, x
        elif mean > 55:
            arr[y][x] = 1
        else:
            arr[y][x] = 0


# Check pixel value of first cell
# firstTile = tiles[0][0]
# pixelValue = 0
# ret, thresh = cv2.threshold(firstTile, 127, 255, cv2.THRESH_BINARY_INV)
#
# for i in range(0, tile_height):
#     for j in range(0, tile_width):
#         pixelValue += thresh[i, j][0]
#
# mean = pixelValue / 529
# print(mean)

print(arr)

# # Resolve the maze
# print("Resolving the maze")

start = ballPosition
print("Ball Position: ",  ballPosition)

start = (0, 0)
end = (22, 22)
the_path = []
best_path = path.getPath(arr, start, end)
print(best_path)

###################################################

############### Move the maze ################

servosPigpio.start(best_path)

##############################################





############ Create the GIF file #############

newMaze = np.zeros(shape=(tile_height + 2, tile_width + 2))
newMaze[start[0], start[1]] = 1

for i in range(10):
    if i % 2 == 0:
        draw_matrix(arr, newMaze, best_path)
    else:
        draw_matrix(arr, newMaze)

images[0].save('images/maze.gif',
               save_all=True, append_images=images[1:],
               optimize=False, duration=3, loop=0)