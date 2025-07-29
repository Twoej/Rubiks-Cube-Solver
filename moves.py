import numpy as np

def squarei(face, index):
    face_to_num = {'U': 0, 'R': 1, 'F': 2, 'D': 3, 'L': 4, 'B': 5}
    square = (face_to_num[face] * 9) + index
    return square

def perm_from_cycle(cycle):
    num_perm = len(cycle)
    perms = np.zeros((num_perm, 2), int)
    for i in range(num_perm):
        nexti = i + 1
        if nexti == num_perm:
            nexti = 0
        perms[i] = [cycle[i], cycle[nexti]]
    return perms

u_move = np.reshape([
    perm_from_cycle([squarei('U', 0), squarei('U', 2), squarei('U', 8), squarei('U', 6)]),
    perm_from_cycle([squarei('U', 1), squarei('U', 5), squarei('U', 7), squarei('U', 3)]),
    perm_from_cycle([squarei('F', 0), squarei('L', 0), squarei('B', 0), squarei('R', 0)]),
    perm_from_cycle([squarei('F', 1), squarei('L', 1), squarei('B', 1), squarei('R', 1)]),
    perm_from_cycle([squarei('F', 2), squarei('L', 2), squarei('B', 2), squarei('R', 2)])
], (20, 2))

u_p_move = np.reshape([
    perm_from_cycle([squarei('U', 6), squarei('U', 8), squarei('U', 2), squarei('U', 0)]),
    perm_from_cycle([squarei('U', 3), squarei('U', 7), squarei('U', 5), squarei('U', 1)]),
    perm_from_cycle([squarei('R', 0), squarei('B', 0), squarei('L', 0), squarei('F', 0)]),
    perm_from_cycle([squarei('R', 1), squarei('B', 1), squarei('L', 1), squarei('F', 1)]),
    perm_from_cycle([squarei('R', 2), squarei('B', 2), squarei('L', 2), squarei('F', 2)])
], (20, 2))

l_move = np.reshape([
    perm_from_cycle([squarei('L', 0), squarei('L', 2), squarei('L', 8), squarei('L', 6)]),
    perm_from_cycle([squarei('L', 1), squarei('L', 5), squarei('L', 7), squarei('L', 3)]),
    perm_from_cycle([squarei('U', 0), squarei('F', 0), squarei('D', 0), squarei('B', 8)]),
    perm_from_cycle([squarei('U', 3), squarei('F', 3), squarei('D', 3), squarei('B', 5)]),
    perm_from_cycle([squarei('U', 6), squarei('F', 6), squarei('D', 6), squarei('B', 2)])
], (20, 2))

l_p_move = np.reshape([
    perm_from_cycle([squarei('L', 6), squarei('L', 8), squarei('L', 2), squarei('L', 0)]),
    perm_from_cycle([squarei('L', 3), squarei('L', 7), squarei('L', 5), squarei('L', 1)]),
    perm_from_cycle([squarei('B', 8), squarei('D', 0), squarei('F', 0), squarei('U', 0)]),
    perm_from_cycle([squarei('B', 5), squarei('D', 3), squarei('F', 3), squarei('U', 3)]),
    perm_from_cycle([squarei('B', 2), squarei('D', 6), squarei('F', 6), squarei('U', 6)])
], (20, 2))

f_move = np.reshape([
    perm_from_cycle([squarei('F', 0), squarei('F', 2), squarei('F', 8), squarei('F', 6)]),
    perm_from_cycle([squarei('F', 1), squarei('F', 5), squarei('F', 7), squarei('F', 3)]),
    perm_from_cycle([squarei('U', 6), squarei('R', 0), squarei('D', 2), squarei('L', 8)]),
    perm_from_cycle([squarei('U', 7), squarei('R', 3), squarei('D', 1), squarei('L', 5)]),
    perm_from_cycle([squarei('U', 8), squarei('R', 6), squarei('D', 0), squarei('L', 2)])
], (20, 2))

f_p_move = np.reshape([
    perm_from_cycle([squarei('F', 6), squarei('F', 8), squarei('F', 2), squarei('F', 0)]),
    perm_from_cycle([squarei('F', 3), squarei('F', 7), squarei('F', 5), squarei('F', 1)]),
    perm_from_cycle([squarei('L', 8), squarei('D', 2), squarei('R', 0), squarei('U', 6)]),
    perm_from_cycle([squarei('L', 5), squarei('D', 1), squarei('R', 3), squarei('U', 7)]),
    perm_from_cycle([squarei('L', 2), squarei('D', 0), squarei('R', 6), squarei('U', 8)])
], (20, 2))

