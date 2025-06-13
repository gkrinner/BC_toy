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
tauE = 20.0 # constante de temps de croissance de l'erreur
tauC = 30.0 # constante de temps de la correction
bias0 = np.array([1.0,-1.0,-2.0])

random.seed(10)

niter = 10
iter = 0

dXdtC = np.zeros(npts)
Xini = np.zeros(npts)
X = np.zeros(npts)
Xmoy = np.zeros(npts)
dXdtM = np.zeros(npts)
dXdtE = np.zeros(npts)

while ( iter <= niter ):
    
    t = 0.0
    dt = 1.0
    nt = 1000
    Xini[:] = Xref[:]
    
    X[:] = Xini[:]
    Xmoy = np.zeros(npts)
    it = 0
    while ( it < nt ) :
        # time step
        t = t+dt
        it = it+1
        
        # the ideal model, some equations that should give a quasi-stationary solution around 0
        dXdtM[0] = -1.0/tauM * ( X[0] - Xref[0] ) + 0.1*(random.random()-.5)
        dXdtM[1] = -1.0/tauM * ( X[1] - Xref[1] ) + 0.1*(random.random()-.5)
        dXdtM[2] = -1.0/tauM * ( X[2] - Xref[2] ) + 0.1*(random.random()-.5)

        # the error tendency
        dXdtE[:] = 1.0/tauE * bias0[:]*(tauE/tauM)
    
        # update state variable
        X[:] = X[:] + dt * (dXdtM[:] + dXdtE[:])
        
        # on ajoute la correction
        X[:] = X[:] + dt * dXdtC[:]
        
        # update "climatology"
        Xmoy[:] = Xmoy[:] + X[:]
    
    Xmoy[:] = Xmoy[:]/nt
    print()
    print("Iteration : ", iter)
    print("Correction utilisee :", dXdtC[:])
    print("Biais :", Xmoy[:]-Xref[:])
    rmse = (np.sum((Xmoy[:]-Xref[:])**2)/npts)**.5
    print("RMSE :",rmse)

    if ( iter > 0 ):
        print("Amélioration du RMSE (%) :", 100*(1.0-np.abs(rmse)/np.abs(oldrmse)))

    oldrmse = rmse
    
    # update bias correction: the reference value is Xref
    dXdtC[:] = dXdtC[:] -1.0/tauC * (Xmoy[:]-Xref[:])
    print("Nouvelle correction :", dXdtC[:])
    
    iter = iter+1

print("Fini")
