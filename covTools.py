import os
# Start dirty hack. To remove the annoying [?1034h character
os.environ['TERM'] = 'linux'
# End of hack.

import math
import ROOT
import HistogramTools as HT
import numpy as np
import re

# these used to be in this file so i import them to ensure compatibility
from rebinTools import *

def printMatrix(M,name):
    n,m=M.shape
    #print n,m
    print "%s = {" % name
    for i in range(n-1):
        print "{",
        for j in range(m-1):
            print ("%e," % M[i,j]),
        print "%e}," % M[i,m-1] 
    print "{",
    for j in range(m-1):
        print ("%e," % M[n-1,j]),
    print "%e}" % M[n-1,m-1] 
    print "};"        

def printMatrixForMathematica(M,name):
    n,m=M.shape
    #print n,m
    os=''
    os=os+( "%s = {\n" % name)
    for i in range(n-1):
        os=os+ "{"
        for j in range(m-1):
            os=os+("%e," % M[i,j])
        os=os+ ("%e},\n" % M[i,m-1]) 
    os=os+ "{"
    for j in range(m-1):
        os=os+ ("%e," % M[n-1,j])
    os=os+ ("%e}\n" % M[n-1,m-1]) 
    os=os+ "};\n"
    return re.sub('e([+-]\d\d)',r' 10^(\1)',os)




def printCov(process,name,parts):
    matrices=[]
    matricesE=[]
    for p in parts:
        f=ROOT.TFile("%s/histograms_%s.root" % (process,p) )
        h=f.Get("h_pt_lastj_cumul_Orig")
        nbins=h.GetNbinsX()
        N=h.getNbrEvents()
        sumOfSquares=[]
        averages=[]

        for ibin in range(nbins+2):
            binWidth=h.GetBinWidth(ibin)
            err=h.GetBinError(ibin)*binWidth
            val=h.GetBinContent(ibin)*binWidth
            sumOfSquares.append(N*(N-1)*err*err +N*val*val)
            averages.append(val)


        def covCoeff(i,j):
            return (sumOfSquares[max(i,j)]/N -averages[i]*averages[j])/sigmas[i]/sigmas[j]
        def cov(i,j):
            return (sumOfSquares[max(i,j)]/N -averages[i]*averages[j])
        def coverr(i,j):
            return (sumOfSquares[max(i,j)]/N -averages[i]*averages[j])/N

        sigmas=[ math.sqrt(ss/N-av*av) for ss,av in zip(sumOfSquares,averages) ]

        M=np.matrix([ [cov(i,j) for i in range(nbins+2)] for j in range(nbins+2)])
        ME=np.matrix([ [coverr(i,j) for i in range(nbins+2)] for j in range(nbins+2)])
        matrices.append(M)
        matricesE.append(ME)
    S=sum(matrices)
    SE=sum(matricesE)
    sigmas=[ math.sqrt(S[i,i]) for i in range(nbins+2) ]
    printMatrix(S,'cov["%s"]' % name)
    
    C=np.matrix([[S[i,j]/sigmas[i]/sigmas[j] for i in range(nbins+2)] for j in range(nbins+2) ])

    printMatrix(C,'corrcoeffs["%s"]' % name)
    printMatrix(SE,'coverr["%s"]' % name)

    return S,C,SE
 

# this gets the covariance matrix for a distibution that was collected
# using the "Cov" switch, that is that contains the full covariance info.
# it is better than the one above

def getCovariance(process,parts,histogram,suffix='',normalizeByBinWidth=False,useNcount=False):
    matrices=[]
    matricesE=[]
    n=0
    for p in parts:
        f=ROOT.TFile("%s/histograms_%s.root" % (process,p) )
        if suffix:
            histname="%s_cov_%s" %(histogram,suffix)
        else:
            histname=histogram
        h=f.Get(histname)
        nbins=h.GetNbinsX()
        n=nbins+2
        N=h.getNbrEvents()
        sumOfSquares=[]
        averages=[]
        errs=[]
        for ibin in range(nbins+2):

            es=[]
            # this is to take the ncount into account, it is
            # one for old ntuples
            binWidthi=h.GetBinWidth(ibin)
            if useNcount:
                a,b=h.getCov(ibin,ibin)/N,h.GetBinContent(ibin)*h.GetBinContent(ibin)*binWidthi*binWidthi
                ee=h.GetBinError(ibin)*binWidthi*math.sqrt(N)
                if b!=0:
                    ncountratio=(a-ee**2)/b
                    print ncountratio
                else :
                    ncountratio=1
            else :
                ncountratio=1
            # this should always give the same answer
            #print ncountratio
            for jbin in range(nbins+2):
                binWidthj=h.GetBinWidth(jbin)
                value=(h.getCov(ibin,jbin)/N-h.GetBinContent(ibin)*h.GetBinContent(jbin)*binWidthi*binWidthj*ncountratio)/N
                if normalizeByBinWidth:
                    value=value/(binWidthi*binWidthj)
                es.append(value)
            #err=h.GetBinError(ibin)*binWidth
            #es[ibin]=err*err
            errs.append(es)
            
        M=np.matrix(errs)    
        matrices.append(M)

    return sum(matrices)


def getCovForCumul(process,parts,histogram,suffix):
    S=getCovariance(process,parts,histogram,suffix)
    A=np.matrix([[ 0 if i<j else 1 for i in range(n) ] for j in range(n) ])
    C=A*S*(A.transpose())
    return C,S

