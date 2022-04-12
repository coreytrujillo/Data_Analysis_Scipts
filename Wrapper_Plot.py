from DataAnalysis_Functions import *
import matplotlib.pyplot as plt
from math import pi
import numpy as np

fpath = './220313_FiberBenchmark_data.csv'

datestr = '220313'

PlotFilter = 1

lbl = ['Fiber A Before Cleaning', 'Fiber A After Cleaning','Fiber B', 'Fiber C', 'Fiber D Backwards', 'Fiber E']

tistr = ['12:33:00', '12:40:00', '13:08:00', '13:39:00', '14:21:00', '14:50:00']

tfstr = ['12:38:00','12:45:00', '13:18:00', '13:52:00', '14:30:00', '14:58:00']

################################
# Don't change anything below this line
################################

# Grab data
data = data_read_format(fpath, datestr)
dc = data.columns
print('Data Headers:\n', dc)
figi = 1 # Figure iterator

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

if 'TC1' in dc:
	plt.figure(figi)
	figi += 1
	plt.title(datestr + ' Ambient Temperature')
	plt.xlabel('Time (MDT)')
	plt.ylabel('Temperature ($^\circ$C)')
	plt.scatter(data['Time'], data['TC1'])
	
	if PlotFilter == 1:
		for i in range(0, len(lbl)):
			dataf = data_filter(data, datestr, tistr[i], tfstr[i])
			
			plt.scatter(dataf['Time'], dataf['TC1'])
			
		plt.legend(['Unfiltered'] + lbl)
		
Ac = pi*0.6**2/4		
if ('PyrE' in dc) & ('Power' in dc) & (PlotFilter == 1):
	plt.figure(figi)
	figi += 1
	[spx, spy] = subcount(len(lbl))
	for i in range(0, len(lbl)):
		dataf = data_filter(data, datestr, tistr[i], tfstr[i])
		PowerAve = dataf['Power'].mean()
		PyrAve = dataf['PyrE'].mean()*Ac
		EffAve = PowerAve/PyrAve
		plt.subplot(spx, spy, i+1)
		plt.scatter(dataf['PyrE']*Ac, dataf['Power'])
		plt.xlabel('Power In [W]')
		plt.ylabel('Power Out [W]')
		plt.title(lbl[i] + ' | Ave Eff: ' +  '{:.4f}'.format(EffAve))
		plt.suptitle(datestr + ' Power Input vs Power Output')

if ('Power' in dc) & (PlotFilter == 1):
	plt.figure(figi)
	figi += 1
	[spx, spy] = subcount(len(lbl))
	for i in range(0, len(lbl)):
		dataf = data_filter(data, datestr, tistr[i], tfstr[i])
		plt.subplot(spx, spy, i+1)
		plt.scatter(dataf['Time'], dataf['Power'])
		PowerAve = dataf['Power'].mean()
		PyrAve = dataf['PyrE'].mean()*Ac
		EffAve = PowerAve/PyrAve
		print(lbl[i], 'Power Average: \t', PowerAve)
		print(lbl[i], 'Pyr Average: \t', PyrAve)
		print(lbl[i], 'Ave eff:  \t', EffAve)
		print(lbl[i], 'Data count: \t', dataf['Power'].size)
		plt.scatter(dataf['Time'], dataf['PyrE']*EffAve*Ac)
		plt.xlabel('Time [MDT]')
		plt.ylabel('Power Output [W]')
		titlestr = lbl[i] + ' | Ave Eff: ' + '{:.4f}'.format(EffAve)
		plt.title(titlestr)
		plt.suptitle(datestr + ' Measured Power Output and Estimated Power Output')
		plt.legend(['Power Output'], ['Est. Power from Pyr'])

plt.show()