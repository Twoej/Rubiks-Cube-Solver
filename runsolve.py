import PictureTaker
import time
import gpiod
from graphics import *
import cv2

win = GraphWin("Rubik's Cube", 900, 600)




solve_pin = 17
chip = gpiod.Chip('gpiochip4')
solve_line = chip.get_line(solve_pin)
solve_line.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN, flags = 32)

while True:
	debounce = 0
	pressed = False
	for i in range(100):
		if (solve_line.get_value() == 0):
			debounce += 1
	if (debounce > 50):
		pressed = True
	if (pressed):
		press_before = time.time()
		while (solve_line.get_value() == 0):
			time.sleep(0.1)
		pressed_time = time.time() - press_before
		if (pressed_time > 3):
			PictureTaker.scramble_cube(win)
		else:
			PictureTaker.read_and_solve(win)
	time.sleep(0.01)
