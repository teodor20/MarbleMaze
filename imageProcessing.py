import cv2
import numpy as np
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1600, 1200)
camera.brightness = 50
sleep(2)

def getMaze():
    #Load the image
    img = captureImage()

    #x, y, w, h = findMazeCoordinates(img)
    x, y, w, h = 125, 59, 1100, 1075
    cropped = img[y: y + h, x: x + w]

    #Resize
    w, h = (529, 529)
    temp = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
    # cv2.imshow('Input', temp)
    # cv2.waitKey()

    #Split into tiles
    tile_height = 23;
    tile_width = 23;
    tiles = temp.reshape((tile_height, h // tile_height,
                          tile_width, w // tile_width, temp.shape[2])).swapaxes(1, 2)

    # Create the maze in 2d array
    arr = np.ones(shape=(tile_height, tile_width))
    foundMarble = False
    ballPosition = (0, 0)
    for y in range(tile_height):
        for x in range(tile_width):
            current_tile = tiles[y, x]

            # Get the ball position
            if foundMarble is False and checkIfBall(current_tile):
                foundMarble = True
                ballPosition = (y, x)

            # Apply masks
            applyMasks(current_tile)

            # Create the maze
            ret, thresh = cv2.threshold(current_tile, 100, 255, cv2.THRESH_BINARY)
            pixelValue = 0
            for i in range(0, tile_height):
                for j in range(0, tile_width):
                    pixelValue += thresh[i, j][0]

            mean = pixelValue / 529
            arr[y][x] = 1 if mean < 150 else 0

    return arr, ballPosition

def checkIfBall(tile):
    # Convert the image to HSV colour space
    hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    # Define a range for blue color
    hsv_l = np.array([100, 150, 0])
    hsv_h = np.array([120, 255, 255])
    # Find blue pixels in the image
    dst = cv2.inRange(hsv, hsv_l, hsv_h)
    # Count the blue pixels
    no_blue = cv2.countNonZero(dst)
    return no_blue > 50

def applyMasks(tile):
    # Apply first mask
    lower = (0, 0, 0)
    upper = (55, 55, 55)

    first_mask = cv2.inRange(tile, lower, upper)
    tile[first_mask != 0] = [255, 255, 255]

    # Apply second mask
    lower = (0, 60, 40)
    upper = (255, 255, 255)

    first_mask = cv2.inRange(tile, lower, upper)
    tile[first_mask != 0] = [255, 255, 255]

def captureImage():
    camera.capture('images/test.jpg')
    img = cv2.imread('images/test.jpg')
    return img

def findMazeCoordinates(img):
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('Input', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Input', gray)
    cv2.waitKey()

    # Bluring
    gray = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow('Input', gray)
    cv2.waitKey()

    # Thresholding
    ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
    cv2.imshow('Input', thresh)
    cv2.waitKey()

    # Find the frame
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    x, y, w, h = cv2.boundingRect(biggest_contour)
    return x, y, w, h