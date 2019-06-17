#!/usr/bin/python
import sys
import re
import os
import socket
from array import array
import platform
import numpy as np
#verbose = False
verbose=False
verbose=True

oldRootPath="/usr/local/root-5.26.00/lib/root"
if oldRootPath in sys.path:
    sys.path.remove(oldRootPath)
sys.path.append('/opt/root/lib')

possiblePaths=[]

hostname=socket.gethostname()
if verbose: 
    print "Hostname: %s" % hostname
cernHost=re.compile(r'.*cern\.ch.*')
cernHost2=re.compile(r'lxplus.*')
cernHost3=re.compile(r'[0-9a-f]{10}')
#sometimes the jobs are confused about where they are on lxplus
cernHost4=re.compile(r'\Z')
kelvinHost=re.compile(r'.*(?:extra.cea|alineos).*')
hoffman2Host=re.compile(r'login.*')
hoffman2Node=re.compile(r'n[0-9]+')
uiHost=re.compile(r'gridui..*.ac.uk')
newuiHost=re.compile(r'gridui..*.ac.uk')
desktops=re.compile(r'[Dd][0-9]*.*')
newdesktops=re.compile(r'[Dd]16*.*')
scummy=re.compile(r'scummy')
xps=re.compile(r'xps')


if cernHost.match(hostname) or cernHost2.match(hostname) or cernHost3.match(hostname) or cernHost4.match(hostname):  
	sys.path.append('/afs/cern.ch/sw/lcg/hepsoft/0.2/x86_64-slc5-gcc44-opt/lib/python2.5/site-packages/')
       	possiblePaths.append('/afs/cern.ch/user/d/dmaitre/myTools/lib/')

if kelvinHost.match(hostname):  
	sys.path.append('/home/dmaitre/root_svn/lib')
	possiblePaths.append('/home/dmaitre/Tools/lib/')


if hoffman2Host.match(hostname) or hoffman2Node.match(hostname):  

#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/u/home/bern/maitreda/tools/lib/')

if uiHost.match(hostname):  
#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/mt/data-grid/daniel/Tools/lib/')
if newuiHost.match(hostname):  
#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/mt/data-grid/daniel/Tools/lib/')

if newdesktops.match(hostname):  
#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/mt/home/daniel/workspace/NtuplesAnalysis/build_newDesktopRoot6/install_dir/lib/')
        possiblePaths.append('/mt/home/daniel/workspace/nTupleReader/build_newDesktopsRoot6/install_dir/lib/')
if desktops.match(hostname) and not newdesktops.match(hostname):  
#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/mt/home/daniel/workspace/NtuplesAnalysis/build_desktops/install_dir/lib/')


if scummy.match(hostname) or xps.match(hostname):
#	sys.path.append('/u/home/bern/maitreda/root_svn/lib')
	possiblePaths.append('/home/daniel/Tools/lib/')


if hostname == 'ithaka' or hostname=='Ithaka' or hostname == 'L25.PhyIP3.Dur.ac.UK' or hostname=='m076.phyip3-mobile.dur.ac.uk':
    if verbose: print platform.dist()
    if platform.dist()[0] == 'fedora' :
        sys.path.append('/home/daniel/workspace/NtupleAnalysis/build_fedora/install_dir/lib/')
        possiblePaths.append('/home/daniel/workspace/NtupleAnalysis/build_fedora/install_dir/lib/')
    else :
        sys.path.append('/home/daniel/workspace/NtupleAnalysis/build/install_dir/lib/')
        possiblePaths.append('/home/daniel/workspace/NtupleAnalysis/build/install_dir/lib/')


possiblePaths.append('/cvmfs/pheno.egi.eu/daniel/lib/')

import ROOT
from ROOT import TFile





libsToLoad = ['libHisto.so','libInfo.so']



for p in possiblePaths:    
    if verbose:
        print "trying path: %s" % p
    libsToTry=list(libsToLoad)
    for lib in libsToTry:
        path=p+lib
        if os.path.isfile(path):
            if verbose: 
                print 'found %s in path %s' % ( lib,path)
            ROOT.gSystem.Load(path)
            libsToLoad.remove(lib)
            continue
        else:
            if verbose: print ' %s not found in path %s' % ( lib,path)
    if not libsToLoad:
        break

