import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
import win32api, win32con
import os, time 

"""
All coordinates assume a screen resoultion of 2560x1440, and 
a league client resolution 1280x720.
Directory needs to be added line 35 and 36.
"""

def get_coords():
	x,y = win32api.GetCursorPos()
	print(x,y)

def test():
	cv2.imshow("img", img)
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
	print("Clicking on ({}, {})".format(x, y))

def find_matches():
	accept_match_button = "INSERT DIRECTORY"
	capture = "INSERT DIRECTORY"

	screen_grab()

	img = cv2.imread(capture)
	grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(accept_match_button, 0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.9;
	loc = np.where(res >= threshold)

	for pt in zip(*loc[::-1]):
		cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

	try:
		x = pt[0] 
		y = pt[1] -- 40 #adjust for openCV
		click(x,y)
		print("Successfully matched template... \n Accepting queue.")
		exit()
	except UnboundLocalError:
		print("Couldn't locate and match template image...")
		time.sleep(4)
		pass   

def main():
	while True:
		find_matches() 

if __name__ == '__main__':
	main()
