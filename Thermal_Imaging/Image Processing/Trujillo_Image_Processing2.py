# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import pandas as pd
import time
import matplotlib.pyplot as plt

# This function will draw a circle where you double click on the image
def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY
	if event == cv2.EVENT_LBUTTONDBLCLK:
		[a1, a2, a3] = img[y, x]
		print(a1, a2, a3)
		a1 = int(a1)
		a2 = int(a2)
		a3 = int(a3)
		cv2.circle(img,(x,y),10,(a1, a2, a3), -1)
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

# Make location variables
# Must be before outline function 
global xloc, yloc, corn
xloc = []
yloc = []
corn = []
def clickfilter(event, x, y, flags, param):
	# This function outlines a rectangle
	# Click clockwise from top right

	# If doubleclick
	if event == cv2.EVENT_LBUTTONDBLCLK:
		
		# Draw a white circle
		# cv2.circle(img,(x,y),1,img[y,x], -1)
		
		# Print the location of that click
		print('location:', x,y)
		
		# Append location vectors
		xloc.append(x)
		yloc.append(y)
		
		
		
		xx = []
		yy = []
		# if len(xloc) == 1:
		bmax = 0
		gmax = 0
		rmax = 0
		bmin = 300
		gmin = 300
		rmin = 300
		if len(xloc) >1:
			if xloc[0] > xloc[1]:
				for i in range(xloc[1], xloc[0]):
					xx.append(i)
			else:
				for i in range(xloc[0], xloc[1]):
					xx.append(i)
			if yloc[0] > yloc [1]:
				for j in range(yloc[1], yloc[0]):
					yy.append(j)
			else:
				for j in range(yloc[0], yloc[1]):
					yy.append(j)
			
			for k in yy:
				[b, g, r] = img[k, xloc[1]]
				print(b, g, r)
				if b > bmax:
					bmax = b
				if b < bmin:
					bmin = b
				if g > gmax:
					gmax = g
				if g < gmin:
					gmin = g
				if r > rmax:
					rmax = r
				if r < rmin:
					rmin = r
			
			bmin = 50
			gmin = 26
			rmin = 215
			rlow = np.array([bmin, gmin, rmin])
			# rlow = np.array([0, 0, 0])
			bmax = 255
			gmax = 255
			rmax = 255
			rhi = np.array([bmax, gmax, rmax])
			# rhi = np.array([255, 255, 255])
			print(rlow)
			print(rhi)
			filt = cv2.inRange(img, rlow, rhi)
			result = cv2.bitwise_and(img, img, mask = filt)
			cv2.imshow('Image1', result)
		
		# # # # # After first click, draw lines between clicks
		# # # # if len(xloc) > 1:
			# # # # cv2.line(img, (xloc[-1], yloc[-1]), (xloc[-2],yloc[-2]), (255, 255, 255), 2)
		
		# # # # # draw line between fourth click and first click
		# # # # if len(xloc) == 4:
			# # # # cv2.line(img, (xloc[0], yloc[0]), (xloc[-1],yloc[-1]), (255, 255, 255), 2)
			
			# # # # # Calculate quadrilateral area in pixels		
			# # # # Apix = quad_area(xloc, yloc)
			
			# # # # # Calculate area of quadrilateral in cm
			# # # # Ltrue = 2 # Vertical distance on pic in inches
			# # # # Wtrue = 12 # Horizontal distance on pic in inches
			
			# # # # # Convert to cm
			# # # # Ltcm = Ltrue*0.3937008
			# # # # Wtcm = Wtrue*0.3937008
			
			# # # # # Caluclate area in cm2
			# # # # Atcm = Ltcm*Wtcm
			
			# # # # # Calculate cm2 per pixel
			# # # # Acmperpix = Atcm/Apix
			
			
			# # # # corn = np.array([xloc, yloc])
			# # # # corn = corn.T
			# # # # print('Corn1', corn)

			
			
			
			# # # # return Acmperpix, corn# XXXXX Figure out how to get this out!!!!!!!!!!!!!!!!!!

def printcolors(event, x, y, flags, param):
	if event == cv2.EVENT_MOUSEMOVE:
		print(img[y,x])
		

def printloc(event, x, y, flags, param):
	if event == cv2.EVENT_MOUSEMOVE:
		print(x,y)

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


