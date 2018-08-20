import math
import numpy as np

def rebinCov(rebin,cov,binWidths=[]):
    '''
    This takes a covariance matrix and returns the covariance matrix after rebinning. The rebin argument is a list of maps: [ (newbin , [ oldbinstocombine ]) ] . If binWidths is specified they are taken into account'''
    n=cov.shape[0]
    if len(binWidths)==0:
        bw=[1]*n
    else:
        if len(binWidths)!=n:
            raise ValueError("bin width has to have the esame length as covariance matrix!")
        bw=binWidths
    newSize=len([r for r in rebin if r[0]!=None])
    rebinMatrix=np.zeros((newSize,n))
    for i,js in rebin:
        if i!=None:
            newWidth=sum([bw[jj] for jj in js])
            for j in js:
                rebinMatrix[i,j]=bw[j]/float(newWidth)

    return np.dot(np.dot(rebinMatrix,cov),rebinMatrix.transpose())


def rebinCovLR(rebinL,rebinR,cov,binWidthsL=[],binWidthsR=[]):
    '''
    This takes a covariance-like matrix (normally a part of the covariance matrix) and returns the covariance matrix after rebinning, with a different rebinning from the left and the right. The rebin arguments is a list of maps: [ (newbin , [ oldbinstocombine ]) ] . If binWidths is specified they are taken into account'''
    nL=cov.shape[0]
    nR=cov.shape[1]
    if len(binWidthsL)==0:
        bwL=[1]*nL
    else:
        if len(binWidthsL)!=nL:
            raise ValueError("bin width has to have the same length as covariance matrix!")
        bwL=binWidthsL

    if len(binWidthsR)==0:
        bwR=[1]*nR
    else:
        if len(binWidthsR)!=nR:
            raise ValueError("bin width has to have the same length as covariance matrix!")
        bwR=binWidthsR


    newSizeL=len([r for r in rebinL if r[0]!=None])
    newSizeR=len([r for r in rebinR if r[0]!=None])
    rebinMatrixL=np.zeros((newSizeL,nL))
    rebinMatrixR=np.zeros((newSizeR,nR))
    for i,js in rebinL:
        if i!=None:
            newWidthL=sum([bwL[jj] for jj in js])
            for j in js:
                rebinMatrixL[i,j]=bwL[j]/float(newWidthL)
    for i,js in rebinR:
        if i!=None:
            newWidthR=sum([bwR[jj] for jj in js])
            for j in js:
                rebinMatrixR[i,j]=bwR[j]/float(newWidthR)

    return np.dot(np.dot(rebinMatrixL,cov),rebinMatrixR.transpose())


def rebinVector(rebin,vec,binWidths=[]):
    '''
    This takes a vector and returns the vector after rebinning. The rebin argument is a list of maps: [ (newbin , [ oldbinstocombine ]) ]. It is provided to match the rebinCov procedure '''
    n=len(vec)
    if len(binWidths)==0:
        bw=[1]*n
    else:
        if len(binWidths)!=n:
            raise ValueError("bin widths has to have the same length as covariance matrix!")
        bw=binWidths
    
 
    newSize=len([r for r in rebin if r[0]!=None])
    
    rebinVector=np.zeros(newSize)
    for i,js in rebin:
        newWidth=0.0
        for j in js:
            rebinVector[i]+=vec[j]*bw[j]
            newWidth+=bw[j]
        rebinVector[i]=rebinVector[i]/newWidth
    return rebinVector



def rebinBinWidth(rebin,binWidths):
    '''
    This takes a vector of binWidths and returns the binWidths after rebinning. The rebin argument is a list of maps: [ (newbin , [ oldbinstocombine ]) ]. It is provided to match the rebinCov procedure '''
    n=len(binWidths)
    bw=binWidths
    
 
    newSize=len([r for r in rebin if r[0]!=None])
    
    rebinVector=np.zeros(newSize)
    for i,js in rebin:
        newWidth=0.0
        for j in js:
            newWidth+=binWidths[j]
        rebinVector[i]=newWidth
    return rebinVector


def rebinBinCenter(rebin,vec,binWidths):
    '''
    This takes the bin centers and returns the bin centers after rebinning. The rebin argument is a list of maps: [ (newbin , [ oldbinstocombine ]) ]. It is provided to match the rebinCov procedure '''
    n=len(vec)
    if len(binWidths)!=n:
        raise ValueError("bin widths has to have the same length as bin enter list!")
    bw=binWidths
    
 
    newSize=len([r for r in rebin if r[0]!=None])
    
    rebinVector=np.zeros(newSize)
    for i,js in rebin:
        left=vec[js[0]]-0.5*binWidths[js[0]]
        newWidth=0.0
        for j in js:
            rebinVector[i]+=vec[j]*binWidths[j]
            newWidth+=binWidths[j]
        rebinVector[i]=left+0.5*newWidth
    return rebinVector




def rebinHist(rebin,h):
    '''
    This takes a histogram and returns a vector of bin values after rebinning, taking the bin width into account. The rebin argument is a list of maps: [ (newbin , [ oldbinstocombine ]) ]. It is provided to match the rebinCov procedure '''
    h_binValues=[h.GetBinContent(ii) for ii in range(1,h.GetNbinsX())]
    h_binWidths=[h.GetBinWidth(ii) for ii in range(1,h.GetNbinsX())]
    n=len(h_binValues)
    newSize=len(rebin)
    rebinVector=np.zeros(newSize)
    for i,js in rebin:
        newWidth=0.0
        for j in js:
            newWidth+=h_binWidths[j]
            rebinVector[i]+=h_binValues[j]*h_binWidths[j]
        rebinVector[i]=rebinVector[i]/newWidth

    return rebinVector



def shift(r,s1,s2):
    '''
    this shifts the bin description, the index is shifted by s1, the bin entries by s2. They need 
    to be different because ignored bins.
    for example 
    shift( [ (1,[1,2]),(2,[3,4]), (None,[5,6]) ] , 3 , 10 ) --> [ (4,[11,12]),(5,[13,14]), (None,[15,16]) ] 
    
    '''
    def shiftBinNbr(i,shift):
        if i!=None:
            return i+shift
        else:
            return None
    return [(shiftBinNbr(i,s1),[rr+s2 for rr in b]) for i,b in r ]

def combine(*rs):
    '''
    this combines different rebinning descriptions into one
    for example 
    combine([ (0,[0,1,2,3]),(1,[4,5,6])] , [ (None,[1,2,3,4,5,6,7,8,9]),(0,[10,11,12])]   )
     -->
    [(0, [0, 1, 2, 3]),
    (1, [4, 5, 6]),
    (None, [8, 9, 10, 11, 12, 13, 14, 15, 16]),
    (2, [17, 18, 19])]
    note that the None bins are kept
    '''
    result=[]
    for r in rs:
        validBins=[rr[0] for rr in result if rr[0]!=None]
        s1=len(validBins)
        if result:
            s2=result[-1][1][-1]+1
        else:
            s2=0
        result.extend(shift(r,s1,s2))
    return result


