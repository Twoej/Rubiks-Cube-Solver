import renderedcube
import moves as mv
import numpy as np
import time
from solutionstate import *
from graphics import *

solved_cube_str = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
#solved_cube_str = "URFDLBURFRRRRRRRRRFFFFFFFFFDDDDDDDDDBBLRFDLRUBBBBBBBBB"
solved_cube = list(solved_cube_str)


solved_case_str = "XXXXXXXXXXXXXXXXXXXXXFXXFXXDXXDXXDXXXXXLLLLLLXXXXXBXXB"
solved_case = list(solved_case_str)

solved_points = [39, 40, 41, 42, 43, 44, 21, 24, 50, 53, 27, 30, 33]
all_points = np.zeros(54)
for i in range(54):
    all_points[i] = i
moves_list = ["U2", "L2", "F2", "R2", "D2", "B2",  "U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]

times_run = 0


def apply_move(cube, move):
    new_cube = cube.copy()
    for i in range(len(move)):
        new_cube[move[i][1]] = cube[move[i][0]]
    return new_cube

def apply_moves(cube, moves):
    new_cube = cube.copy()
    for i in range(len(moves)):
        if (i + 1) >= len(moves):
            move_postfix = ""
        else:
            move_postfix = moves[i + 1]
        if moves[i] != ' ' and moves[i] != "'" and moves[i] != "2":
            new_cube = apply_move(new_cube, mv.all_moves[(moves[i] + move_postfix).strip()])
    return new_cube

def solve_dfs(cube, solution, solution_check, depth_remaining):
    global times_run
    times_run += 1
    if solution_check.is_solved(cube):
        return solution
    arguement = ''.join(cube)
    lower_bound = solution_check.pruning_table.get(arguement)
    if lower_bound == None:
        lower_bound = solution_check.pruning_depth + 1
    if lower_bound > depth_remaining:
        return None
    if (depth_remaining == 0):
        return None
    for move in solution_check.moves:
        result = solve_dfs(apply_move(cube, mv.all_moves[move]), solution + ' ' + move, solution_check, depth_remaining - 1)
        if result != None:
            return result
    return None

def solve_iddfs(cube, depth_limit, solution_check):
    for depth in range(depth_limit):
        solution = solve_dfs(cube, "", solution_check, depth)
        if solution != None:
            return solution
    return None


#Stages
g1_solved_points = [mv.squarei('U', 1), mv.squarei('U', 3), mv.squarei('U', 5), mv.squarei('U', 7), mv.squarei('D', 1), mv.squarei('D', 3),
                    mv.squarei('D', 5), mv.squarei('D', 7), mv.squarei('F', 3), mv.squarei('F', 5), mv.squarei('B', 3), mv.squarei('B', 5)]
g1_solved_case_str = "XOXOXOXOXXXXXXXXXXXXXOXOXXXXOXOXOXOXXXXXXXXXXXXXOXOXXX"
g1_solved_case = list(g1_solved_case_str)
g0_moves_list = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'", "U2", "L2", "F2", "R2", "D2", "B2"]
g1_state = SolutionState(g1_solved_case, g0_moves_list, 7)

g2_solved_points = [mv.squarei('U', 1), mv.squarei('U', 3), mv.squarei('U', 5), mv.squarei('U', 7), mv.squarei('D', 1), mv.squarei('D', 3),
                    mv.squarei('D', 5), mv.squarei('D', 7), mv.squarei('F', 3), mv.squarei('F', 5), mv.squarei('B', 3), mv.squarei('B', 5),
                    mv.squarei('U', 0), mv.squarei('U', 2), mv.squarei('U', 6), mv.squarei('U', 8), mv.squarei('D', 0), mv.squarei('D', 2),
                    mv.squarei('D', 6), mv.squarei('D', 8)]
g2_solved_case_str = "AAAAXAAAAXXXXXXXXXXXXCXCXXXAAAAXAAAAXXXXXXXXXXXXCXCXXX"
g2_solved_case = list(g2_solved_case_str)
g1_moves_list = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "U2", "L2", "F2", "R2", "D2", "B2"]
g2_state = SolutionState(g2_solved_case, g1_moves_list, 5)

