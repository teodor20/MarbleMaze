import servosPigpio
import path
import imageProcessing

#Get the maze from a photo
maze, ballPosition = imageProcessing.getMaze('images/maze4.jpg')
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

servosPigpio.start(best_path)

##############################################


# ############ Create the GIF file #############
#
# zoom = 20
# borders = 6
# images = []
#
# def draw_matrix(filledMaze, emptyMaze, the_path = []):
#     im = Image.new('RGB', (zoom * len(filledMaze[0]), zoom * len(filledMaze)), (255, 255, 255))
#     draw = ImageDraw.Draw(im)
#     for i in range(len(filledMaze)):
#         for j in range(len(filledMaze[i])):
#             color = (255, 255, 255)
#             r = 0
#             if filledMaze[i][j] == 1:
#                 color = (0, 0, 0)
#             if i == start[0] and j == start[1]:
#                 color = (0, 255, 0)
#                 r = borders
#             if i == end[0] and j == end[1]:
#                 color = (0, 255, 0)
#                 r = borders
#             draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
#             if emptyMaze[i][j] > 0:
#                 r = borders
#                 draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
#                                fill=(255,0,0))
#     for u in range(len(the_path)-1):
#         y = the_path[u][0]*zoom + int(zoom/2)
#         x = the_path[u][1]*zoom + int(zoom/2)
#         y1 = the_path[u+1][0]*zoom + int(zoom/2)
#         x1 = the_path[u+1][1]*zoom + int(zoom/2)
#         draw.line((x,y,x1,y1), fill=(255, 0,0), width=5)
#     draw.rectangle((0, 0, zoom * len(filledMaze[0]), zoom * len(filledMaze)), outline=(0,255,0), width=2)
#     images.append(im)
#
# newMaze = np.zeros(shape=(tile_height + 2, tile_width + 2))
# newMaze[start[0], start[1]] = 1
#
# for i in range(10):
#     if i % 2 == 0:
#         draw_matrix(arr, newMaze, best_path)
#     else:
#         draw_matrix(arr, newMaze)
#
# images[0].save('images/maze.gif',
#                save_all=True, append_images=images[1:],
#                optimize=False, duration=3, loop=0)