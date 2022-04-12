from DataAnalysis_Functions import *
import matplotlib.pyplot as plt
from matplotlib import colors, rcParams, cycler
from math import pi
import numpy as np
from statistics import stdev

# File Location and Names
fpath = '../Box_Experiments/'

fnames = ['220315_CollectorBenchmark/220315_CollectorBenchmark_data.csv', '220324_CollectorBenchmark/220324_CollectorBenchmark_data.csv', '220331_CollectorFiberBenchmark/220331_CollectorFiberBenchmark_data.csv']

# Date Strings Remove XXXXXXXXXX
datestrs = ['220315', '220324', '220331']

# Filter data for each experiment?
PlotFilter = 1

# Which dataset is accociated with which file?
filenum = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]

# Labels
lbl = ['C1 FB', 'C2 FB', 'C3 FB', 'C4 FB', 'C2 FB: Round II', 'C2 FB', 'C4 FB', 'C3 FC', 'C1 FC', 'C1 FC', 'C2 FA', 'C3 FF', 'C4 FD']

# Initial Time filters
tistr = ['12:00:00', '13:01:00', '14:06:00', '15:25:15', '16:25:00', '13:44:00', '14:40:00', '15:32:00', '16:32:00', '13:42:00', '14:16:00', '14:46:00', '15:15:00']

# Final time filters
tfstr = ['12:10:00', '13:11:00', '14:17:00', '15:36:00', '16:35:00', '13:54:00', '14:50:00', '15:42:00', '16:44:00', '13:52:00', '14:26:00', '14:56:00', '15:26:00']

# Read Data 
data1 = data_read_format(fpath + fnames[0], datestrs[0])
data2 = data_read_format(fpath + fnames[1], datestrs[1])
data3 = data_read_format(fpath + fnames[2], datestrs[2])

# Format Time in all datasets
data1['Time'] = pd.to_datetime(data1['Time'], format='%y%m%d %H:%M:%S.%f')
data2['Time'] = pd.to_datetime(data2['Time'], format='%y%m%d %H:%M:%S.%f')
data3['Time'] = pd.to_datetime(data3['Time'], format='%y%m%d %H:%M:%S.%f')

# Format pyrheliometer in necessary dataset
data1['PyrE'] = -data1['PyrE']

# Combine Data
data = [data1, data2, data3]

################################
# Don't change anything below this line
################################

# Setup plot colors
clrs = ['red', 'orange', 'gold', 'green','blue', 'purple', 'peru', 'gray', 'firebrick', 'chocolate', 'coral', 'lime', 'cornflowerblue', 'magenta', 'brown', 'darkred', 'coral', 'goldenrod', 'yellowgreen', 'cyan', 'slateblue' ]
if len(lbl) > len(clrs):
	print('You need to add some colors \n')
	print('Consider the following: \n')
	for name, hex in colors.cnames.items():
		print(name)
	print('\nYou need to add some colors \n')
	print('Consider colors above \n')
	exit()
rcParams['axes.prop_cycle'] = cycler(color = clrs) 

# Create a summary dataframe
smry =  pd.DataFrame()
dtstr = []
for i in range(0, len(lbl)):
	dtstr.append(datestrs[filenum[i]])
smry = smry.assign(Date=dtstr)
smry = smry.assign(Name=lbl)

# Create Legend
leg = []
for i in range(0, len(lbl)):
	leg.append(datestrs[filenum[i]] + ' ' + lbl[i])

# Set up variables
dc = data1.columns # Get headers
figi = 1 # Figure iterator
Ac = pi*0.6**2/4
numf = len(lbl) # Number of datasets

# Efficiency Time seriesPlot
if ('PyrE' in dc) & ('Power' in dc):
	# Setup figure and variables
	plt.figure(figi)
	figi += 1
	
	Eff_headtag = 'Eff'
	Eff_ptitle = 'Efficiency'
	Eff_xlab = 'Efficiency [%]'
	Eff_ylab = 'Run Time (mins)'
	
	[EffAve, EffSTDV] = timeplot(data, tistr, tfstr, Eff_headtag, numf, filenum, datestrs, leg, Eff_ptitle, Eff_xlab, Eff_ylab)
	
	# Output to summary table
	smry = smry.assign(Eff_Ave=EffAve)
	smry = smry.assign(Eff_STDV = EffSTDV)
	
