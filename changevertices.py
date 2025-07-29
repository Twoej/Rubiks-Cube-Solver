import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import libcamera

points_file = open("points.txt", "w")
points_file.close()
points_file = open("points.txt", "a")

sticker_count = 0
point_count = 0

stickers = ["F7", "F8", "F5", "F2", "R7", "R6", "R3", "R0", "D1", "D2", "D5", "U0", "U3", "L0", "L1", "L2"]
temp_stickers_arr = []

img_low = None
img_high = None

def mousePoints(event, x, y, flags, params):
	global sticker_count
	global point_count
	global temp_stickers_arr
	global img_low
	global img_high
	if event == cv2.EVENT_LBUTTONDOWN:
		points_file.write(str(x) + " " + str(y) + " ")
		temp_stickers_arr.append([x, y])
		point_count += 1
		if (point_count > 3):
			if (sticker_count < 11):
				img_low = cv2.fillConvexPoly(img_low, np.array(temp_stickers_arr), color = (255, 255, 255))
				cv2.imshow('Low', img_low)
			else:
				img_high = cv2.fillConvexPoly(img_high, np.array(temp_stickers_arr), color = (255, 255, 255))
				cv2.imshow('High', img_high)
			temp_stickers_arr = []
			point_count = 0
			sticker_count += 1
			if sticker_count < len(stickers):
				print(stickers[sticker_count])
		

picam_low = Picamera2(1)
picam_high = Picamera2(0)

config = picam_low.create_preview_configuration(main={"size": (2592, 1944)})
picam_low.configure(config)
config = picam_high.create_preview_configuration(main={"size": (2592, 1944)})
picam_high.configure(config)

picam_low.start()
picam_high.start()

picam_low.capture_file("low_img.jpg")
img_low = cv2.imread("low_img.jpg", -1)
picam_high.capture_file("high_img.jpg")
img_high = cv2.imread("high_img.jpg", -1)

print(stickers[0])

cv2.imshow('Low', img_low)
cv2.setMouseCallback('Low', mousePoints)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imshow('High', img_high)
cv2.setMouseCallback('High', mousePoints)
cv2.waitKey()
cv2.destroyAllWindows()


picam_low.close()
picam_high.close()
points_file.close()