def getOneBin(histFile,observable,suffix,verbose=False):
    f = TFile( histFile )
    histName='%s_%s' % (observable,suffix)
    histogram=f.Get(histName )
    try:
        xsec= histogram.GetBinContent(1)
        error=histogram.GetBinError(1)
        return xsec,error
    except:
        if verbose:
            print 'Histogram %s not found in %s' % (histName,histFile)
            print f.ls()
            raise AttributeError 
        
def getXsection(histFile,suffix):
    return getOneBin(histFile,'xsection',suffix)

def getXsectionInfo(histFile,suffix,part,pdfFile=''):
    f = TFile( histFile )
    histogram=f.Get('xsection_%s' % suffix)
    upperHist=f.Get('xsection_%s_S0' % suffix)
    lowerHist=f.Get('xsection_%s_S2' % suffix)
    central=histogram.GetBinContent(1)
    error=histogram.GetBinError(1)
    upper,lower=0,0
    res=''
    if lowerHist and upperHist:
        upper=upperHist.GetBinContent(1)
        lower=lowerHist.GetBinContent(1)
        res+= '%s: %f (%f) +%f -%f' % (part,central,error,upper-central,central-lower)
    else:
        res+= '%s: %f (%f) ' % (part,central,error)
    if pdfFile != '':
        pdfFile=TFile('pdfErrorsCombined.root')
        g = pdfFile.Get("xsection_%s_PDFE" % suffix)
        if g:
            upperPDF=g.GetErrorYhigh(0)
            lowerPDF=g.GetErrorYlow(0)
            res+=' [pdf: +%f -%f ] ' % (upper,lower)
    return res


def getSuffixes(rootFile):
    f=TFile(rootFile)
    keyList=f.GetListOfKeys()
    nKeys=keyList.GetSize()
    res=[]
    for i in range(nKeys):
        hist=keyList.At(i).GetName()
        xsRegex=re.compile(r'xsection_(?P<suffix>[^_]+)')
        match=xsRegex.match(hist) 
        if match:
            suffix=match.group('suffix')
            if not suffix in res: res.append(suffix)
    return res



def getInfo(rootFileName='',name='',rootFile=None):
    if rootFile:
    	info = rootFile.Get(name)
    else:
    	f = ROOT.TFile(rootFileName)
     	info = f.Get(name)
    return info.getContent()

    


#needs implementing...

def getIntegral(histFile,histname,min,max,verbose=False,includeOverflow=False):
    f = TFile( histFile )
    if verbose: print f 
    try:
        histogram=f.Get(histname)
        try:
            n=histogram.GetNbinsX()
            total,toterr= 0,0
            for i in range(1,n+1):
                le=histogram.GetBinLowEdge(i)
                ue=le+histogram.GetBinWidth(i)
                if  le >= min and ue <= max :
                    total+=histogram.GetBinContent(i)
                    toterr+=histogram.GetBinError(i)
            if max > histogram.GetBinLowEdge(n)+histogram.GetBinWidth(n):
                if verbose: print 'Overflow bin: %s' % histogram.GetBinContent(n+1)
                if includeOverflow:
                    total+=histogram.GetBinContent(n+1)
                    toterr+=histogram.GetBinError(n+1)
            return total,toterr
        except:
            print 'problem with histogram %s' % histname
            return None

    except:
        print 'Problem with file %s',histFile
        return None
        
        
def getRebinned(histogramName,rootFile,xs,newName='h_new'):
	f=TFile(rootFile)
	h=f.Get(histogramName)
	a=array('d',xs)
	return h.Rebin(len(xs)-1,newName,a)

def RebinHist(h,xs,newName='h_new'):
	hw=CloneHist(h)
        
        for i in range(1,hw.GetNbinsX()+1):
            hw.SetBinContent(i,h.GetBinContent(i)*h.GetBinWidth(i))
            hw.SetBinError(i,0)  # needs a better implementation
        #return hw
        try: 
            len(xs)
            a=array('d',xs)
            hwr=hw.Rebin(len(xs)-1,newName,a)
	except TypeError:
            hwr=hw.Rebin(xs,newName)
        
        hwr.Scale(1.0,"width")
        return hwr


	
	
