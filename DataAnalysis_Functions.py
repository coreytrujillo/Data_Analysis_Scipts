import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from statistics import stdev
from math import pi

# Read data and format for time	
def data_read_format(fpath, datestr):
	data = pd.read_csv(fpath, header = 0)
	data['Time'] = pd.to_datetime(datestr + ' ' + data['Time'], format='%y%m%d %H:%M:%S.%f')
	return data

# Filter data for time
def data_filter(data, datestr, tistr, tfstr):
	# This script filters data for a particular timeset
	# fpath = path to file string including file name
	# datestr = six-digit date string YYMMDD
	# tistr = filter start time string HH:MM:SS
	# tfstr = filter finish time string HH:MM:SS
	# lbl = label for this filtered dataset
	# hvar = string for header of data being filtered
	dti = datetime.strptime(datestr + ' ' + tistr, '%y%m%d %H:%M:%S')
	dtf = datetime.strptime(datestr + ' ' + tfstr, '%y%m%d %H:%M:%S')

	# Filter data
	filter = (data['Time'] > dti) & (data['Time'] < dtf) 

	dataf = data.loc[filter]
	return dataf

# Create the proper number of windows in a subplot
def subcount(WinCount):
	if WinCount < 1:
		print('Error! Nothing to Plot????')
	elif WinCount == 1:
		spx = 1
		spy = spx
	elif WinCount == 2:
		spx = 1
		spy = 2
	elif WinCount < 5:
		spx = 2
		spy = 2
	elif WinCount < 7:
		spx = 2
		spy = 3
	elif WinCount < 10:
		spx = 3
		spy = 3
	elif WinCount < 13:
		spx = 4
		spy = 3
	elif WinCount < 17:
		spx = 4
		spy = 4
	elif WinCount < 21:
		spx = 5
		spy = 4
	else:
		print('We need ', WinCount, 'windows')
		print('This is more windows than the subcount function is built for')
		print('please write a new scenario for WinCount')
		exit()
	
	return spx, spy

# Plot time series
def timeplot(data, tistr, tfstr, headtag, datestr, leg, ptitle, xlab, ylab):
	# data = combined data
	# headtag = header string. Use 'Eff' to calculate efficiency from irradiance and power
	# filenum = array of indicies for data files
	# datestr = string of dates for each dataset
	# leg = array of strings for legend
	# ptitle = plot title
	# xlab = xlabel
	# ylab = ylabel
	
	Ave = []
	STDV = []
	
	numf = len(tistr)
	for i in range(0, numf):
		# Filter data
		dataf = data_filter(data, datestr, tistr[i], tfstr[i])
		
		# Get min index of filtered data
		idxmin = dataf.index.min()
		
		# Get run time and format for minutes
		dtime = dataf['Time'] - dataf['Time'][idxmin]
		dtime = dtime.dt.total_seconds()/60
		
		if headtag == 'Eff':
			Ac = pi*0.6**2/4
			Eff = dataf['Power']/(dataf['PyrE']*Ac)*100
			Ave.append(Eff.mean())
			STDV.append(stdev(Eff))
			plt.plot(dtime, Eff)	
			
		else: 
			# Find and record average and STDV of data
			Ave.append(dataf[headtag].mean())
			STDV.append(stdev(dataf[headtag]))
			
			# Plot data
			plt.plot(dtime, dataf[headtag])
	
	# Configure plot
	plt.title(ptitle)
	plt.legend(leg, fontsize=10)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	# plt.show()
	
	# Format output arrays
	Ave = np.asarray(Ave)
	STDV = np.asarray(STDV)
	
	return Ave, STDV

# Linear Regression	
def linreg(x, y, tx, ty):
	# This script takes data and performs a linear regression. It outputs the trendline and R-Squared value. 
	# See notes from Murty's ME Analysis from 10/10 for how this was developed
	# S = C*V
	
	x = np.asarray(x)
	y = np.asarray(y)
	
	# Vandermonde? Matrix
	V = np.array([[len(x), sum(x)], [sum(x), sum(x*x)]]) 
	S = np.array([[sum(y)], [sum(x*y)]])
	
	# Coefficients of tendline
	C = np.linalg.solve(V, S)
	C = np.flip(C)
	
	# Evaluate Trendline at Coefficients
	TLx = np.sort(x)
	TLy = np.polyval(C, TLx)
	
	# Calculate R-squared value
	SSR = sum((np.polyval(C, x) - y)**2)
	SST = sum((y - np.mean(y))**2)
	R2 = 1 - SSR/SST
	
	# Text locations and content
	if tx == 0:
		tx = TLx[-1] - (TLx[-1] - TLx[0])*0.15
	if ty == 0:	
		if C[0][0] > 0:
			ty = TLy[-1]
		elif C[0][0] < 0:
			ty = TLy[-1] + abs(TLy[-1] - TLy[0])*0.2
	tstr =  'y = ' + "{:.2f}".format(C[0][0]) + 'x + ' + "{:.2f}".format(C[1][0]) + '\nR$^2$ = ' + "{:.2f}".format(R2)
	
	return(TLx, TLy, C, R2, tx, ty, tstr)

# Plot averaged values with error bars
def plotaves(xave, yave, xstdv, ystdv, leg, xlab, ylab, ptitle, tx, ty):
	numf = len(leg)
	for i in range(0, numf):
		plt.errorbar(xave[i], yave[i], xerr=xstdv[i], yerr=ystdv[i], fmt='o')
	
	plt.grid()
	plt.legend(leg, fontsize = 10)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.title(ptitle)
	
	[TLx, TLy, Coeff, R2, tx, ty, tstr] = linreg(xave, yave, tx, ty)
	plt.plot(TLx, TLy, 'k:')
	plt.text(tx, ty, tstr)
	