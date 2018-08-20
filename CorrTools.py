import numpy as np
import math

def safeCorr(c,ii,jj):
    '''
    normalises the ii,jj element of a matrix by the square root of the corresonding diagonal elements
    '''
    if c[ii,ii]==0 or c[jj,jj]==0:
        return 0
    else:
        return c[ii,jj]/math.sqrt(c[ii,ii])/math.sqrt(c[jj,jj])

def checkSymm(c):
    for ii in range(len(c)):
        for jj in range(ii+1,len(c)):
            if c[ii,jj]!=c[jj,ii]:
                return False
    return True

def makeCorrFromCov(c):
    corr=np.array([ [safeCorr(c,ii,jj) for jj in range(len(c)) ] for ii in range(len(c)) ])
    return corr

def rescaleCov(c,v):
    if len(c)!=len(v):
        raise ValueError
    rescaled=np.array([ [c[ii,jj] *v[ii]*v[jj] for jj in range(len(c)) ] for ii in range(len(c)) ])
    return rescaled

if __name__=="__main__":
    import random
    n=10
    # build a andom covariance matrix as a sum of purely correlated errors 
    ee=np.zeros((n,n))
    for _ in range(5):
        e=np.array([[random.random()-0.5 for _ in range(n)]])
        ee=ee+np.dot(e.transpose(),e)
        
    dia=[math.sqrt(ee[ii,ii]) for ii in range(n) ]
    corr=makeCorrFromCov(ee)
    print corr 
    print rescaleCov(corr,dia)-ee
