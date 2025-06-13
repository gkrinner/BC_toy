# -*- coding: utf-8 -*-
"""

GK20240827

Toy model 1d, modèle "biaisé" qui devrait converger vers 0 en moyenne mais qui converge vers un biais prescrit.

On fait plusieurs itérations du modèle

"""

import numpy as np
import random

npts = 3

Xini = np.zeros(npts)
Xref = np.zeros(npts)
tauM = 10.0 # constante de temps du modele
tauE = 6.0 # constante de temps de croissance de l'erreur
tauN = 3.0 # constante de temps de la correction
bias0 = np.array([1.0,-1.0,-2.0])

AmpNoise = 0.1

random.seed(10)

niter = 10
iter = -1

dXdtC = np.zeros(npts)
X = np.zeros(npts)
XR = np.zeros(npts)
dXdtM = np.zeros(npts)
dXdtR = np.zeros(npts)
dXdtE = np.zeros(npts)
dXdtN = np.zeros(npts)
BiaisNudge = np.zeros(npts)
Biais = np.zeros(npts)

dXdtNm = np.zeros(npts)
dXdtNmOld = np.zeros(npts)

dt = 1.0
nt = 1000

while ( iter <= niter ):

  for type in ["Adaptation", "ERBC"]:

    if ( iter >= 0 ) or ( type == "ERBC" ):

        if ( type == "Adaptation"):
            BiaisNudge = np.zeros(npts)
        else:
            Biais = np.zeros(npts)

        XR[:] = Xini[:]
        X[:] = Xini[:]
        t = 0.0

        if ( type == "ERBC"):
            dXdtNmOld[:] = dXdtNm[:]
    
        it = 0
        while ( it < nt ) :
            # time step
            t = t+dt
            it = it+1
            
            # the ideal model, some equations that should give a quasi-stationary solution around 0
            dXdtM[0] = -1.0/tauM * ( X[0] - Xref[0] ) + AmpNoise*(random.random()-.5)
            dXdtM[1] = -1.0/tauM * ( X[1] - Xref[1] ) + AmpNoise*(random.random()-.5)
            dXdtM[2] = -1.0/tauM * ( X[2] - Xref[2] ) + AmpNoise*(random.random()-.5)
            
            # the error tendency
            dXdtE[:] = 1.0/tauE * (bias0[:]-X[:])
        
            # update state variable
            X[:] = X[:] + dt * (dXdtM[:] + dXdtE[:] + dXdtNmOld[:])

            # la realite: same equations
            dXdtR[0] = -1.0/tauM * ( XR[0] - Xref[0] ) + AmpNoise*(random.random()-.5)
            dXdtR[1] = -1.0/tauM * ( XR[1] - Xref[1] ) + AmpNoise*(random.random()-.5)
            dXdtR[2] = -1.0/tauM * ( XR[2] - Xref[2] ) + AmpNoise*(random.random()-.5)
            XR[:] = XR[:] + dt * dXdtR[:]
            
            if ( type == "Adaptation" ):

                # on nudge
                dXdtN[:] = -1./tauN * (X[:]-XR[:])
                X[:] = X[:] + dt * dXdtN[:]
            
                # update "climatology" of nudging tendencies
                dXdtNm[:] = dXdtNm[:] + dXdtN[:]/nt

                BiaisNudge[:] = BiaisNudge[:] + (X[:]-XR[:])/nt

            else:

                Biais[:] = Biais[:] + (X[:]-XR[:])/nt
    
        
  print()
  print("Iteration : ", iter)
  print("Correction utilisee :", dXdtNm[:])
  print("Biais nudge:", BiaisNudge[:])
  print("Biais :", Biais[:])
  rmse = (np.sum((Biais[:])**2)/npts)**.5
  print("RMSE :",rmse)

  if ( iter > 0 ):
    print("Amélioration du RMSE // dernier (%) :", 100*(1.0-np.abs(rmse)/np.abs(oldrmse)))

  oldrmse = rmse
    
  iter = iter+1

print("Fini")
