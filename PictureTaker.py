import time, libcamera
from picamera2 import Picamera2, Preview
import numpy as np
import cv2
from moves import squarei
from graphics import *
import renderedcube
from pruning import ifcube_index_to_cube_face
import serial as ser
import errordetection
import solver
from scramble import gen_scramble



picam_low = Picamera2(1)
picam_high = Picamera2(0)

ard = ser.Serial('/dev/ttyUSB0', 9600, timeout = None)
time.sleep(2)
ard.reset_input_buffer()

config = picam_low.create_preview_configuration(main={"size": (2592, 1944)})
picam_low.configure(config)
config = picam_high.create_preview_configuration(main={"size": (2592, 1944)})
picam_high.configure(config)

picam_high.start()
picam_low.start()

delay = 0.4


def take_picture(camera):
	global picam_high
	global picam_low
	if (camera == picam_low):
		picam_low.capture_file("low_img.jpg")
		low_cam = cv2.imread('low_img.jpg', -1)
		return low_cam
	elif (camera == picam_high):
		picam_high.capture_file("high_img.jpg")
		high_cam = cv2.imread('high_img.jpg', -1)
		return high_cam

def wait_for_ard(end_con):
	while (True):
		if (ard.in_waiting > 0):
			ardSer = ard.readline().decode('utf-8').rstrip()
			if (ardSer == end_con):
				break

			
def ard_write_move(move):
	moves_conversion = {"U": 'U', "U'": 'u', "U2": 'U', "D": 'D', "D'": 'd', "D2": 'D', "L": 'L', "L'": 'l', "L2": 'L', "R": 'R', "R'": 'r', "R2": 'R',
		"F": 'F', "F'": 'f', "F2": 'F', "B": 'B', "B'": 'b', "B2": 'B'}
	ard.write((str(moves_conversion[move]) + "\n").encode('utf-8'))
	if (len(move) > 1):
		if (list(move)[1] == '2'):
			wait_for_ard("next")
			ard.write((str(moves_conversion[move]) + "\n").encode('utf-8'))
	
def ard_write_moves(moves):
	ard.write(b"moves")
	wait_for_ard("ready")
	listed_moves = moves.split()
	for move in listed_moves:
		ard_write_move(move)
		wait_for_ard("next")
	ard.write(b"stop")
	wait_for_ard("done")
		
def fix_errors(cube, error_list, prev_error_list, camera, win):
	for error in error_list:
		piece_type = 0
		if (len(error) < 3):
			piece_type = 1
		if not (errordetection.error_correcting_moves[str(error)] == ""):
			ard_write_moves(errordetection.error_correcting_moves[str(error)])
		print(errordetection.error_correcting_moves[str(error)])
		if (len(prev_error_list) > 0):
			if (error_list[0] == prev_error_list[0]):
				ard_write_moves("R R' U U'")
				print("fixed")
		time.sleep(delay)
		image = take_picture(camera)
		for i, sticker in enumerate(error):
			cube[errordetection.error_move_casting[str(error)][i]] = get_colour(errordetection.error_fix_stickers[piece_type][i], image)
		renderedcube.draw_cube(cube, win)
		if not (errordetection.error_correcting_moves[str(error)] == ""):
			ard_write_moves(errordetection.reverse_moves(errordetection.error_correcting_moves[str(error)]))
		print(errordetection.reverse_moves(errordetection.error_correcting_moves[str(error)]))
	return cube


points_file = open("points.txt", "r")
points = points_file.read().rstrip()
points_file.close()
points_list = points.split()
pv = [int(x) for x in points_list]
stickers = {squarei('F', 7): np.reshape(pv[0:8], (4, 2)), squarei('F', 8): np.reshape(pv[8:16], (4, 2)),
	squarei('F', 5): np.reshape(pv[16:24], (4, 2)), squarei('F', 2): np.reshape(pv[24:32], (4, 2)),
	squarei('R', 7): np.reshape(pv[32:40], (4, 2)), squarei('R', 6): np.reshape(pv[40:48], (4, 2)),
	squarei('R', 3): np.reshape(pv[48:56], (4, 2)), squarei('R', 0): np.reshape(pv[56:64], (4, 2)),
	squarei('D', 1): np.reshape(pv[64:72], (4, 2)), squarei('D', 2): np.reshape(pv[72:80], (4, 2)),
	squarei('D', 5): np.reshape(pv[80:88], (4, 2)), squarei('U', 0): np.reshape(pv[88:96], (4, 2)),
	squarei('U', 3): np.reshape(pv[96:104], (4, 2)), squarei('L', 0): np.reshape(pv[104:112], (4, 2)),
	squarei('L', 1): np.reshape(pv[112:120], (4, 2)), squarei('L', 2): np.reshape(pv[120:128], (4, 2))}



