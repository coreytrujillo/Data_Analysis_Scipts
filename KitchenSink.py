from DataAnalysis_Functions import *
import matplotlib.pyplot as plt
from matplotlib import colors, rcParams, cycler, patches
from math import pi
import numpy as np
from statistics import stdev
import re


# Date Strings
datestrs = ['220418', '220418']

# Filter data for each experiment?
PlotFilter = 0

# Figure Output Values
fs = (20,12)
savefig = 0 # set to 1 to save pngs of figures
figrootname = './KitchenSinkFigs/' + datetime.now().strftime('%y%m%d') + '_KS_'

# File Location and Names
fpath = '../../Box_Experiments/'

fdry = '220418_TC_Benchmark/220418_TC_Benchmark_data.csv'
fwet = '220418_TC_WaterBoil/220418_TC_WaterBoil_data.csv'

fnames = [fdry, fwet] # Array of file names

# Labels
lbldry = ['Dry: All Shade', 'Dry: TC Sun LJ Shade', 'Dry: All Sun', 'Dry: TC Sun LJ Covered']
lblwet = ['Wet: LJ Shade', 'Wet: LJ Sun', 'Wet: LJ Covered']

lbl = lbldry + lblwet # Array of labels
lblidx = [lbldry, lblwet] # Array for label indices

# Initial time strings
tistrdry = ['13:29:00', '13:46:00', '13:59:00', '14:13:00']
tistrwet = ['15:23:00', '16:01:00', '16:30:00']

tistr = tistrdry + tistrwet # Array of inital time srings

# Final time strings
tfstrdry = ['13:40:00', '13:56:00', '14:07:00', '14:20:00']
tfstrwet = ['15:57:00', '16:20:00', '16:42:00']

tfstr = tfstrdry + tfstrwet # Array of final time srings

#######################################
# Don't change anything below this line
#######################################

# Identify which dataset is accociated with which file
filenum = []
for i in range(0, len(fnames)):
	for j in range(0, len(lblidx[i])):
		filenum.append(i)

# Compile data into single variable
data = []
for i in range(0, len(fnames)):
	datai = data_read_format(fpath + fnames[i], datestrs[i])
	datai['Time'] = pd.to_datetime(datai['Time'], format='%y%m%d %H:%M:%S.%f')
	
	if (datestrs[i] == '220313') or (datestrs[i] == '220314') or (datestrs[i] == '220315'):
		datai['PyrE'] = -datai['PyrE']
	data.append(datai)

# Setup plot colors
clrs = ['red', 'orange', 'gold', 'green','blue', 'purple', 'peru', 'gray', 'firebrick', 'chocolate', 'coral', 'lime', 'cornflowerblue', 'magenta', 'brown', 'darkred', 'coral', 'goldenrod', 'yellowgreen', 'cyan', 'slateblue', 'deeppink', 'darksalmon' , 'darkseagreen', 'darkturquoise', 'darkorchid']

# If there aren't enough color options for the dataset, show remaining options
if len(lbl)> len(clrs):
	# Notify user that there aren't enough colors named
	print('You need to add some colors \n')
	print('Consider the following: \n')
	
	# Identify remaning colors and plot for user
	poscols = [] # Initiate possible color variable
	for name, hex in colors.cnames.items():
		poscols.append(name)
	for x in set(poscols).intersection(clrs):
		poscols.remove(x)
	print(poscols)
	
	# Tell user how many colors are needed
	print('\nThere are only',  len(clrs), 'but',len(lbl) ,'datasets to plot')
	print('You need to add', len(lbl) - len(clrs),  'colors')
	print('Consider colors above')
	
	# Plot available colors
	rcParams['axes.prop_cycle'] = cycler(color = poscols)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ratio = 1.0 / 3.0
	count = np.ceil(np.sqrt(len(poscols)))
	x_count = count * ratio
	y_count = count / ratio
	x = 0
	y = 0
	w = 1 / x_count
	h = 1 / y_count
	for c in poscols:
		pos = (x / x_count, y / y_count)
		ax.add_patch(patches.Rectangle(pos, w, h, color=c))
		ax.annotate(c, xy=pos)
		if y >= y_count-1:
			x += 1
			y = 0
		else:
			y += 1

	plt.show()
	exit()

