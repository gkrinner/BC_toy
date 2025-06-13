# -*- coding: utf-8 -*-
"""

GK20240827

Toy model 1d, modèle "biaisé" qui devrait converger vers 0 en moyenne mais qui converge vers un biais prescrit.

On fait plusieurs itérations du modèle

"""

import numpy as np

npts = 3

Xini = np.zeros(npts)
Xref = np.zeros(npts)
tauM = 10.0 # constante de temps du modele
tauE = 20.0 # constante de temps de croissance de l'erreur
tauN = 30.0 # constante de temps de la correction
bias0 = np.array([1.0,-1.0,-2.0])

niter = 10
iter = -1

dXdtC = np.zeros(npts)
X = np.zeros(npts)
Xera = np.zeros(npts)
dXdtM = np.zeros(npts)
dXdtE = np.zeros(npts)
dXdtN = np.zeros(npts)
BiaisNudge = np.zeros(npts)

dXdtNm = np.zeros(npts)
dXdtNmOld = np.zeros(npts)

dt = 1.0
nt = 1000

while ( iter <= niter ):

    if ( iter >= 0):

        # nudging phase
        
        BiaisNudge = np.zeros(npts)
        Xera[:] = Xini[:]
        X[:] = Xini[:]
        t = 0.0
        dXdtNmOld[:] = dXdtNm[:]
    
        it = 0
        while ( it < nt ) :
            # time step
            t = t+dt
            it = it+1
            
            # the ideal model, some equations that should give a quasi-stationary solution around 0
            dXdtM[0] = -1.0/tauM * ( X[0] - Xref[0] ) + 0.1*np.arctan( X[0]**2. * X[1] )
            dXdtM[1] = -1.0/tauM * ( X[1] - Xref[1] ) + 0.1*np.arctan( X[0] )
            dXdtM[2] = -1.0/tauM * ( X[2] - Xref[2] ) - 0.1*np.arctan( X[0]+X[2] )
    
            # la reference : "ERA"
            Xera[:] = Xera[:] + dt * dXdtM[:]
            
            # the error tendency
            dXdtE[:] = 1.0/tauE * (bias0[:]-X[:])
        
            # update state variable
            X[:] = X[:] + dt * (dXdtM[:] + dXdtE[:] + + dXdtNmOld[:])
            
            # on nudge
            dXdtN[:] = -1./tauN * (X[:]-Xera[:])
            X[:] = X[:] + dt * dXdtN[:]
            
            # update "climatology" of nudging tendencies
            dXdtNm[:] = dXdtNm[:] + dXdtN[:]/nt

            BiaisNudge[:] = BiaisNudge[:] + (X[:]-Xera[:])/nt

    # bias-corrected run

    Xera[:] = Xini[:]
    X[:] = Xini[:]
    Biais = np.zeros(npts)
    t = 0.0

    it = 0
    while (it < nt ) :
        # time step
        t = t+dt
        it = it+1
        
        # the ideal model, some equations that should give a quasi-stationary solution around 0
        dXdtM[0] = -1.0/tauM * ( X[0] - Xref[0] ) + 0.1*np.arctan( X[0]**2. * X[1] )
        dXdtM[1] = -1.0/tauM * ( X[1] - Xref[1] ) + 0.1*np.arctan( X[0] )
        dXdtM[2] = -1.0/tauM * ( X[2] - Xref[2] ) - 0.1*np.arctan( X[0]+X[2] )

        # la reference : "ERA"
        Xera[:] = Xera[:] + dt * dXdtM[:]
        
        # the error tendency
        dXdtE[:] = 1.0/tauE * (bias0[:]-X[:])
    
        # update state variable
        X[:] = X[:] + dt * (dXdtM[:] + dXdtE[:] + dXdtNm[:])
        
        Biais[:] = Biais[:] + (X[:]-Xera[:])/nt
        
    print()
    print("Iteration : ", iter)
    print("Correction utilisee :", dXdtNm[:])
    print("Biais nudge:", BiaisNudge[:])
    print("Biais :", Biais[:])
    rmse = (np.sum((Biais[:])**2)/npts)**.5
    print("RMSE :",rmse)

    if ( iter > 0 ):
        print("Amélioration du RMSE (%) :", 100*(1.0-np.abs(rmse)/np.abs(oldrmse)))

    oldrmse = rmse
    
    iter = iter+1

print("Fini")
