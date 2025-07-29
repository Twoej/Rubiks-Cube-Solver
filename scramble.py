from random import *
import time
from moves import all_moves

def gen_scramble():
	moves_output = ""
	moves = list(all_moves.keys())
	seed(time.time())
	length = int(random() * 10) + 15
	for i in range(length):
		index = int(random() * 18)
		if (index > (len(moves) - 1)):
			index = len(moves) - 1
		moves_output += moves[index]
		moves_output += " "
	return moves_output.rstrip()