r_move = np.reshape([
    perm_from_cycle([squarei('R', 0), squarei('R', 2), squarei('R', 8), squarei('R', 6)]),
    perm_from_cycle([squarei('R', 1), squarei('R', 5), squarei('R', 7), squarei('R', 3)]),
    perm_from_cycle([squarei('U', 8), squarei('B', 0), squarei('D', 8), squarei('F', 8)]),
    perm_from_cycle([squarei('U', 5), squarei('B', 3), squarei('D', 5), squarei('F', 5)]),
    perm_from_cycle([squarei('U', 2), squarei('B', 6), squarei('D', 2), squarei('F', 2)])
], (20, 2))

r_p_move = np.reshape([
    perm_from_cycle([squarei('R', 6), squarei('R', 8), squarei('R', 2), squarei('R', 0)]),
    perm_from_cycle([squarei('R', 3), squarei('R', 7), squarei('R', 5), squarei('R', 1)]),
    perm_from_cycle([squarei('F', 8), squarei('D', 8), squarei('B', 0), squarei('U', 8)]),
    perm_from_cycle([squarei('F', 5), squarei('D', 5), squarei('B', 3), squarei('U', 5)]),
    perm_from_cycle([squarei('F', 2), squarei('D', 2), squarei('B', 6), squarei('U', 2)])
], (20, 2))

d_move = np.reshape([
    perm_from_cycle([squarei('D', 0), squarei('D', 2), squarei('D', 8), squarei('D', 6)]),
    perm_from_cycle([squarei('D', 1), squarei('D', 5), squarei('D', 7), squarei('D', 3)]),
    perm_from_cycle([squarei('F', 6), squarei('R', 6), squarei('B', 6), squarei('L', 6)]),
    perm_from_cycle([squarei('F', 7), squarei('R', 7), squarei('B', 7), squarei('L', 7)]),
    perm_from_cycle([squarei('F', 8), squarei('R', 8), squarei('B', 8), squarei('L', 8)])
], (20, 2))

d_p_move = np.reshape([
    perm_from_cycle([squarei('D', 6), squarei('D', 8), squarei('D', 2), squarei('D', 0)]),
    perm_from_cycle([squarei('D', 3), squarei('D', 7), squarei('D', 5), squarei('D', 1)]),
    perm_from_cycle([squarei('L', 6), squarei('B', 6), squarei('R', 6), squarei('F', 6)]),
    perm_from_cycle([squarei('L', 7), squarei('B', 7), squarei('R', 7), squarei('F', 7)]),
    perm_from_cycle([squarei('L', 8), squarei('B', 8), squarei('R', 8), squarei('F', 8)])
], (20, 2))

b_move = np.reshape([
    perm_from_cycle([squarei('B', 0), squarei('B', 2), squarei('B', 8), squarei('B', 6)]),
    perm_from_cycle([squarei('B', 1), squarei('B', 5), squarei('B', 7), squarei('B', 3)]),
    perm_from_cycle([squarei('U', 2), squarei('L', 0), squarei('D', 6), squarei('R', 8)]),
    perm_from_cycle([squarei('U', 1), squarei('L', 3), squarei('D', 7), squarei('R', 5)]),
    perm_from_cycle([squarei('U', 0), squarei('L', 6), squarei('D', 8), squarei('R', 2)])
], (20, 2))

b_p_move = np.reshape([
    perm_from_cycle([squarei('B', 6), squarei('B', 8), squarei('B', 2), squarei('B', 0)]),
    perm_from_cycle([squarei('B', 3), squarei('B', 7), squarei('B', 5), squarei('B', 1)]),
    perm_from_cycle([squarei('R', 8), squarei('D', 6), squarei('L', 0), squarei('U', 2)]),
    perm_from_cycle([squarei('R', 5), squarei('D', 7), squarei('L', 3), squarei('U', 1)]),
    perm_from_cycle([squarei('R', 2), squarei('D', 8), squarei('L', 6), squarei('U', 0)])
], (20, 2))

u_2_move = np.reshape([
    perm_from_cycle([squarei('U', 0), squarei('U', 8)]),
    perm_from_cycle([squarei('U', 2), squarei('U', 6)]),
    perm_from_cycle([squarei('U', 1), squarei('U', 7)]),
    perm_from_cycle([squarei('U', 5), squarei('U', 3)]),
    perm_from_cycle([squarei('F', 0), squarei('B', 0)]),
    perm_from_cycle([squarei('F', 1), squarei('B', 1)]),
    perm_from_cycle([squarei('F', 2), squarei('B', 2)]),
    perm_from_cycle([squarei('L', 0), squarei('R', 0)]),
    perm_from_cycle([squarei('L', 1), squarei('R', 1)]),
    perm_from_cycle([squarei('L', 2), squarei('R', 2)]),
], (20, 2))

