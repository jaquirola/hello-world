import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from math import *

	
#Save data inside array flujo
flujo = loadtxt("datos.txt", float)
Energy = []
lent = len(flujo)
a = lent/100
Erange1 = 6.0
#Create the energy range
for k in range(0,100):
	Erange1 = Erange1 + 0.025
	Energy.append(Erange1)
#define the label of the plots:[open_angle_lower,open_angle_upper,line-of-sight_angle]
parameters = []
for i in range(0,91,10):
	for j in range(0,91,10):
		if (j>i):
			for k in range(0,91,10):
				z = ([i,j,k])
				x = i+j+k
				parameters.append(z)
#Save the data of flujo like a matrix, where each raw is the flux of the state [open_angle_lower,open_angle_upper,line-of-sight_angle]
ima = []
for i in range(0, a):
	ima.append([])
	for j in range(i*100, 100*(i+1)):
		x = flujo[j]
		ima[i].append(x)
#Create an array of 20 images
para = len(parameters)
lent = len(ima)
print lent, para
m = lent/20	
for t in range(22,23):
	fig, ax = plt.subplots(ncols=5,nrows=4,sharex=True,figsize=[7*3,3.5*4])
	i=j=0
	for s in range(t*20, 20*(t+1)):
		ax[j,i].step(Energy,ima[s], '-', lw=3)
		ax[j,i].annotate(parameters[s], xy=(6.42, 0.1))
		fig.patch.set_facecolor('white')
		plt.xlim([6.41,6.85])
		i = i + 1
		if (i>4):
			i = 0
			j = j + 1
	fig.tight_layout()
#	plt.savefig('Imagen' + str(t) + '.eps')
#	plt.clf()	
#	plt.close
	plt.show()
#Ya que no siempre todo puede entrar en arrays de 20 imagenes, hay que crear las ultimas sobrantes

#fig, ax = plt.subplots(ncols=5,nrows=2,sharex=True,figsize=[7*3,3.5*4])
#i=j=0
#for s in range(440, 450):
#	ax[j,i].step(Energy,ima[s], '-', lw=3)
#	ax[j,i].annotate(parameters[s], xy=(6.42, 0.1))
#	fig.patch.set_facecolor('white')
#	plt.xlim([6.41,6.85])
#	i = i + 1
#	if (i>4):
#		i = 0
#		j = j + 1
#fig.tight_layout()
#	plt.savefig('Imagen' + str(t) + '.eps')
#	plt.clf()	
#	plt.close
#plt.show()