# Color and font settings for plots
rcParams['axes.prop_cycle'] = cycler(color = clrs) 
rcParams['font.size'] = 15

# Create a summary dataframe and add name and date data
smry =  pd.DataFrame()
dtstr = []
leg = []
for i in range(0,len(lbl)):
	dtstr.append(datestrs[filenum[i]])
	leg.append(datestrs[filenum[i]] + ' ' + lbl[i])
smry = smry.assign(Date=dtstr)
smry = smry.assign(Name=lbl)

# Define global variables
dc = data[0].columns # Get data headers
print('Headers:\n', dc)
figi = 1 # Initiate igure iterator
Ac = pi*0.6**2/4 # Area of the collector
numf = len(lbl) # Number of datasets

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
	[EffAve, EffSTDV] = timeplot(data, tistr, tfstr, Eff_headtag, numf, filenum, datestrs, leg, Eff_ptitle, Eff_xlab, Eff_ylab)
	
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
	[PowerAve, PowerSTDV] = timeplot(data, tistr, tfstr, Power_headtag, numf, filenum, datestrs, leg, Power_ptitle, Power_xlab, Power_ylab)
	
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
	[PyrAve, PyrSTDV] = timeplot(data, tistr, tfstr, Pyr_headtag, numf, filenum, datestrs, leg, Pyr_ptitle, Pyr_xlab, Pyr_ylab)
	
	# Output to Summary Table
	smry = smry.assign(Pyr_Pyr=PyrAve)
	smry = smry.assign(Pyr_STDV = PyrSTDV)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + Pyr_ptitle +'.png')

wild = re.compile('Temp*')
THead = [Tempstr for Tempstr in dc if re.match(wild, Tempstr)]

# Plot Thermocouple Data
if len(THead) > 0:
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	TC_ptitle = 'Temperatures'
	TC_xlab = 'Run Time (mins)'
	TC_ylab = 'Temperature ($^\circ$C)'
	
	TAve = []
	Tstdv = []
	for TH in THead:
		[TA, TS] = timeplot(data, tistr, tfstr, TH, numf, filenum, datestrs, leg, TC_ptitle, TC_xlab, TC_ylab)
		
		TAL = TH + '_Ave'
		TAS = TH + '_STDV'
		
		pos = len(smry.columns)
		smry.insert(loc=pos, column=TAL, value=TA)
		smry.insert(loc=pos+1, column=TAS, value=TS)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + TC_ptitle +'.png')


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
	plotaves(PyrAve, PowerAve, PyrSTDV, PowerSTDV, numf, leg, PyrPowAve_xlab, PyrPowAve_ylab, PyrPowAve_ptitle, PyrPowtx, PyrPowty)
	
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
	plotaves(EffAve, PowerAve, EffSTDV, PowerSTDV, numf, leg, PowEffAve_xlab, PowEffAve_ylab, PowEffAve_ptitle, PowEfftx, PowEffty)
	
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
	plotaves(PyrAve, EffAve, PyrSTDV, EffSTDV, numf, leg, PyrEffAve_xlab, PyrEffAve_ylab, PyrEffAve_ptitle, PyrEfftx, PyrEffty)
	
	# Save figure as png
	if savefig == 1:
		plt.savefig(figrootname + PyrEffAve_ptitle +'.png')
	
	##################################
	# Power vs. Ambient Temp
	plt.figure(figi, figsize=fs)
	figi += 1
	
	# Data and plot variables
	TempPowAve_xlab = 'Ambient Temperature [$^\circ$C]'
	TempPowAve_ylab = 'Power Output [W]'
	TempPowAve_ptitle = 'Ambient Temperature vs. Power'
	TempPowtx = 0
	TempPowty = 0
	
	# Create plot
	plotaves(TAve, PowerAve, Tstdv, PowerSTDV, numf, leg, TempPowAve_xlab, TempPowAve_ylab, TempPowAve_ptitle, TempPowtx, TempPowty)
	
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