#############################################3
#############################################
################################################
################################################
def outline(event, x, y, flags, param):
	# This function outlines a rectangle
	# Click clockwise from top right

	# If doubleclick
	if event == cv2.EVENT_LBUTTONDBLCLK:
		
		# Draw a white circle
		cv2.circle(img,(x,y),1,(255, 255, 255), -1)
		
		# Append location vectors
		xloc.append(x)
		yloc.append(y)

		# After first click, draw lines between clicks
		if len(xloc) > 1:
			cv2.line(img, (xloc[-1], yloc[-1]), (xloc[-2],yloc[-2]), (255, 255, 255), 2)
		
		# draw line between fourth click and first click
		if len(xloc) == 4:
			cv2.line(img, (xloc[0], yloc[0]), (xloc[-1],yloc[-1]), (255, 255, 255), 2)
			
			# Calculate quadrilateral area in pixels		
			Apix = quad_area(xloc, yloc)
			
			# Calculate area of quadrilateral in cm
			Ltrue = 2 # Vertical distance on pic in inches
			Wtrue = 12 # Horizontal distance on pic in inches
			
			# Convert to cm
			Ltcm = Ltrue*0.3937008
			Wtcm = Wtrue*0.3937008
			
			# Caluclate area in cm2
			Atcm = Ltcm*Wtcm
			
			# Calculate cm2 per pixel
			Acmperpix = Atcm/Apix
			
			
			corn = np.array([xloc, yloc])
			corn = corn.T
			print('Corn1', corn)


# Outline rectangle and calculate the area
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	print('Resolution: ', img.shape)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', outline)

	while True:
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF
		
# Create a dot where ever you double click
# The dot will be the color of the pixel clicked
# The RGB values will be printed to the terminal
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', draw_circle)

	while True:
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF

# Print the color values where the mouse hovers
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', printcolors)

	while(True):
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF
		if k == 27:
			break
		elif k == ord('a'):
			print('mouseX','mouseY')

# Plot colorbar color values
if 1 == 1:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	ytop = 50
	ymid = 240
	ybot = 430
	ytq = 144
	ybq = 336
	yploc = np.arange(ytop,ybot)
	bv = [] 
	gv = [] 
	rv = []
	for i in yploc:
		[b,g,r] = img[i,626]
		bv.append(b)
		gv.append(g)
		rv.append(r)
	
	itr = 0
	for i in range(ytop, ybot):
		if i <= ytq:
			ibq = itr
		elif i <= ymid:
			imid = itr
		elif i <= ybq:
			itq = itr
		elif i <= ybot:
			itop = itr
		else:
			print('We have a problem')
			exit()
		itr += 1
	
	q1min = np.array([min(bv[0:ibq]), min(gv[0:ibq]), min(rv[0:ibq])])
	q2min = np.array([min(bv[ibq:imid]), min(gv[ibq:imid]), min(rv[ibq:imid])])
	q3min = np.array([min(bv[imid:itq]), min(gv[imid:itq]), min(rv[imid:itq])])
	q4min = np.array([min(bv[itq:-1]), min(gv[itq:-1]), min(rv[itq:-1])])
	q1max = np.array([max(bv[0:ibq]), max(gv[0:ibq]), max(rv[0:ibq])])
	q2max = np.array([max(bv[ibq:imid]), max(gv[ibq:imid]), max(rv[ibq:imid])])
	q3max = np.array([max(bv[imid:itq]), max(gv[imid:itq]), max(rv[imid:itq])])
	q4max = np.array([max(bv[itq:-1]), max(gv[itq:-1]), max(rv[itq:-1])])
	
	fq1 = cv2.inRange(img, q1min, q1max)
	rq1 = cv2.bitwise_and(img, img, mask = fq1)
		
	fq2 = cv2.inRange(img, q2min, q2max)
	rq2 = cv2.bitwise_and(img, img, mask = fq2)
		
	fq3 = cv2.inRange(img, q3min, q3max)
	rq3 = cv2.bitwise_and(img, img, mask = fq3)
		
	fq4 = cv2.inRange(img, q4min, q4max)
	rq4 = cv2.bitwise_and(img, img, mask = fq4)
	
	
	plt.plot(bv, yploc, 'b')
	plt.plot(gv, yploc, 'g')
	plt.plot(rv, yploc, 'r')
	plt.plot(np.arange(0,255), ymid*np.ones(255), 'k')
	plt.plot(np.arange(0,255), ytq*np.ones(255), 'k')
	plt.plot(np.arange(0,255), ybq*np.ones(255), 'k')
	plt.plot(np.arange(0,255), ytop*np.ones(255), 'k')
	plt.plot(np.arange(0,255), ybot*np.ones(255), 'k')
	plt.gca().invert_yaxis()
	plt.xlabel('Color Value')
	plt.ylabel('Y-pixel location')
	
	
	
	cv2.line(img, (620, ytop), (630,ytop), (0, 0, 255), 1)
	cv2.line(img, (620, ymid), (630,ymid), (0, 0, 255), 1)
	cv2.line(img, (620, ybot), (630,ybot), (0, 0, 255), 1)
	cv2.line(img, (620, ytq), (630,ytq), (0, 0, 255), 1)
	cv2.line(img, (620, ybq), (630,ybq), (0, 0, 255), 1)
	cv2.imshow('Orig', img)
	
	cv2.imshow('Quarter 1 Filter', rq1)
	cv2.imshow('Quarter 2 Filter', rq2)
	cv2.imshow('Quarter 3 Filter', rq3)
	cv2.imshow('Quarter 4 Filter', rq4)
	
	plt.show()
	cv2.waitKey(0)






