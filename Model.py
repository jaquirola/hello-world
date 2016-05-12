from astropy.io import fits
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from math import *
import time

def my_range(start, end, step):
    while start <= end:
        yield start
        start = start + step
#Define the parameters
energy = 6.7
aopenl = 0
aopenu = 90
alos = 0
vmax = 5000
#Crate the flux array
photar = []
for t in my_range(0.1,50,0.01):	
	x = 0	
	photar.append(x)
ear = []
for t in my_range(0.1,50,0.01):	
	ear.append(t)
#Condition to the angles
if (aopenl > aopenu):
        tmp1=aopenu
        aopenu=aopenl
        aopenl=tmp1
vrel = vmax/300000.
gamma = (1/(1-vrel**2))**0.5
dera = 0.017453293
#Define the dimension of the array
ne = len(ear)

#Angular resolution
#Angular step
phinum = 10
thetanum = 10
#Angular limits
theta0 = -90+thetanum/2
theta1 = 0-thetanum/2
phi0 = 90+phinum/2
phi1 = 270-phinum/2
#Energy limits
Emin = energy/(1.+vrel)/gamma
Emax = energy/(1.-vrel)/gamma

zpbin2 = 0
zpbin1 = 0
for theta in my_range (theta0,theta1,thetanum):
	if (((theta >= 0-aopenu) and (theta <= 0-aopenl))or((theta >= 0+aopenl) and (theta <= 0+aopenu))):
		rtheta = float(theta)
		for phi in my_range (phi0, phi1, phinum):
			rphi = float(phi)
			y=cos(dera*rtheta)*sin(dera*rphi)
          		yu1=cos(dera*(rtheta+thetanum/2.))*sin(dera*(rphi+phinum/2.))
          		yu2=cos(dera*(rtheta+thetanum/2.))*sin(dera*(rphi-phinum/2.))
          		yl1=cos(dera*(rtheta-thetanum/2.))*sin(dera*(rphi+phinum/2.))
          		yl2=cos(dera*(rtheta-thetanum/2.))*sin(dera*(rphi-phinum/2.))
          		z=sin(dera*rtheta)
          		zu=sin(dera*(rtheta+thetanum/2.))
          		zl=sin(dera*(rtheta-thetanum/2.))
          		dE=cos(dera*rtheta)*dera*dera*float(thetanum*phinum)
         	        zp=z*cos(dera*alos)+y*sin(dera*alos)
		        zpu=zu*cos(dera*alos)+max(yu1,yu2,yl1,yl2)*sin(dera*alos)
		        zpl=zl*cos(dera*alos)+min(yu1,yu2,yl1,yl2)*sin(dera*alos)
			if (zpu < zpl):
				tmp1 = zpu
				zpu = zpl
				zpl = tmp1
			if (zpl < -1):
				zpl = -1
			if (zpu > 1):
				zpu = 1
			subang_tot=(acos(zpl)-acos(zpu))/dera
          		Emin=energy/(1.+zpu*vrel)/gamma
          		Emax=energy/(1.+zpl*vrel)/gamma
			iel=1
          		ieh=ne-1
			
			for ie in range (iel, ieh):
				if ((ear[ie+1] >= Emin) and (ear[ie] < Emax)):
					if (ear[ie] <= Emin): 
             					zpbin1=(energy-Emin*gamma)/Emin/vrel/gamma
             					iel=ie
            				else:
            					zpbin1=(energy-ear[ie]*gamma)/ear[ie]/vrel/gamma            				
            				if (zpbin1 < -1):
             					zpbin1=-1
            				elif (zpbin2 < -1):
             					zpbin2=-1
            				
            				if (ear[ie+1] > Emax):
             					zpbin2=(energy-Emax*gamma)/Emax/vrel/gamma
             					ieh=ie+2
            				else:
             					zpbin2=(energy-ear[ie+1]*gamma)/ear[ie+1]/vrel/gamma  				
            				if (ieh > ne-1):
             					ieh=ne-1            		
            				if (zpbin1 > 1):
             					zpbin1=1
            				elif (zpbin2 > 1):
             					zpbin2=1
            				subang_bin=(acos(zpbin2)-acos(zpbin1))/dera
            				Eweight=subang_bin/subang_tot
					photar[ie]=photar[ie]+2*dE*Eweight
                        #Mirror flux
			zp=zp*(-1)
          		tmp1=zpu
          		zpu=zpl*(-1)
          		zpl=tmp1*(-1)
			subang_tot=(acos(zpl)-acos(zpu))/dera
          		Emin=energy/(1.+zpu*vrel)/gamma
          		Emax=energy/(1.+zpl*vrel)/gamma
          		iel=1
          		ieh=ne-1			
			for ie in range (iel, ieh):
				if ((ear[ie+1] >= Emin) and (ear[ie] < Emax)):
					if (ear[ie] <= Emin):
             					zpbin1=(energy-Emin*gamma)/Emin/vrel/gamma
             					iel=ie
            				else:
             					zpbin1=(energy-ear[ie]*gamma)/ear[ie]/vrel/gamma
            				if (zpbin1 < -1):
             					zpbin1=-1
            				elif (zpbin1 > 1):
             					zpbin1=1

            				if (ear[ie+1] > Emax):
             					zpbin2=(energy-Emax*gamma)/Emax/vrel/gamma
             					ieh=ie+2
            				else:
             					zpbin2=(energy-ear[ie+1]*gamma)/ear[ie+1]/vrel/gamma
            				if (ieh > ne-1):
             					ieh=ne-1
            				if (zpbin2 < -1):
             					zpbin2=-1
            				elif (zpbin2 > 1):
             					zpbin2=1
            				subang_bin=(acos(zpbin2)-acos(zpbin1))/dera
            				Eweight=subang_bin/subang_tot
					photar[ie]=photar[ie]+2*dE*Eweight
#To normalize the flux
suma = 0
for ie in range(1, ne):
	suma = suma + photar[ie]
if (suma > 0):
	for ie in range(1, ne):
		photar[ie] = photar[ie]/suma

#print len(photar), len(ear)
plt.step(ear, photar, '-', color = 'r')
plt.xlabel('Energy(KeV)')
plt.ylabel('Photons cm$^{-2}$s$^{-1}$KeV$^{-1}$')
plt.legend(loc = 'upper left')
#plt.title('Funcion de distribucion acumulativa')
plt.show()
