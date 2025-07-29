import pruning

class SolutionState:
    def __init__(self, solved_state, moves, pruning_depth):
        self.solved_state = solved_state.copy()
        self.solved_points = []
        for i in range(54):
            if solved_state[i] != 'X':
                self.solved_points.append(i)
        self.moves = moves
        self.pruning_depth = pruning_depth
        self.one_solution = True
        if (len(solved_state[i]) > 1):
            self.one_solution = False
        if self.one_solution:
            self.pruning_table = pruning.gen_pruning_table([solved_state], self.pruning_depth, self.moves)
        else:
            self.pruning_table = pruning.gen_pruning_table(solved_state, self.pruning_depth, self.moves)

    def is_solved(self, cube):
        if (self.pruning_table.get(''.join(cube)) == 0):
            return True
        else:
            return False