def getHistogramsList(rootFile,typeList=['MyHist','TH1D']):
    try:
        l=list(rootFile.GetListOfKeys())
    except:
        f=ROOT.TFile(rootFile)
        l=list(f.GetListOfKeys())
    names=[ll.GetName() for ll in l if ll.GetClassName() in typeList ]
    return names

def getInfoList(rootFile):
    return getHistogramsList(rootFile,['InfoFile'])



def hasVariableBinSize(hist):
    n=hist.GetXaxis().GetXbins().GetSize()
    if n==0:
        return False
    else :
        return True
    


def CloneHist(h,name=None,title=None,histType=None):
    if not name:
        name=h.GetName()
    if not title:
        title=h.GetTitle()
    if not histType:
        histType=type(h)
    nbrBins=h.GetNbinsX()
    binWidths=[ h.GetBinWidth(i) for i in range(1,nbrBins+1) ]
    if len(set(binWidths))==1  :  #constant bin width
            return histType(name,title,nbrBins,h.GetBinLowEdge(1),h.GetBinLowEdge(nbrBins+1))
    else:   # variable bin width
            bins=h.GetXaxis().GetXbins()
            bs=[ bins[i] for i in range(nbrBins+1)]
            b=array('d',bs)
            return histType(name,title,nbrBins,b)


def CloneHist2D(h,name=None,title=None,histType=None):
    if not name:
        name=h.GetName()
    if not title:
        title=h.GetTitle()
    if not histType:
        histType=type(h)
    nbrBinsX=h.GetNbinsX()
    nbrBinsY=h.GetNbinsY()
    binWidthsX=[ h.GetXaxis().GetBinWidth(i) for i in range(1,nbrBinsX+1) ]
    binWidthsY=[ h.GetYaxis().GetBinWidth(i) for i in range(1,nbrBinsY+1) ]
    if len(set(binWidthsX))==1 and len(set(binWidthsY))==1  :  #constant bin width
            return histType(name,title,
                            nbrBinsX,h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinLowEdge(nbrBinsX+1),
                            nbrBinsY,h.GetYaxis().GetBinLowEdge(1),h.GetYaxis().GetBinLowEdge(nbrBinsY+1))
    else:   # variable bin width
            binsX=h.GetXaxis().GetXbins()
            binsY=h.GetYaxis().GetXbins()
            bsX=[ binsX[i] for i in range(nbrBinsX+1)]
            bsY=[ binsY[i] for i in range(nbrBinsY+1)]
            bX=array('d',bsX)
            bY=array('d',bsY)
            return histType(name,title,nbrBinsX,bX,nbrBinsY,bY)


        

def getHistogramsListWithoutPDFandScale(rootFile):
    if type(rootFile)==str:
        f=TFile(rootFile)
    if type(rootFile)==ROOT.TFile:
        f=rootFile
    keyList=f.GetListOfKeys()
    nKeys=keyList.GetSize()
    res=[]
    for i in range(nKeys):
        if keyList.At(i).GetClassName()  not in ['TH1D','MyHist']:
            continue
        hist=keyList.At(i).GetName()
        pdfRegex=re.compile(r'.*_PDFe.*')
        scaleRegex=re.compile(r'.*_S[0-9]+')
        
        if not pdfRegex.match(hist) and not scaleRegex.match(hist):
            if not hist in res: res.append(hist)
    return res


# Note that this will not reproduce the error on the full cross section since 
# we loose some cancellation between events and counterevent that land in 
# different bind in the differential distribution, but are in the same bin
# for the total cross section  

