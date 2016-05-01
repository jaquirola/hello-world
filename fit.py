from astropy.io import fits
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from math import *

#Open file shell.fits	
hdulist = fits.open('shell.fits', mode='update')
#Save in an array the primary extension
tbdata0 = hdulist[0].data
#Save in an array the parameters extension
tbdata1 = hdulist[1].data
#Save in an array the energy extension
tbdata2 = hdulist[2].data
#Save in an array the spectrum extension
tbdata3 = hdulist[3].data
#We can call a sub-array with this syntaxis: tbdata1[0]
#We can call a sub-sub-array with the syntaxis: tbdata1[0][1]

#We should define the number of elements of each parameter
maxi = []
for i in range (0,5,1):
#We define the number of elements like abs(min-max)/delta
	x = abs(tbdata1[i][4]-tbdata1[i][6])/tbdata1[i][3]
	tbdata1[i][8] = x
	maxi.append(x)
#Numvalues' maximun
maximo = max(maxi)
#Add elements to the Values column
for i in range (0,5,1):
	suma = tbdata1[i][4]
	k=0
	while (k<maximo):
		if (k<tbdata1[i][8]):
#We consider the initial value and the accumulative sum
			suma = suma + tbdata1[i][3]
#Store the elements inside each array for parameters
			tbdata1[i][9][k] = suma
		else:
			tbdata1[i][9][k] = 0
		k = k + 1	
#We ought to define the energy bins array,
#First, we should fix the low energy and high energy bins range
#E = (0.1;50)KeV
low_energy = 0.1
high_energy = 50
size = 0.1
#With this result, we built the number of rows in the Energy extension
bin_size = (high_energy-low_energy)/size
#tbdata2[][] take one energy bin
#We store the energy bin in an array in the energy extension
i = 0
while (i <= bin_size):		
	tbdata2[i][0] = low_energy
	tbdata2[i][1] = high_energy
	low_energy = high_energy
	high_energy = high_energy + size
	i = i + 1

#print tbdata3[0]
#We find the dimenion for the PARAMVAL column
size = 1
for i in range (0,5,1):
	size = size * tbdata1[i][8]
#The next code lines add parameter values to the spectrum extension
#We extract the values of parameters extensions and include in the 
#spectrum extension 
a = 0
j = 0
t = 0
#Open angle lower
while (j < tbdata1[0][8]):
	k = 0
#Open angle upper$$$$$$$$$$$$$$$$$$$$$$$$$$
	while (k < tbdata1[1][8]):
		l = 0
#Line/of/sight angle$$$$$$$$$$$$$$$$$$$$$$$
		while (l < tbdata1[2][8]):
			m = 0	
#Line energy$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
			while (m < tbdata1[3][8]):
				n = 0
#Velocity$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
				while (n < tbdata1[4][8]):
					t = a
					while (t<size):
						tbdata3[t][0][0] = tbdata1[0][4] + (j * tbdata1[0][3])
						tbdata3[t][0][1] = tbdata1[1][4] + (k * tbdata1[1][3])
						tbdata3[t][0][2] = tbdata1[2][4] + (l * tbdata1[2][3])
						tbdata3[t][0][3] = tbdata1[3][4] + (m * tbdata1[3][3])
						tbdata3[t][0][4] = tbdata1[4][4] + (n * tbdata1[4][3])
						a = a + 1
						break
					n = n + 1
				m = m + 1
			l = l + 1
		k = k + 1
	j = j + 1
hdulist.close()
hdulist.flush()
