import pruning
import renderedcube
from graphics import *
from moves import squarei

error_cube_str = "UUUUUUUUURRRRRRRRRFFFFFFFFFLDDDDDDDDLLLLLLRLLBBBBBBBBB"
#error_cube_str = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
error_cube = list(error_cube_str)

error_correcting_moves = {
    str([squarei('U', 6), squarei('F', 0), squarei('L', 2)]): "F2",
    str([squarei('U', 8), squarei('F', 2), squarei('R', 0)]): "F",
    str([squarei('U', 0), squarei('B', 2), squarei('L', 0)]): "U U R'",
    str([squarei('U', 2), squarei('B', 0), squarei('R', 2)]): "U R'",
    str([squarei('D', 0), squarei('F', 6), squarei('L', 8)]): "D",
    str([squarei('D', 2), squarei('F', 8), squarei('R', 6)]): "",
    str([squarei('D', 6), squarei('B', 8), squarei('L', 6)]): "D2",
    str([squarei('D', 8), squarei('B', 6), squarei('R', 8)]): "D'",
    str([squarei('U', 7), squarei('F', 1)]): "F",
    str([squarei('U', 1), squarei('B', 1)]): "U R'",
    str([squarei('U', 3), squarei('L', 1)]): "U' F",
    str([squarei('U', 5), squarei('R', 1)]): "R'",
    str([squarei('D', 1), squarei('F', 7)]): "F'",
    str([squarei('D', 7), squarei('B', 7)]): "D' R",
    str([squarei('D', 3), squarei('L', 7)]): "D F'",
    str([squarei('D', 5), squarei('R', 7)]): "R",
    str([squarei('F', 3), squarei('L', 5)]): "F2",
    str([squarei('F', 5), squarei('R', 3)]): "",
    str([squarei('B', 5), squarei('L', 3)]): "L' D F'",
    str([squarei('B', 3), squarei('R', 5)]): "R2"
    }
error_move_casting = {
    str([squarei('U', 6), squarei('F', 0), squarei('L', 2)]): [squarei('F', 0), squarei('L', 2), squarei('U', 6)],
    str([squarei('U', 8), squarei('F', 2), squarei('R', 0)]): [squarei('F', 2), squarei('U', 8), squarei('R', 0)],
    str([squarei('U', 0), squarei('B', 2), squarei('L', 0)]): [squarei('U', 0), squarei('L', 0), squarei('B', 2)],
    str([squarei('U', 2), squarei('B', 0), squarei('R', 2)]): [squarei('U', 2), squarei('B', 0), squarei('R', 2)],
    str([squarei('D', 0), squarei('F', 6), squarei('L', 8)]): [squarei('L', 8), squarei('F', 6), squarei('D', 0)],
    str([squarei('D', 2), squarei('F', 8), squarei('R', 6)]): [],
    str([squarei('D', 6), squarei('B', 8), squarei('L', 6)]): [squarei('B', 8), squarei('L', 6), squarei('D', 6),],
    str([squarei('D', 8), squarei('B', 6), squarei('R', 8)]): [squarei('R', 8), squarei('B', 6), squarei('D', 8)],
    str([squarei('U', 7), squarei('F', 1)]): [squarei('F', 1), squarei('U', 7)],
    str([squarei('U', 1), squarei('B', 1)]): [squarei('U', 1), squarei('B', 1)],
    str([squarei('U', 3), squarei('L', 1)]): [squarei('L', 1), squarei('U', 3)],
    str([squarei('U', 5), squarei('R', 1)]): [squarei('U', 5), squarei('R', 1)],
    str([squarei('D', 1), squarei('F', 7)]): [squarei('F', 7), squarei('D', 1)],
    str([squarei('D', 7), squarei('B', 7)]): [squarei('D', 7), squarei('B', 7)],
    str([squarei('D', 3), squarei('L', 7)]): [squarei('D', 3), squarei('L', 7)],
    str([squarei('D', 5), squarei('R', 7)]): [squarei('D', 5), squarei('R', 7)],
    str([squarei('F', 3), squarei('L', 5)]): [squarei('F', 3), squarei('L', 5)],
    str([squarei('F', 5), squarei('R', 3)]): [],
    str([squarei('B', 5), squarei('L', 3)]): [squarei('L', 3), squarei('B', 5)],
    str([squarei('B', 3), squarei('R', 5)]): [squarei('B', 3), squarei('R', 5)]
    }


def sort_piece_str(piece_str):
    sorted_str_list = list(piece_str)
    n = len(sorted_str_list)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if (pruning.letter_order[sorted_str_list[j]] > pruning.letter_order[sorted_str_list[j + 1]]):
                sorted_str_list[j], sorted_str_list[j + 1] = sorted_str_list[j + 1], sorted_str_list[j]
                swapped = True
        if (not swapped):
            break
    sorted_str = ""
    for i in range(n):
        sorted_str += sorted_str_list[i]
    return sorted_str

def detect_errors(cube):
    errors = []
    checked = {}
    for piece in pruning.pieces:
        piece_str = ""
        for i in range(len(piece)):
            piece_str += cube[piece[i]]
        piece_str = sort_piece_str(piece_str)
        if piece_str not in pruning.faces_to_piece.keys():
            errors.append(piece)
        if piece_str in checked.keys():
            errors.append(piece)
            errors.append(checked[piece_str])
        else:
            checked[piece_str] = piece
    return errors

error_list = detect_errors(error_cube)


for i in range(len(error_list)):
    for j in range(len(error_list[i])):
        error_cube[error_list[i][j]] = 'X'

print(error_list)

win = GraphWin("Rubik's Cube", 900, 600)
renderedcube.draw_cube(error_cube, win)
win.getMouse()