#this gives the covariance matrix for the cumulative  distribution
def getCovNew(process,parts):
    matrices=[]
    matricesE=[]
    n=0
    for p in parts:
        f=ROOT.TFile("%s/histograms_%s.root" % (process,p) )
        h=f.Get("h_pt_lastj_cov_Orig")
        nbins=h.GetNbinsX()
        n=nbins+2
        N=h.getNbrEvents()
        sumOfSquares=[]
        averages=[]
        errs=[]
        for ibin in range(nbins+2):
            es=[]
            binWidth=h.GetBinWidth(ibin)
            for jbin in range(nbins+2):
                es.append((h.getCov(ibin,jbin)/N-h.getWgt(ibin)*h.getWgt(jbin)/N/N)/N)
            #err=h.GetBinError(ibin)*binWidth
            #es[ibin]=err*err
            errs.append(es)
            
        M=np.matrix(errs)    
        matrices.append(M)

    S=sum(matrices)
    
    A=np.matrix([[ 0 if i<j else 1 for i in range(n) ] for j in range(n) ])
    
    C=A*S*(A.transpose())

    return C,S


def printCovNew(process,name,parts):
    C,S=getCovNew(process,parts)
    printMatrix(C,'c["%s"]' % name)
    
    return C,S








def getCovariance2D(directory,parts,histogram,suffix='',normalizeByBinWidth=False):
    matrices=[]
    matricesE=[]
    n=0
    for p in parts:
        f=ROOT.TFile("%s/histograms_%s.root" % (directory,p) )
        if suffix:
            histname="%s_cov_%s" %(histogram,suffix)
        else:
            histname=histogram
        h=f.Get(histname)
        nbinsX=h.GetNbinsX()
        nbinsY=h.GetNbinsY()
        
        n=nbinsX+2+nbinsY+2
        N=h.getNbrEvents()
        sumOfSquares=[]
        averages=[]
        errs=[]
        weightsX=[sum([h.GetBinContent(i,j)*h.GetYaxis().GetBinWidth(j) for j in range(nbinsY+2)]) for i in range(nbinsX+2)]
        weightsY=[sum([h.GetBinContent(i,j)*h.GetXaxis().GetBinWidth(i) for i in range(nbinsX+2)]) for j in range(nbinsY+2)]

        for ibin in range(n):
            es=[]
            if ibin<nbinsX+2:
                binWidthi=h.GetXaxis().GetBinWidth(ibin)
                weighti=weightsX[ibin]*binWidthi
            else:
                binWidthi=h.GetYaxis().GetBinWidth(ibin-nbinsX-2)
                weighti=weightsY[ibin-nbinsX-2]*binWidthi
                
            for jbin in range(n):
                if jbin<nbinsX+2:
                    binWidthj=h.GetXaxis().GetBinWidth(jbin)
                    weightj=weightsX[jbin]*binWidthj
                else:
                    binWidthj=h.GetYaxis().GetBinWidth(jbin-nbinsX-2)
                    weightj=weightsY[jbin-nbinsX-2]*binWidthj
                
                value=(h.getCov(ibin,jbin)/N-weighti*weightj)/N
                #if ibin==jbin:
                #    print ibin,value,h.getCov(ibin,jbin)/N
                if normalizeByBinWidth:
                    value=value/(binWidthi*binWidthj)
                es.append(value)
            #err=h.GetBinError(ibin)*binWidth
            #es[ibin]=err*err
            errs.append(es)
            
        M=np.matrix(errs)    
        matrices.append(M)

    return sum(matrices)



if __name__=="__main__":
    import ROOT
    f=ROOT.TFile('/home/daniel/ntuplesSample/Zee2j7TeV/born/histograms_born.root')
    h=f.Get('h_pt_j1_Orig')
    hb=f.Get('h_pt_j1b_Orig')
    h2=f.Get('h2_pt_y_j1_Orig')
    hy=f.Get('h_yabs_Orig')
    xs=f.Get('xsection_Orig')
    xsectionError=xs.GetBinError(1)
    
    
    
    
    cx=getCovariance('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h_pt_j1_Orig')
    cy=getCovariance('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h_yabs_Orig')
    cxb=getCovariance('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h_pt_j1b_Orig')

    v=np.array([[1]*(h.GetNbinsX()+2)])
    
    ematrix=np.dot(v,np.dot(cx,v.transpose()))
    e=math.sqrt(ematrix.getA()[0,0])

    print e/xsectionError
    
    cxn=getCovariance('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h_pt_j1_Orig',normalizeByBinWidth=True)
    
    binWidths=np.array([h.GetBinWidth(i) for i in range(h.GetNbinsX()+2)])
    norm=sum(binWidths[1:-1])
    v=np.array([binWidths])
    
    
    ematrix=np.dot(v,np.dot(cxn,v.transpose()))
    e=math.sqrt(ematrix.getA()[0,0])

    print e/xsectionError
    

    A=np.array([
        [1]+[0]*32,
        [0]+[1,1]+[0]*30,
        [0,0,0,1]+[0]*29,
        [0,0,0,0,1,1]+[0]*27,
        [0,0,0,0,0,0,1,1]+[0]*25
    ] +[ [0]*i+[1]+[0]*(32-i) for i in range(8,33) ])



    
    cxb=getCovariance('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h_pt_j1b_Orig')
    cxbrec=np.dot(np.dot(A,cx),A.transpose())
    print max([max(row) for row in ((cxb-cxbrec)/cxb).getA()])    


    c=getCovariance2D('/home/daniel/ntuplesSample/Zee2j7TeV/born',['born'],'h2_pt_y_j1_Orig')


    cupup=c[np.ix_(range(33),range(33))]
    cdodo=c[np.ix_(range(33,40),range(33,40))]

    
    print "max diff between upper matrix and cov of 1D hist: ",max([max(row) for row in ((cupup-cx)/cx).getA()])
    print "max diff between lower matrix and cov of 1D hist: ",max([max(row[1:-2]) for row in ((cdodo-cy)/cy).getA()[1:-2]])