g3_solved_points = [0, 2, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 29,
                     33, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53]
g3_ce_solved_case_str = "UXUXXXUXURRRRXRRRRFFFFXFFFFDXDXXXDXDLRLRXRLRLBFBFXFBFB"
g3_ce_solved_case = list(g3_ce_solved_case_str)
g3_ce_move_list = ["U2", "D2", "F2", "B2", "L2", "R2"]
g3_solved_cases = list(pruning.gen_pruning_table([g3_ce_solved_case], 10, g3_ce_move_list).keys())
g2_moves_list = ["U", "U'", "D", "D'", "U2", "L2", "F2", "R2", "D2", "B2"]
g3_state = SolutionState(g3_solved_cases, g2_moves_list, 5)

g4_solved_points = all_points
g4_solved_case = solved_cube
g3_moves_list = ["U2", "L2", "F2", "R2", "D2", "B2"]
g4_state = SolutionState(g4_solved_case, g3_moves_list, 6)


win = GraphWin("Rubik's Cube", 900, 600)

#TESTING
#for i in range(96):
#    renderedcube.draw_cube(g3_solved_cases[i], win)
#    print(str(g3_solved_cases[i]))
#    win.getMouse()

renderedcube.draw_cube(g1_solved_case, win)
win.getMouse()
current_cube = apply_moves(solved_cube, "F' D2 R U' L' U' F' L U' B' U L' F L' B D' R D2 R' D R2 U' F L R D' L F U R2")
current_cube_str = "LBLDUFRDUBLDURBFBFBLRRFLUDRFFUDDLLUDDBDRLFURLFUBRBURFB"
current_cube = list(current_cube_str)
renderedcube.draw_cube(current_cube, win)
current_cube_masked = pruning.g1_mask(pruning.fcube_to_ifcube(current_cube), g1_solved_points)
win.getMouse()

renderedcube.draw_cube(current_cube_masked, win)

win.getMouse()
start_time = time.time()
solution_current = solve_iddfs(current_cube_masked, 20, g1_state)
end_time = time.time()
time_elapsed = end_time - start_time
print(time_elapsed)
print(times_run)
print(solution_current)
if solution_current != None:
    current_cube = apply_moves(current_cube, solution_current)
renderedcube.draw_cube(current_cube, win)
current_cube_masked = pruning.g2_mask(pruning.fcube_to_ifcube(current_cube), g2_solved_points)
win.getMouse()
renderedcube.draw_cube(g2_solved_case, win)
win.getMouse()
renderedcube.draw_cube(current_cube_masked, win)
win.getMouse()
solution_current = solve_iddfs(current_cube_masked, 20, g2_state)
print(solution_current)
if solution_current != None:
    current_cube = apply_moves(current_cube, solution_current)
renderedcube.draw_cube(current_cube, win)
current_cube_masked = pruning.g3_mask(pruning.fcube_to_ifcube(current_cube), g3_solved_points)
win.getMouse()
renderedcube.draw_cube(g3_solved_cases[0], win)
win.getMouse()
renderedcube.draw_cube(current_cube_masked, win)
win.getMouse()
solution_current = solve_iddfs(current_cube_masked, 20, g3_state)
print(solution_current)
if solution_current != None:
    current_cube = apply_moves(current_cube, solution_current)
renderedcube.draw_cube(current_cube, win)
win.getMouse()
solution_current = solve_iddfs(current_cube, 20, g4_state)
print(solution_current)
if solution_current != None:
    current_cube = apply_moves(current_cube, solution_current)
renderedcube.draw_cube(current_cube, win)
win.getMouse()

win.close()
