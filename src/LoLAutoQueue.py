import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
import win32api, win32con
import os, time 

"""
All click functions assume a screen resoultion of 2560x1440.
Directory needs to be added line 13 and 14.
"""

templates = ""
capture = ""

def get_coords():
	x,y = win32api.GetCursorPos()
	print(x,y)

def test():
	cv2.imshow("image", capture_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	print(loc)

def screen_grab():
	im = ImageGrab.grab()
	im.save(os.getcwd() + '\\capture' + '.png', 'PNG')

def click(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	print("Clicking on accept match button at ({}, {})".format(x, y))

def auto_queue():
	time.sleep(1)
	screen_grab()

	# reading capture.png
	capture_img = cv2.imread(capture)
	capture_grey_img = cv2.cvtColor(capture_img, cv2.COLOR_BGR2GRAY)

	# loop through different button sizes
	print("Attempting to match template...")
	for i in range(4):
		template = cv2.imread(templates.format(i), 0)

		# MATCHING TEMPLATES
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(capture_grey_img, template, cv2.TM_CCOEFF_NORMED)
		threshold = 0.9;
		loc = np.where(res >= threshold)

		# DRAWING RECTANGLES
		for pt in zip(*loc[::-1]):
			cv2.rectangle(capture_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		try:
			x = pt[0] 
			y = pt[1] -- 40 # adjust for openCV border
			click(x,y)
			print("Successfully matched template. \nAccepting queue.")
			exit()
		except UnboundLocalError:
			print("Couldn't locate and match button{}.png...".format(i))
			pass   

def main():
	while True:
		auto_queue() 

if __name__ == '__main__':
	main()
