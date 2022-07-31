from DataAnalysis_Functions import *
import matplotlib.pyplot as plt
from matplotlib import colors, rcParams, cycler, patches
from math import pi
import numpy as np
from statistics import stdev
import re


# Date Strings
datestr = '220515'

# Filter data for each experiment?
PlotFilter = 1

# Figure Output Values
fs = (20,12)
savefig = 0 # set to 1 to save pngs of figures
figrootname = datetime.now().strftime('%y%m%d') + '_KS_'

# File Location and Names
fpath = '../../Box_Experiments/220515_SingleChannel_GACSoil/'

fname = '220515_PowerBenchmark_data.csv'

lbl = ['C1 FC', 'C2 FA', 'C3 FF'] # Array of labels

# Initial time strings
tistr = ['13:03:30', '13:30:00', '13:56:00']
tfstr = ['13:14:00', '13:41:00', '15:52:00']

#######################################
# Don't change anything below this line
#######################################

data = data_read_format(fpath + fname, datestr)

rcParams['font.size'] = 15

# Create a summary dataframe and add name and date data
smry =  pd.DataFrame()
dtstr = []
leg = []
for i in range(0,len(lbl)):
	dtstr.append(datestr)
	leg.append(datestr + ' ' + lbl[i])
smry = smry.assign(Date=dtstr)
smry = smry.assign(Name=lbl)

# Define global variables
dc = data.columns # Get data headers
print('Headers:\n', dc)
figi = 1 # Initiate igure iterator
Ac = pi*0.6**2/4 # Area of the collector
numf = len(lbl) # Number of datasets

# Power Plot
if 'Power' in dc:
	plt.figure(figi)
	figi += 1
	plt.subplot(211)
	plt.title(datestr + ' Power Data')
	plt.xlabel('Time (MDT)')
	plt.ylabel('Power [W]')
	plt.scatter(data['Time'], data['Power'])
	
	if PlotFilter == 1:
		for i in range(0, len(lbl)):
			dataf = data_filter(data, datestr, tistr[i], tfstr[i])
			
			plt.scatter(dataf['Time'], dataf['Power'])
	
			
if 'PyrE' in dc:
	plt.subplot(212)
	plt.title(datestr + ' Pyrheliometer Data')
	plt.xlabel('Time (MDT)')
	plt.ylabel('Power (W/m$^2$)')
	plt.scatter(data['Time'], data['PyrE'])
	
	if PlotFilter == 1:
		for i in range(0, len(lbl)):
			dataf = data_filter(data, datestr, tistr[i], tfstr[i])
			
			plt.scatter(dataf['Time'], dataf['PyrE'])
			
		plt.legend(['Unfiltered'] + lbl)
	plt.tight_layout(h_pad=-2)

# Efficiency Time seriesPlot
if ('PyrE' in dc) & ('Power' in dc):
	# Setup figure and variables
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	Eff_headtag = 'Eff'
	Eff_ptitle = 'Efficiency'
	Eff_xlab = 'Efficiency [%]'
	Eff_ylab = 'Run Time (mins)'
	
	# Create Plot
	[EffAve, EffSTDV] = timeplot(data, tistr, tfstr, Eff_headtag, datestr, leg, Eff_ptitle, Eff_xlab, Eff_ylab)
	
	# Output to summary table
	smry = smry.assign(Eff_Ave=EffAve)
	smry = smry.assign(Eff_STDV = EffSTDV)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + Eff_ptitle +'.png')
	
# Power Timeseries Plot
if 'Power' in dc:
	# Setup figure and variables 
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	Power_headtag = 'Power'
	Power_ptitle = 'Power Comparison'
	Power_xlab = 'Run Time (mins)'
	Power_ylab = 'Power [W]'
	
	# Create Plot
	[PowerAve, PowerSTDV] = timeplot(data, tistr, tfstr, Power_headtag, datestr, leg, Power_ptitle, Power_xlab, Power_ylab)
	
	# Output to summary table
	smry = smry.assign(Power_Ave=PowerAve)
	smry = smry.assign(Power_STDV = PowerSTDV)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + Power_ptitle +'.png')

# Irradiance Timeseries Plot
if 'PyrE' in dc:
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	Pyr_headtag = 'PyrE'
	Pyr_ptitle = 'Pyrheliometer Comparison'
	Pyr_xlab = 'Run Time (mins)'
	Pyr_ylab = 'Power [W/m$^2$]'
	
	# Create plot
	[PyrAve, PyrSTDV] = timeplot(data, tistr, tfstr, Pyr_headtag, datestr, leg, Pyr_ptitle, Pyr_xlab, Pyr_ylab)
	
	# Output to Summary Table
	smry = smry.assign(Pyr_Pyr=PyrAve)
	smry = smry.assign(Pyr_STDV = PyrSTDV)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + Pyr_ptitle +'.png')

