from graphics import *

side = 40

colour = {
    'U': "white",
    'D': "yellow",
    'L': "orange",
    'R': "red",
    'F': "green",
    'B': "blue",
    'X': "gray",
    'O': "tan",
    'A': "purple",
    'C': "magenta"
}


def draw_cube(cube, win):
    startx = 25
    starty = 160
    edge = 3 * side
    draw_face(Point(startx, starty), cube, 4, win)
    draw_face(Point((startx + edge), starty), cube, 2, win)
    draw_face(Point((startx + (2 * edge)), starty), cube, 1, win)
    draw_face(Point((startx + (3 * edge)), starty), cube, 5, win)
    draw_face(Point((startx + edge), (starty - edge)), cube, 0, win)
    draw_face(Point((startx + edge), (starty + edge)), cube, 3, win)

def draw_face(corner, cube, face, win):
    for i in range(3):
        for j in range(3):
            square_corner = Point(corner.x + (i * side), corner.y + (j * side))
            square_index = (face * 9) + i + (j * 3)
            draw_square(square_corner, cube, square_index, win)

def draw_square(corner, cube, index, win):
    sq = Rectangle(corner, Point(corner.x + side, corner.y + side))
    sq.setFill(colour[cube[index]])
    sq.draw(win)