def cumul(h,useNbFormula=True,name=None):
    if not h:
        print "not an histogram!"
        return None
    if name==None:
        name=h.GetName()+'_cumul'
    nbrBins=h.GetNbinsX()
    combined=[]
    errs=[]
    Ns=[]
    WSum=[]
    WSquaredSum=[]
    NbrTotal=h.getNbrEvents()
    for i in range(1,nbrBins+2):
        binValue=h.GetBinContent(i)*h.GetBinWidth(i)
        binErr=h.GetBinError(i)*h.GetBinWidth(i)
        binErr2=binErr*binErr
        N=h.getNbrEntries(i)
        W2=h.getWgtSqr(i)
        for c in range(len(combined)):
            combined[c]+=binValue
            errs[c]+=binErr2
            Ns[c]+=N
            WSum[c]+=binValue*NbrTotal
            WSquaredSum[c]+=W2
        combined.append(binValue)
        errs.append(binErr2)
        Ns.append(N)
        WSum.append(binValue*NbrTotal)
        WSquaredSum.append(W2)    
    combined.pop()
    errs.pop()
    Ns.pop()
    WSum.pop()
    WSquaredSum.pop()

    hnew=CloneHist(h,name)
    for i in range(0,nbrBins):
        #print 'bin %d, Wsum: %.4f, WS: %.4f, n: %d ' % (i,WSum[i],WSquaredSum[i],Ns[i])
        hnew.setBin(i+1,WSum[i],WSquaredSum[i],Ns[i])

    if useNbFormula:
    	hnew.ComputeErrorsNb()
    else:
        hnew.ComputeErrorsN(NbrTotal) 	
    hnew.normaliseByNumberOfEvents(NbrTotal) 	
    hnew.RemoveBinWidth()
    
    return hnew



def getData(filename,histname):
   f=ROOT.TFile(filename)
   h=f.Get(histname)
   nbins=h.GetNbinsX()
   x=np.array([h.GetBinLowEdge(i) for i in range(1,nbins+2)])
   v=np.array([h.GetBinContent(i) for i in range(0,nbins+2)])
   e=np.array([h.GetBinError(i)  for i in range(0,nbins+2)])
   return x,v,e

def getBinData(filename,histname):
   f=ROOT.TFile(filename)
   h=f.Get(histname)
   nbins=h.GetNbinsX()
   xl=np.array([h.GetBinLowEdge(i) for i in range(1,nbins+2)])
   n=np.array([h.getNbrEntries(i) for i in range(0,nbins+2)])
   w=np.array([h.GetBinContent(i)*h.getNbrEvents()*h.GetBinWidth(i) for i in range(0,nbins+2)])
   w2=np.array([h.getWgtSqr(i) for i in range(0,nbins+2)])

   return xl,w,w2,n,h.getNbrEvents()




def checkHist2Dconsistency(fileName,hx,hy,h2d):

    '''
    This checks that the total weights are consistent between the 2d histogram and the 1d ones. It also checks that the projections are consistent
    '''





    f=ROOT.TFile(fileName)

    h1=f.Get(hx)
    h2=f.Get(hy)
    h=f.Get(h2d)

    nbinsX=h.GetNbinsX()
    nbinsY=h.GetNbinsY()



    sx=sum([h1.GetBinContent(i)*h1.GetXaxis().GetBinWidth(i) for i  in range(nbinsX+2)])
    sy=sum([h2.GetBinContent(i)*h2.GetXaxis().GetBinWidth(i) for i  in range(nbinsY+2)])
    s2=sum([sum([h.GetBinContent(i,j)*h.GetXaxis().GetBinWidth(i)*h.GetYaxis().GetBinWidth(j) for j in range(nbinsY+2)]) for i in range(nbinsX+2)] )


    diffs=((s2-sx)/s2,(s2-sy)/s2,(sx-sy)/s2)
    if max([abs(d) for d in diffs])<1e-13:
        print "OK!"
    else:
        print "s2: %s  sX: %s  sY: %s" % (s2,sx,sy)
        print "1-s2/sX: %s  1-s2/sY: %s  1-sX/sY: %s" % diffs


    wx=np.array([sum([h.GetBinContent(i,j)*h.GetYaxis().GetBinWidth(j) for j in range(nbinsY+2)]) for i in range(nbinsX+2)])

    wy=np.array([sum([h.GetBinContent(i,j)*h.GetXaxis().GetBinWidth(i) for i in range(nbinsX+2)]) for j in range(nbinsY+2)] )

    vx=np.array([h1.GetBinContent(i) for i in range(nbinsX+2)] )
    vy=np.array([h2.GetBinContent(i) for i in range(nbinsY+2)] )


    print wx/vx
    print wy/vy
