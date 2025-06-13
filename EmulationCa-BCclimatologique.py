# -*- coding: utf-8 -*-
"""

GK20240827

Toy model 1d, modèle "biaisé" qui devrait converger vers 0 en moyenne mais qui converge vers un biais prescrit.

On fait plusieurs itérations du modèle

"""

import numpy as np
import random

npts = 3

Xref = np.zeros(npts)
tauM = 10.0 # constante de temps du modele
tauE = 6.0 # constante de temps de croissance de l'erreur
tauC = 3.0 # constante de temps de la correction
bias0 = np.array([1.0,-1.0,-2.0])

niter = 0
iter = 0

dXdtC = np.zeros(npts)
Xini = np.zeros(npts)
X = np.zeros(npts)
Xmoy = np.zeros(npts)
XR = np.zeros(npts)
XRmoy = np.zeros(npts)
dXdtM = np.zeros(npts)
dXdtR = np.zeros(npts)
dXdtE = np.zeros(npts)
Bias = np.zeros(npts)

AmpNoise = 0.1

random.seed(10)

dt = 1.0
dXdtC[:] = 0.

for type in ["Adaptation", "ERBC"]:

    print()
    print(type)
    print("----------")
    print()

    nt = 1000
    t = 0.0
    it = 0
    
    Xini[:] = Xref[:]
    X[:] = Xini[:]
    Xmoy[:] = 0.
    XR[:] = Xini[:]
    XRmoy[:] = 0.
    
    while ( it < nt ) :
       # time step
       t = t+dt
       it = it+1
            
       # the ideal model. Some "equations" that should give a quasi-stationary solution around 0
       dXdtM[0] = -1.0/tauM * ( X[0] - Xref[0] ) + AmpNoise*(random.random()-.5)
       dXdtM[1] = -1.0/tauM * ( X[1] - Xref[1] ) + AmpNoise*(random.random()-.5)
       dXdtM[2] = -1.0/tauM * ( X[2] - Xref[2] ) + AmpNoise*(random.random()-.5)
            
       # the error tendency
       dXdtE[:] = 1.0/tauE * bias0[:] * tauE/tauM
        
       # update state variable
       X[:] = X[:] + dt * (dXdtM[:] + dXdtE[:])
            
       # on ajoute la correction
       X[:] = X[:] + dt * dXdtC[:]
    
       # the "reality". Same equations
       dXdtR[0] = -1.0/tauM * ( XR[0] - Xref[0] ) + AmpNoise*(random.random()-.5)
       dXdtR[1] = -1.0/tauM * ( XR[1] - Xref[1] ) + AmpNoise*(random.random()-.5)
       dXdtR[2] = -1.0/tauM * ( XR[2] - Xref[2] ) + AmpNoise*(random.random()-.5)

       XR[:] = XR[:] + dt * dXdtR[:]

       # update "climatologies"
       if ( it == 1 ):
           Xmoy[:] = X[:]
           XRmoy[:] = XR[:]
       else:
           Xmoy[:] = ((it-1)*Xmoy[:] + 1*X[:]) / it
           XRmoy[:] = ((it-1)*XRmoy[:] + 1*XR[:]) / it

       # the mean bias:
       Bias[:] = Xmoy[:] - XRmoy[:]
              
       if ( type == "Adaptation" ):
           # update the correction term
           dXdtC[:] = -1.0/tauC * Bias[:]
           # dXdtC[:] = 0. # converges to prescribed bias if correction set to 0
              
       # some output
       if ( it < 10 ):
         outputfreq=1
       elif ( it < 100 ):
         outputfreq=10
       else:
         outputfreq=100

       if ( np.mod(it,outputfreq) == 0 ):
          print()
          print("Pas de temps : ", it)
          print("Correction utilisee :", dXdtC[:])
          print("Biais :", Bias[:])
          rmse = (np.sum((Bias[:])**2)/npts)**.5
          print("RMSE :",rmse)
        
print("Fini")
