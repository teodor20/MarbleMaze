import cv2
import numpy as np

def getMaze(imagePath):
    #Load the image
    img = cv2.imread(imagePath)

    #Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('Input', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Input', gray)
    cv2.waitKey()

    #Bluring
    gray = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow('Input', gray)
    cv2.waitKey()

    #Thresholding
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('Input', thresh)
    cv2.waitKey()

    #Find the frame
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    x, y, w, h = cv2.boundingRect(biggest_contour)
    cropped = img[y: y + h, x: x + w]
    cv2.imshow('Input', cropped)
    cv2.waitKey()

    #Apply first mask
    lower = (0, 0, 0)
    upper = (55, 55, 55)

    first_mask = cv2.inRange(cropped, lower, upper)
    cropped[first_mask != 0] = [255, 255, 255]
    cv2.imshow('Input', cropped)
    cv2.waitKey()

    #Apply first mask
    lower = (0, 60, 40)
    upper = (255, 255, 255)

    first_mask = cv2.inRange(cropped, lower, upper)
    cropped[first_mask != 0] = [255, 255, 255]
    cv2.imshow('Input', cropped)
    cv2.waitKey()

    #Resize
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
            ret, thresh = cv2.threshold(current_tile, 100, 255, cv2.THRESH_BINARY)

            pixelValue = 0
            for i in range(0, tile_height):
                for j in range(0, tile_width):
                    pixelValue += thresh[i, j][0]

            mean = pixelValue / 529
            #arr[y][x] = 1 if mean > 55 else 0
            arr[y][x] = 1 if mean < 150 else 0
            # if (foundMarble == False) and (mean < 43) and (mean > 25):
            #     arr[y][x] = 0
            #     foundMarble = True
            #     ballPosition = y, x
            # elif mean > 55:
            #     arr[y][x] = 1
            # else:
            #     arr[y][x] = 0

    return arr

def getBallPosition():
    return (0, 0)