colour_ranges = [[[200, 200, 200], [255, 255, 255]],		#White
				[[0, 170, 170], [60, 255, 255]],			#Yellow
				[[0, 45, 180], [30, 165, 255]],				#Orange
				[[0, 0, 160], [36, 36, 255]],				#Red
				[[0, 70, 0], [130, 255, 35]],				#Green
				[[90, 0, 0], [255, 34, 34]]]				#Blue
colours = [[0, 0, 255], [30, 255, 255], [19, 255, 255], [0, 255, 255], [60, 255, 255], [120, 255, 255]]
				
side_indicators = ['U', 'D', 'L', 'R', 'F', 'B']



def get_colour(sticker, image):
	height, width, _ = image.shape
	mask = np.zeros((height, width), dtype = np.uint8)
	mask = cv2.fillConvexPoly(mask, np.array(stickers[sticker]), color = (255, 255, 255))
	(mean, std) = cv2.meanStdDev(image, mask=mask)
	mean = mean.ravel()
	colour_int = 0
	for colour in colour_ranges:
		iscolour = True
		for i in range(3):
			if not (mean[i] >= colour[0][i] and mean[i] <= colour[1][i]):
				iscolour = False
		if iscolour:
			break
		else:
			colour_int += 1
	if colour_int > 5:
		mean = np.uint8([[[mean[0], mean[1], mean[2]]]])
		mean = cv2.cvtColor(mean, cv2.COLOR_BGR2HSV)
		mean = mean.ravel()
		closeness = 100000
		closest = 0
		colour_index = 0
		for colour in colours:
			temp_closeness = 0
			for i in range(3):
				temp_closeness += abs(colour[i] - mean[i])
			if (temp_closeness < closeness):
				closeness = temp_closeness
				closest = colour_index
			colour_index += 1
		colour_int = closest
	return side_indicators[colour_int]
	
