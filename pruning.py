import numpy as np
import moves as mv

solved_points = [39, 40, 41, 42, 43, 44, 21, 24, 50, 53, 27, 30, 33]
moves_list = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]
solved_ifcube = np.zeros(54)
for i in range(54):
    solved_ifcube[i] = i
corners = [0, 2, 6, 8, 9, 11, 15, 17, 18, 20, 24, 26, 27, 29, 33, 35, 36, 38, 42, 44, 45, 47, 51, 53]

faces_to_piece = {
    "UFL" : [mv.squarei('U', 6), mv.squarei('F', 0), mv.squarei('L', 2)],
    "UFR" : [mv.squarei('U', 8), mv.squarei('F', 2), mv.squarei('R', 0)],
    "UBL" : [mv.squarei('U', 0), mv.squarei('B', 2), mv.squarei('L', 0)],
    "UBR" : [mv.squarei('U', 2), mv.squarei('B', 0), mv.squarei('R', 2)],
    "DFL" : [mv.squarei('D', 0), mv.squarei('F', 6), mv.squarei('L', 8)],
    "DFR" : [mv.squarei('D', 2), mv.squarei('F', 8), mv.squarei('R', 6)],
    "DBL" : [mv.squarei('D', 6), mv.squarei('B', 8), mv.squarei('L', 6)],
    "DBR" : [mv.squarei('D', 8), mv.squarei('B', 6), mv.squarei('R', 8)],
    "UF" : [mv.squarei('U', 7), mv.squarei('F', 1)],
    "UB" : [mv.squarei('U', 1), mv.squarei('B', 1)],
    "UL" : [mv.squarei('U', 3), mv.squarei('L', 1)],
    "UR" : [mv.squarei('U', 5), mv.squarei('R', 1)],
    "DF" : [mv.squarei('D', 1), mv.squarei('F', 7)],
    "DB" : [mv.squarei('D', 7), mv.squarei('B', 7)],
    "DL" : [mv.squarei('D', 3), mv.squarei('L', 7)],
    "DR" : [mv.squarei('D', 5), mv.squarei('R', 7)],
    "FL" : [mv.squarei('F', 3), mv.squarei('L', 5)],
    "FR" : [mv.squarei('F', 5), mv.squarei('R', 3)],
    "BL" : [mv.squarei('B', 5), mv.squarei('L', 3)],
    "BR" : [mv.squarei('B', 3), mv.squarei('R', 5)]
}

pieces = [
    [mv.squarei('U', 6), mv.squarei('F', 0), mv.squarei('L', 2)],
    [mv.squarei('U', 8), mv.squarei('F', 2), mv.squarei('R', 0)],
    [mv.squarei('U', 0), mv.squarei('B', 2), mv.squarei('L', 0)],
    [mv.squarei('U', 2), mv.squarei('B', 0), mv.squarei('R', 2)],
    [mv.squarei('D', 0), mv.squarei('F', 6), mv.squarei('L', 8)],
    [mv.squarei('D', 2), mv.squarei('F', 8), mv.squarei('R', 6)],
    [mv.squarei('D', 6), mv.squarei('B', 8), mv.squarei('L', 6)],
    [mv.squarei('D', 8), mv.squarei('B', 6), mv.squarei('R', 8)],
    [mv.squarei('U', 7), mv.squarei('F', 1)],
    [mv.squarei('U', 1), mv.squarei('B', 1)],
    [mv.squarei('U', 3), mv.squarei('L', 1)],
    [mv.squarei('U', 5), mv.squarei('R', 1)],
    [mv.squarei('D', 1), mv.squarei('F', 7)],
    [mv.squarei('D', 7), mv.squarei('B', 7)],
    [mv.squarei('D', 3), mv.squarei('L', 7)],
    [mv.squarei('D', 5), mv.squarei('R', 7)],
    [mv.squarei('F', 3), mv.squarei('L', 5)],
    [mv.squarei('F', 5), mv.squarei('R', 3)],
    [mv.squarei('B', 5), mv.squarei('L', 3)],
    [mv.squarei('B', 3), mv.squarei('R', 5)]
]

letter_order = {
    'U' : 0,
    'D' : 1,
    'F' : 2,
    'B' : 3,
    'L' : 4,
    'R' : 5
}

def fcube_to_ifcube(cube):
    ifcube = np.zeros(54)
    for i in range(4, 50, 9):
        ifcube[i] = i
    for piece in pieces:
        piece_str = ""
        for i in range(len(piece)):
            piece_str += cube[piece[i]]
        piece_str, sort_order = sort_piece_str(piece_str)
        casts = faces_to_piece[piece_str]
        for i in range(len(sort_order)):
            ifcube[piece[sort_order[i]]] = casts[i]
    return ifcube

def sort_piece_str(piece_str):
    sorted_str_list = list(piece_str)
    sort_order = []
    for i in range(len(sorted_str_list)):
        sort_order.append(i)
    n = len(sorted_str_list)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if (letter_order[sorted_str_list[j]] > letter_order[sorted_str_list[j + 1]]):
                sorted_str_list[j], sorted_str_list[j + 1] = sorted_str_list[j + 1], sorted_str_list[j]
                sort_order[j], sort_order[j + 1] = sort_order[j + 1], sort_order[j]
                swapped = True
        if (not swapped):
            break
    sorted_str = ""
    for i in range(n):
        sorted_str += sorted_str_list[i]
    return sorted_str, sort_order
    


def apply_move(cube, move):
    new_cube = cube.copy()
    for i in range(len(move)):
        new_cube[move[i][1]] = cube[move[i][0]]
    return new_cube

def ifcube_index_to_cube_face(idx):
    return "URFDLB"[int(idx/9)]

def mask_ifcube(ifcube, mask):
    fcube = ['X'] * 54
    for i in range(54):
        if ifcube[i] in mask:
            fcube[i] = ifcube_index_to_cube_face(ifcube[i])
    return fcube

def g1_mask(ifcube, mask):
    fcube = ['X'] * 54
    for i in range(54):
        if ifcube[i] in mask:
            fcube[i] = 'O'
    return fcube

def g2_mask(ifcube, mask):
    fcube = ['X'] * 54
    for i in range(54):
        if ifcube[i] in mask:
            face = ifcube_index_to_cube_face(ifcube[i])
            if (face == 'U' or face == 'D'):
                fcube[i] = 'A'
            else:
                fcube[i] = 'C'
    return fcube

def g3_mask(ifcube, mask):
    fcube = ['X'] * 54
    for i in range(54):
        if ifcube[i] in mask:
            face = ifcube_index_to_cube_face(ifcube[i])
            corner = False
            if ifcube[i] in corners:
                corner = True
            if (not corner):
                if (face == 'L' or face == 'R'):
                    fcube[i] = 'R'
                else:
                    fcube[i] = 'F'
            else:
                fcube[i] = ifcube_index_to_cube_face(ifcube[i])
    return fcube


def gen_pruning_table(solved_states, depth, moveset):
    pruning_table = {}
    previous_frontier = solved_states.copy()
    for i in range(len(solved_states)):
        pruning_table[''.join(solved_states[i])] = 0
    for i in range(1, depth + 1):
        frontier = []
        for state in previous_frontier:
            for move in moveset:
                new_state = ''.join(apply_move(list(state), mv.all_moves[move]))
                if (pruning_table.get(new_state) == None):
                    pruning_table[new_state] = i
                    frontier += [new_state]
        for i in range(len(frontier)):
            if (i >= len(previous_frontier)):
                previous_frontier += [frontier[i]]
            else:
                previous_frontier[i] = frontier[i]
    print(len(pruning_table))
    return pruning_table