l_2_move = np.reshape([
    perm_from_cycle([squarei('L', 0), squarei('L', 8)]),
    perm_from_cycle([squarei('L', 2), squarei('L', 6)]),
    perm_from_cycle([squarei('L', 1), squarei('L', 7)]),
    perm_from_cycle([squarei('L', 5), squarei('L', 3)]),
    perm_from_cycle([squarei('F', 0), squarei('B', 8)]),
    perm_from_cycle([squarei('F', 3), squarei('B', 5)]),
    perm_from_cycle([squarei('F', 6), squarei('B', 2)]),
    perm_from_cycle([squarei('D', 0), squarei('U', 0)]),
    perm_from_cycle([squarei('D', 3), squarei('U', 3)]),
    perm_from_cycle([squarei('D', 6), squarei('U', 6)]),
], (20, 2))

f_2_move = np.reshape([
    perm_from_cycle([squarei('F', 0), squarei('F', 8)]),
    perm_from_cycle([squarei('F', 2), squarei('F', 6)]),
    perm_from_cycle([squarei('F', 1), squarei('F', 7)]),
    perm_from_cycle([squarei('F', 5), squarei('F', 3)]),
    perm_from_cycle([squarei('L', 2), squarei('R', 6)]),
    perm_from_cycle([squarei('L', 5), squarei('R', 3)]),
    perm_from_cycle([squarei('L', 8), squarei('R', 0)]),
    perm_from_cycle([squarei('D', 0), squarei('U', 8)]),
    perm_from_cycle([squarei('D', 1), squarei('U', 7)]),
    perm_from_cycle([squarei('D', 2), squarei('U', 6)]),
], (20, 2))

r_2_move = np.reshape([
    perm_from_cycle([squarei('R', 0), squarei('R', 8)]),
    perm_from_cycle([squarei('R', 2), squarei('R', 6)]),
    perm_from_cycle([squarei('R', 1), squarei('R', 7)]),
    perm_from_cycle([squarei('R', 5), squarei('R', 3)]),
    perm_from_cycle([squarei('F', 2), squarei('B', 6)]),
    perm_from_cycle([squarei('F', 5), squarei('B', 3)]),
    perm_from_cycle([squarei('F', 8), squarei('B', 0)]),
    perm_from_cycle([squarei('D', 2), squarei('U', 2)]),
    perm_from_cycle([squarei('D', 5), squarei('U', 5)]),
    perm_from_cycle([squarei('D', 8), squarei('U', 8)]),
], (20, 2))

d_2_move = np.reshape([
    perm_from_cycle([squarei('D', 0), squarei('D', 8)]),
    perm_from_cycle([squarei('D', 2), squarei('D', 6)]),
    perm_from_cycle([squarei('D', 1), squarei('D', 7)]),
    perm_from_cycle([squarei('D', 5), squarei('D', 3)]),
    perm_from_cycle([squarei('F', 6), squarei('B', 6)]),
    perm_from_cycle([squarei('F', 7), squarei('B', 7)]),
    perm_from_cycle([squarei('F', 8), squarei('B', 8)]),
    perm_from_cycle([squarei('L', 6), squarei('R', 6)]),
    perm_from_cycle([squarei('L', 7), squarei('R', 7)]),
    perm_from_cycle([squarei('L', 8), squarei('R', 8)]),
], (20, 2))

b_2_move = np.reshape([
    perm_from_cycle([squarei('B', 0), squarei('B', 8)]),
    perm_from_cycle([squarei('B', 2), squarei('B', 6)]),
    perm_from_cycle([squarei('B', 1), squarei('B', 7)]),
    perm_from_cycle([squarei('B', 5), squarei('B', 3)]),
    perm_from_cycle([squarei('U', 2), squarei('D', 6)]),
    perm_from_cycle([squarei('U', 1), squarei('D', 7)]),
    perm_from_cycle([squarei('U', 0), squarei('D', 8)]),
    perm_from_cycle([squarei('R', 2), squarei('L', 6)]),
    perm_from_cycle([squarei('R', 5), squarei('L', 3)]),
    perm_from_cycle([squarei('R', 8), squarei('L', 0)]),
], (20, 2))

all_moves = {"U": u_move, "U'": u_p_move, "L": l_move, "L'": l_p_move, "F": f_move, "F'": f_p_move, "R": r_move, "R'": r_p_move, "D": d_move, "D'": d_p_move,
             "B": b_move, "B'": b_p_move, "U2": u_2_move, "L2": l_2_move, "F2": f_2_move, "R2": r_2_move, "D2": d_2_move, "B2": b_2_move}