# Print the image location anywhere you doubleclick
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', printloc)
	while(True):
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF
		if k == 27:
			break
		elif k == ord('a'):
			print('mouseX','mouseY')

# Show cropped image and increase size
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	crop = img[49:436, 614:637]
	
	cv2.imshow('Orig', img)
	cv2.imshow('Cropped', crop)
	
	scale = 2
	sw = int(crop.shape[1]*scale)
	sh = int(crop.shape[0]*scale)
	dim = (sw, sh)
	
	resized = cv2.resize(crop, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow('Resized', resized)
	
	cv2.waitKey(0)



#  Show filtered image
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	rlow = np.array([0, 0, 200])
	rhi = np.array([255, 255, 255])
	filt = cv2.inRange(img, rlow, rhi)
	result = cv2.bitwise_and(img, img, mask = filt)
	cv2.imshow('Image1', result) # Image after bitwise operation
	cv2.waitKey(0)
	

# Blackout everything except rectangle
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	print('Resolution: ', img.shape)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', outline)

	while True:
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF # Escape Key 
		if k == 27: # If escape key is hit
			break
		elif k == ord('b'): # if B key is hit
			corn = np.array([[67, 216], [554, 209], [552, 293], [65, 298]]) # rectangle corners
			p1 = np.array([[0, 0], corn[0,:], corn[1,:],  [img.shape[1], 0] ]) # area above rectangle
			p2 = np.array([ [img.shape[1], 0], corn[1,:], corn[2,:], [img.shape[1], img.shape[0]] ]) # area right of rectangle
			p3 = np.array([ [img.shape[1], img.shape[0]], corn[2,:], corn[3,:], [0, img.shape[0]] ]) # area below rectangle
			p4 = np.array([ [0, img.shape[0]], corn[3,:], corn[0,:], [0,0] ]) # area left of rectangle
			
			# Fill areas with black
			cv2.fillPoly(img, [p1], (0,0,0))
			cv2.fillPoly(img, [p2], (0,0,0))
			cv2.fillPoly(img, [p3], (0,0,0))
			cv2.fillPoly(img, [p4], (0,0,0))
			
#  Click to filter
if 1 == 0:
	fname = 'FLIR2540.jpg'
	img = cv2.imread(fname)
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', clickfilter)
	while True:
		cv2.imshow('image',img)
		k = cv2.waitKey(20) & 0xFF # Escape Key 
		if k == 27: # If escape key is hit
			break
	
	# rlow = np.array([0, 0, 200])
	# rhi = np.array([255, 255, 255])
	# filt = cv2.inRange(img, rlow, rhi)
	# result = cv2.bitwise_and(img, img, mask = filt)
	# cv2.imshow('Image1', result) # Image after bitwise operation
	# cv2.waitKey(0)




cv2.destroyAllWindows()