def read_and_solve(win):
	global picam_low
	global picam_high
	
	ard.write(b"read")
	wait_for_ard("updated")
	
	ard_write_moves("U U' L L'")
	time.sleep(delay)
	
	img_low = take_picture(picam_low)
	img_high = take_picture(picam_high)

	highlighted_img = img_low.copy()
	for i, sticker in enumerate(stickers.values()):
		if (i > 10):
			break
		highlighted_img = cv2.fillConvexPoly(highlighted_img, np.array(sticker), color = (255, 255, 255))

	cv2.imshow('Image', highlighted_img)
	cv2.waitKey()
	cv2.destroyAllWindows()

	cube_state = ['X'] * 54
	for i in range(4, 50, 9):
		cube_state[i] = ifcube_index_to_cube_face(i)

	first_colour_check = [squarei('F', 7), squarei('F', 8), squarei('F', 5), squarei('F', 2), squarei('R', 7), squarei('R', 6), squarei('R', 3), squarei('R', 0),
		squarei('D', 1), squarei('D', 2), squarei('D', 5)]

	for sticker in first_colour_check:
		cube_state[sticker] = get_colour(sticker, img_low)
	renderedcube.draw_cube(cube_state, win)
		

	second_colour_check = [squarei('U', 0), squarei('U', 3), squarei('L', 0), squarei('L', 1), squarei('L', 2)]

	for sticker in second_colour_check:
		cube_state[sticker] = get_colour(sticker, img_high)
	renderedcube.draw_cube(cube_state, win)
		
		
	third_fifth_colour_check = [squarei('F', 8), squarei('D', 2), squarei('R', 6), squarei('R', 7), squarei('D', 5)]
	third_colour_indices = [squarei('R', 8), squarei('D', 8), squarei('B', 6), squarei('B', 7), squarei('D', 7)]
	fourth_colour_indices = [squarei('B', 8), squarei('D', 6), squarei('L', 6), squarei('L', 7), squarei('D', 3)]
	fifth_colour_indices = [squarei('L', 8), squarei('D', 0), squarei('F', 6), squarei('F', 7), squarei('D', 1)]

	sixth_seventh_colour_check = [squarei('L', 0), squarei('L', 1), squarei('U', 0), squarei('U', 3)]
	sixth_colour_indices = [squarei('F', 0), squarei('F', 1), squarei('U', 6), squarei('U', 7)]
	seventh_colour_indices = [squarei('R', 1), squarei('R', 2), squarei('U', 8), squarei('U', 5)]

	ard_write_moves("D' U L' L")
	time.sleep(delay)
	img_low = take_picture(picam_low)
	img_high = take_picture(picam_high)

	for i in range(5):
		cube_state[third_colour_indices[i]] = get_colour(third_fifth_colour_check[i], img_low)
	renderedcube.draw_cube(cube_state, win)

	for i in range(4):
		cube_state[sixth_colour_indices[i]] = get_colour(sixth_seventh_colour_check[i], img_high)
	renderedcube.draw_cube(cube_state, win)
		

	ard_write_moves("D' U L' L")
	time.sleep(delay)
	img_low = take_picture(picam_low)
	img_high = take_picture(picam_high)

	for i in range(5):
		cube_state[fourth_colour_indices[i]] = get_colour(third_fifth_colour_check[i], img_low)
	renderedcube.draw_cube(cube_state, win)

	sixth_seventh_colour_check = [squarei('L', 1), squarei('L', 2), squarei('U', 0), squarei('U', 3)]

	for i in range(4):
		cube_state[seventh_colour_indices[i]] = get_colour(sixth_seventh_colour_check[i], img_high)
	renderedcube.draw_cube(cube_state, win)
		

	ard_write_moves("D' U L' L")
	time.sleep(delay)
	img_low = take_picture(picam_low)
	img_high = take_picture(picam_high)

	for i in range(5):
		cube_state[fifth_colour_indices[i]] = get_colour(third_fifth_colour_check[i], img_low)
	renderedcube.draw_cube(cube_state, win)

	for i in range(3):
		cube_state[squarei('B', i)] = get_colour(squarei('L', i), img_high)
	renderedcube.draw_cube(cube_state, win)

	cube_state[squarei('U', 2)] = get_colour(squarei('U', 0), img_high)
	cube_state[squarei('U', 1)] = get_colour(squarei('U', 3), img_high)
	renderedcube.draw_cube(cube_state, win)
		

	ard_write_moves("D' U L D")
	time.sleep(delay)
	img_low = take_picture(picam_low)
	cube_state[squarei('L', 5)] = get_colour(squarei('F', 7), img_low)
	cube_state[squarei('F', 3)] = get_colour(squarei('D', 1), img_low)
	renderedcube.draw_cube(cube_state, win)

	ard_write_moves("D' L' R2")
	time.sleep(delay)
	img_low = take_picture(picam_low)
	cube_state[squarei('R', 5)] = get_colour(squarei('R', 3), img_low)
	cube_state[squarei('B', 3)] = get_colour(squarei('F', 5), img_low)
	renderedcube.draw_cube(cube_state, win)

	ard_write_moves("R2 L")
	time.sleep(delay)
	img_high = take_picture(picam_high)
	cube_state[squarei('L', 3)] = get_colour(squarei('L', 1), img_high)
	cube_state[squarei('B', 5)] = get_colour(squarei('U', 3), img_high)
	renderedcube.draw_cube(cube_state, win)
	ard_write_moves("L'")


	prev_error_list = []

	colour_test = ['R', 'L', 'D', 'U', 'B', 'F']
	
	ard.write(b"error-detect")
	wait_for_ard("updated")
	win.getMouse()
	
	for i in range(10):
		if (i > 2 and len(error_list) > 0):
			if (error_list[0] == prev_error_list[0]):
				fixed = False
				for sticker in error_list[0]:
					original_colour = cube_state[sticker]
					for colour in colour_test:
						cube_state[sticker] = colour
						test_error = errordetection.detect_errors(cube_state)
						if (len(test_error) == 0):
							test_solution = solver.solve(cube_state)
							if not (test_solution == None):
								fixed = True
								break
						cube_state[sticker] = original_colour
					if fixed:
						error_list = []
						break
				if (len(error_list) == 2):
					fixed = False
					for sticker in error_list[1]:
						original_colour = cube_state[sticker]
						for colour in colour_test:
							cube_state[sticker] = colour
							test_error = errordetection.detect_errors(cube_state)
							if (len(test_error) == 0):
								test_solution = solver.solve(cube_state)
								if not (test_solution == None):
									fixed = True
									break
							cube_state[sticker] = original_colour
						if fixed:
							break
		error_list = errordetection.detect_errors(cube_state)
		if (len(error_list) > 0):
			print(error_list)
			cube_state = fix_errors(cube_state, error_list, prev_error_list, picam_low, win)
		prev_error_list = error_list
	error_list = errordetection.detect_errors(cube_state)
	print(len(error_list))

	if (len(error_list) == 0):
		
		ard.write(b"solve")
		wait_for_ard("updated")
		
		solution = solver.solve(cube_state)
		if not (solution == None):
			ard_write_moves(solution)
	ard.write(b"complete")

	print(cube_state)



def scramble_cube(win):
	scramble_moves = gen_scramble()
	ard_write_moves(scramble_moves)
	ard.write(b"complete")
