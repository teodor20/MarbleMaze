import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import self as self
import image_slicer

def make_step(k, filledMaze, emptyMaze):
    for i in range(len(emptyMaze)):
        for j in range(len(emptyMaze[i])):
            if emptyMaze[i][j] == k:
                if i > 0 and emptyMaze[i - 1][j] == 0 and filledMaze[i - 1][j] == 0:
                    emptyMaze[i - 1][j] = k + 1
                if j > 0 and emptyMaze[i][j - 1] == 0 and filledMaze[i][j - 1] == 0:
                    emptyMaze[i][j - 1] = k + 1
                if i < len(emptyMaze) - 1 and emptyMaze[i + 1][j] == 0 and filledMaze[i + 1][j] == 0:
                    emptyMaze[i + 1][j] = k + 1
                if j < len(emptyMaze[i]) - 1 and emptyMaze[i][j + 1] == 0 and filledMaze[i][j + 1] == 0:
                    emptyMaze[i][j + 1] = k + 1


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
arr = np.ones(shape=(tile_height + 2, tile_width + 2)) #+2 for walls

for y in range(tile_height):
    for x in range(tile_width):
        current_tile = tiles[y, x]
        ret, thresh = cv2.threshold(current_tile, 127, 255, cv2.THRESH_BINARY_INV)

        pixelValue = 0
        for i in range(0, tile_height):
            for j in range(0, tile_width):
                pixelValue += thresh[i, j][0]

        mean = pixelValue / 529
        arr[y+1][x+1] = 1 if mean > 55 else 0

print(arr)

# Resolve the maze
print("Resolving the maze")
start = 0, 0
end = 22, 22

emptyMaze = np.zeros(shape=(tile_height + 2, tile_width + 2))
emptyMaze[start] = 1

print(emptyMaze)

k = 0
while emptyMaze[end[0]][end[1]] == 0:
    k += 1
    make_step(k, arr, emptyMaze)


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