# Power Timeseries Plot
if 'Power' in dc:
	# Setup figure and variables 
	plt.figure(figi)
	figi += 1
	
	Power_headtag = 'Power'
	Power_ptitle = 'Power Comparison'
	Power_xlab = 'Run Time (mins)'
	Power_ylab = 'Power [W]'
		
	[PowerAve, PowerSTDV] = timeplot(data, tistr, tfstr, Power_headtag, numf, filenum, datestrs, leg, Power_ptitle, Power_xlab, Power_ylab)
	
	# Output to summary table
	smry = smry.assign(Power_Ave=PowerAve)
	smry = smry.assign(Power_STDV = PowerSTDV)

# Irradiance Timeseries Plot
if 'PyrE' in dc:
	plt.figure(figi)
	figi += 1
	
	Pyr_headtag = 'PyrE'
	Pyr_ptitle = 'Pyrheliometer Comparison'
	Pyr_xlab = 'Run Time (mins)'
	Pyr_ylab = 'Power [W/m$^2$]'
	
	[PyrAve, PyrSTDV] = timeplot(data, tistr, tfstr, Pyr_headtag, numf, filenum, datestrs, leg, Pyr_ptitle, Pyr_xlab, Pyr_ylab)
	
	# Output to Summary Table
	smry = smry.assign(Pyr_Pyr=PyrAve)
	smry = smry.assign(Pyr_STDV = PyrSTDV)

# Plot Thermocouple Data
if 'TC1' in dc:
	plt.figure(figi)
	figi += 1
	
	TC_headtag = 'TC1'
	TC_ptitle = 'Ambient Temperature'
	TC_xlab = 'Run Time (mins)'
	TC_ylab = 'Temperature ($^\circ$C)'
	
	[TAve, Tstdv] = timeplot(data, tistr, tfstr, TC_headtag, numf, filenum, datestrs, leg, TC_ptitle, TC_xlab, TC_ylab)
	
	# Output to Summary Table
	smry = smry.assign(T_Ave_Amb=TAve)
	smry = smry.assign(T_stdv = Tstdv)


# Averaged plots with standard deviations
if ('PyrE' in dc) & ('Power' in dc):
	##################################
	# Irradiance vs. Power
	plt.figure(figi)
	figi += 1

	PyrPowAve_xlab = 'Solar Irradiance [W/m$^2$]'
	PyrPowAve_ylab = 'Power Output [W]'
	PyrPowAve_ptitle = 'Solar Irradiance vs. Power'

	plotaves(PyrAve, PowerAve, PyrSTDV, PowerSTDV, numf, leg, PyrPowAve_xlab, PyrPowAve_ylab, PyrPowAve_ptitle)
	
	##################################
	# Efficiency vs. Power
	plt.figure(figi)
	figi += 1
	
	PowEffAve_xlab = 'Average Efficiency [%]'
	PowEffAve_ylab = 'Power Output [W]'
	PowEffAve_ptitle = 'Effeciency vs. Power'
	
	plotaves(EffAve, PowerAve, EffSTDV, PowerSTDV, numf, leg, PowEffAve_xlab, PowEffAve_ylab, PowEffAve_ptitle)
	
	##################################
	# Irradiance vs. Efficiency
	plt.figure(figi)
	figi += 1
	
	PyrEffAve_xlab = 'Solar Irradiance [W/m$^2$]'
	PyrEffAve_ylab = 'Average Efficiency [%]'
	PyrEffAve_ptitle = 'Irradiance vs. Efficiency'
	
	plotaves(PyrAve, EffAve, PyrSTDV, EffSTDV, numf, leg, PyrEffAve_xlab, PyrEffAve_ylab, PyrEffAve_ptitle)
	
	##################################
	# Power vs. Ambient Temp
	plt.figure(figi)
	figi += 1
	
	TempPowAve_xlab = 'Ambient Temperature [$^\circ$C]'
	TempPowAve_ylab = 'Power Output [W]'
	TempPowAve_ptitle = 'Ambient Temperature vs. Power'
	
	plotaves(TAve, PowerAve, Tstdv, PowerSTDV, numf, leg, TempPowAve_xlab, TempPowAve_ylab, TempPowAve_ptitle)
	


# Output summary csv file
outf = __file__ 
outf = outf[:-3]
outf = outf + '_Summary.csv'
smry.to_csv(outf)

# Show plots
plt.show()