# Quadratic and linear regression on just C3 FF
plt.figure(figi, figsize=fs)
figi += 1
dflong = data_filter(data, datestr, tistr[-1], tfstr[-1])
DI = dflong['PyrE']*Ac
plt.scatter(DI, dflong['Power'])
plt.xlabel('Solar Irradiance [W]')
plt.ylabel('Power Output [W]')
plt.title('Solar Irradiance vs. Power Output for Collector 3 Fiber F during Hazy Clouds')
[TLx, TLy, C, R2, txo, tyo, tstr] = quadreg(DI, dflong['Power'], 190, 60)
plt.plot(TLx, TLy, 'k:')
plt.text(txo, tyo, tstr,)
[TLx, TLy, C, R2, txo, tyo, tstr] = linreg(DI, dflong['Power'], 210, 44)
plt.plot(TLx, TLy, 'r:')
plt.text(txo, tyo, tstr, c='r')


# Quadratic Regression for all filtered datasets
if 1 == 0:
	tx = [255, 230, 145]
	ty = [55, 40, 50]
	plt.figure(figi, figsize=fs)
	figi += 1
	for i in range(0, len(tistr)):
		dflong = data_filter(data, datestr, tistr[i], tfstr[i])
		DI = dflong['PyrE']*Ac
		plt.scatter(DI, dflong['Power'])
	
	plt.legend(lbl)
	plt.xlabel('Solar Irradiance [W/m$^2$]')
	plt.ylabel('Power Output [W]')
	plt.title('Solar Irradiance vs. Power Output for Collector 3 Fiber F during Hazy Clouds')
	
	for i in range(0, len(tistr)):
		dflong = data_filter(data, datestr, tistr[i], tfstr[i])
		DI = dflong['PyrE']*Ac
		[TLx, TLy, C, R2, txo, tyo, tstr] = quadreg(DI, dflong['Power'], tx[i], ty[i])
		plt.plot(TLx, TLy, 'k:')
		plt.text(txo, tyo, tstr)

# Linear Regression for all filtered datasets
if 1 == 0:
	tx = [255, 230, 145]
	ty = [55, 40, 50]
	plt.figure(figi, figsize=fs)
	figi += 1
	for i in range(0, len(tistr)):
		dflong = data_filter(data, datestr, tistr[i], tfstr[i])
		DI = dflong['PyrE']*Ac
		plt.scatter(DI, dflong['Power'])
	
	plt.legend(lbl)
	plt.xlabel('Solar Irradiance [W/m$^2$]')
	plt.ylabel('Power Output [W]')
	plt.title('Solar Irradiance vs. Power Output for Collector 3 Fiber F during Hazy Clouds')
	
	for i in range(0, len(tistr)):
		dflong = data_filter(data, datestr, tistr[i], tfstr[i])
		DI = dflong['PyrE']*Ac
		[TLx, TLy, C, R2, txo, tyo, tstr] = linreg(DI, dflong['Power'], tx[i], ty[i])
		plt.plot(TLx, TLy, 'k:')
		plt.text(txo, tyo, tstr)

# Averaged plots with standard deviations
if ('PyrE' in dc) & ('Power' in dc):
	##################################
	# Irradiance vs. Power
	plt.figure(figi, figsize=fs)
	figi += 1

	# Data and plot variables
	PyrPowAve_xlab = 'Solar Irradiance [W/m$^2$]'
	PyrPowAve_ylab = 'Power Output [W]'
	PyrPowAve_ptitle = 'Solar Irradiance vs. Power'
	PyrPowtx = 0
	PyrPowty = 0
	
	# Create plot
	plotaves(PyrAve, PowerAve, PyrSTDV, PowerSTDV, leg, PyrPowAve_xlab, PyrPowAve_ylab, PyrPowAve_ptitle, PyrPowtx, PyrPowty)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + PyrPowAve_ptitle +'.png')
	
	##################################
	# Efficiency vs. Power
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	PowEffAve_xlab = 'Average Efficiency [%]'
	PowEffAve_ylab = 'Power Output [W]'
	PowEffAve_ptitle = 'Effeciency vs. Power'
	PowEfftx = 0
	PowEffty = 0
	
	# Create Plot
	plotaves(EffAve, PowerAve, EffSTDV, PowerSTDV, leg, PowEffAve_xlab, PowEffAve_ylab, PowEffAve_ptitle, PowEfftx, PowEffty)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + PowEffAve_ptitle +'.png')
	
	##################################
	# Irradiance vs. Efficiency
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Create Plot
	PyrEffAve_xlab = 'Solar Irradiance [W/m$^2$]'
	PyrEffAve_ylab = 'Average Efficiency [%]'
	PyrEffAve_ptitle = 'Irradiance vs. Efficiency'
	PyrEfftx = 0
	PyrEffty = 0
	
	# Create Plot
	plotaves(PyrAve, EffAve, PyrSTDV, EffSTDV, leg, PyrEffAve_xlab, PyrEffAve_ylab, PyrEffAve_ptitle, PyrEfftx, PyrEffty)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + PyrEffAve_ptitle +'.png')
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + TempPowAve_ptitle +'.png')
	


# Output summary csv file
outf = __file__ 
outf = outf[:-3]
outf = outf + '_Summary.csv'
smry.to_csv(outf)

# Show plots

plt.show()