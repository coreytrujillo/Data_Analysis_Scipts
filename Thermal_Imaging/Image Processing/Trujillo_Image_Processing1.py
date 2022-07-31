# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import pandas as pd
import time

def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY
	if event == cv2.EVENT_LBUTTONDBLCLK:
		[a1, a2, a3] = img[y, x]
		print(a1, a2, a3)
		a1 = int(a1)
		a2 = int(a2)
		a3 = int(a3)
		# b = (a[0],a[1],a[2])
		# print(b)
		cv2.circle(img,(x,y),10,(a1, a2, a3), -1)
		# print(np.asarray(a))
		print('location:', x,y)
		print('colors', img[y, x])
		mouseX,mouseY = x,y

def quad_area(x,y):
	# Finds the area of a quadrilateral from four points
	# given as vectors of x and y
	# Points should be clockwise from top left
	
	#  1 ______________2
	#	|			  /|
	#	|			/  |
	#	|		 /     |
	#	|	   /	   |
	#	|    /		   |
	#	|  /		   |
	#	|/_____________|
	#  0				3
	
	# Length of bottom on left of quadrilateral
	L02 = np.sqrt( (x[2] - x[0])**2 + (y[2] - y[0])**2 )
	L01 = np.sqrt( (x[1] - x[0])**2 + (y[1] - y[0])**2 )
	
	# Length of diagonal from bottom left corner to top right
	L03 = np.sqrt( (x[3] - x[0])**2 + (y[3] - y[0])**2 )
	
	# Angle between left and diagonal
	theta012 = np.arccos( ( (x[2] - x[0])*(x[1] - x[0]) + (y[2] - y[0])*(y[1] - y[0]) )/(L02 * L01) )
	
	# Angle between bottom and diagonal
	theta023 = np.arccos( ( (x[3] - x[0])*(x[2] - x[0]) + (y[3] - y[0])*(y[2] - y[0]) )/(L03 * L02) )
	
	# Height of top left triangle
	h012 = L01*np.sin(theta012)
	
	# Height of bottom right triangle
	h023 = L03*np.sin(theta023)
	
	# Triangle Areas
	A012 = (L03*h012)/2
	A023 = (L03*h023)/2
	
	# Total Area
	A = A012 + A023
	
	return(A)

global xloc, yloc
xloc = []
yloc = []

def outline(event, x, y, flags, param):

	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(img,(x,y),1,(255, 255, 255), -1)
		print('location:', x,y)
		xloc.append(x)
		yloc.append(y)
		print(len(xloc))
		print(xloc)
		if len(xloc) > 1:
			cv2.line(img, (xloc[-1], yloc[-1]), (xloc[-2],yloc[-2]), (255, 255, 255), 2)
		if len(xloc) == 4:
			cv2.line(img, (xloc[0], yloc[0]), (xloc[-1],yloc[-1]), (255, 255, 255), 2)
			Apix = quad_area(xloc, yloc)
			Ltrue = 6
			Wtrue = 6 
			Ltcm = Ltrue*0.3937008
			Wtcm = Wtrue*0.3937008
			Atcm = Ltcm*Wtcm
			
			Acmperpix = Atcm/Apix
			
			
			print(A)

def printcolors(event, x, y, flags, param):
	if event == cv2.EVENT_MOUSEMOVE:
		print(img[y,x])
	

fname = 'FLIR2314.jpg'
img = cv2.imread(fname)
print('Resolution: ', img.shape)
cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)
# cv2.setMouseCallback('image',outline)

A = False

if A:
	cv2.setMouseCallback('image',printcolors)

while(A):
	cv2.imshow('image',img)
	k = cv2.waitKey(20) & 0xFF
	if k == 27:
		break
	elif k == ord('a'):
		print('mouseX','mouseY')



if ~A:
	# rlow = np.array([54, 20, 230])
	rlow = np.array([0, 0, 200])
	rhi = np.array([255, 255, 255])
	filter = cv2.inRange(img, rlow, rhi)
	result = cv2.bitwise_and(img, img, mask = filter)
	cv2.imshow('Image1',result) # Image after bitwise operation
	cv2.waitKey(0)

cv.destroyWindow('Image1')
exit()
# a = True
# while True:
	# cv2.imshow('Original', img)
	# cv2.waitKey(0)
	# time.sleep(3)
# while True:
	
	# # time.sleep(10)
	
	# a = False

# exit()
# index = ["color", "color_name", "hex", "R", "G", "B"]
# data = pd.read_csv("colors.csv", names=index, header=None)

clicked = []



def call_back_function (event, x,y,flags,param):
  if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow("Color Detection Window")
cv2.setMouseCallback("Color Detection Window",call_back_function)
cv2.imshow('Color Detection Window', img)

while(1):
	cv2.imshow('Color Detection Window', img)
	cv2.waitKey(21)
	if (clicked):
		cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
		text = 'R='+str(r)+'G='+ str(g)+'B='+ str(b)
		print(text)
		cv2.putText(img, text,(50,50),2,0.8, (255,255,255),2,cv2.LINE_AA)
	if(r+g+b>=600):
		cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
		clicked=False
	if cv2.waitKey(20) & 0xFF ==27:
		break
cv2.destroyAllWindows()


exit()
image = cv2.imread(fname)
cv2.imshow('Original', image)
cv2.waitKey(0)

B, G, R = cv2.split(image)

cv2.imshow('Blue', B)
cv2.waitKey(0)

cv2.imshow('Green', G)
cv2.waitKey(0)

cv2.imshow('Red', R)
cv2.waitKey(0)

cv2.destroyAllWindows()