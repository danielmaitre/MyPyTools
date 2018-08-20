import sys
import ROOT
import array
import HistogramTools
import math

from ROOT import gROOT, TH1D, TFile, THStack
import re
import sys
gROOT.Reset()

basePath='/home/daniel/NtuplesAnalysis'
analysisName='Joey'
process='Wm'


paths = ['%s/analysis_%s%sj7TeV_%s' % (basePath,process,i,analysisName) for i in range(0,5) ]
filesj = [ TFile( '%s/combinedNLO.root' % path ) for path in paths ]
filesjborn = [ TFile( '%s/histograms_born.root' % path ) for path in paths ]

colors=[8,2,5,3,4,6,1]

def setProcessAndAnalysis(pro,analysis,path='/home/daniel/NtuplesAnalysis'):
    global process
    process=pro
    global analysisName
    analysisName=analysis
    global basePath
    basePath=path
    global paths
    paths = ['%s/analysis_%s%sj7TeV_%s' % (basePath,process,i,analysisName) for i in range(0,5) ]
    global filesj
    filesj = [ TFile( '%s/combinedNLO.root' % path ) for path in paths ]
    global filesjborn
    filesjborn = [ TFile( '%s/histograms_born.root' % path ) for path in paths ]

def setColors(cols):
    global colors    
    colors=cols
    
def total(data):
    return [
        n for n in data.njex if n
    ]

def W1jComp(data):
    den = data.nj[1]
    if den != 0.0:
        return [
            0,
            data.njex[1]/den, 
            2*data.njex[2]/den, 
            3*data.njex[3]/den, 
            4*data.nj[4]/den,
            0 
            ]
    else:
        return [0,0,0,0,0,0]

def W2jComp(data):
    den = data.nj[2]
    if den != 0.0:
        return [
        0,
        0,
        2*data.njex[2]/den, 
        3*data.njex[3]/den, 
        4*data.nj[4]/den,
        0
            ]
    else:
        return [0,0,0,0,0,0]

def W3jComp(data):
    den = data.nj[3]
    if den!=0:
        return [
            0,
            0,
            0,
            3*data.njex[3]/den, 
            4*data.nj[4]/den,
            0
          ]
    else:
        return [0]*6

def WjSum(data):
    n5=data.nj[4]-data.njex[4]
    return [
        data.njex[0], 
        data.njex[1], 
        data.njex[2], 
        data.njex[3], 
        data.njex[4],
        n5
      ]

def WjSumBrian(data):
    n5=data.nj[4]-data.njex[4]
    return [
        data.nj[0],
        #data.nj[0]-data.njborn[1], 
        data.nj[1]-data.njborn[1], 
        data.nj[2]-data.njborn[2], 
        data.nj[3]-data.njborn[3], 
        data.nj[4]-data.njborn[4], # same as njborn[5]
        0
      ]



class container():
    pass


def doPlot(plotName,fn,Nmax=5,Nmin=0,outputSuffix='',inputSuffix='',outputHistogramName='',histogramDescription='',rootFile=None,doStack=True,errfn=None,doSaveHistograms=False,Rebin=None):
    '''
    plotName is the name of the plot, without scale suffix
    inputSuffix is the suffix of the input histogram    
    '''
    N=Nmax-Nmin+1
    fullPlotName='%s_%s' % (plotName,inputSuffix)
    
    if outputHistogramName=='':
        outputHistogramName=plotName
    if histogramDescription=='':
        histogramDescription='Merged sample for %s' % plotName
        
    
    print 'Looking for information for plot: ',plotName
    hjs=[0]*6
    hjexs=[0]*6
    hjborns=[0]*6
    for n in range(Nmin,min(Nmax+1,5)):
        hjs[n]=filesj[n].Get(fullPlotName)
        htest=filesj[n].Get(fullPlotName+'%%Njets_%s_%s' % (n-0.5,n+0.5))
        if htest:
            hjexs[n]=htest
        else:
            htest=filesj[n].Get(fullPlotName+'%%%sj' % (n) )
            if htest:
                hjexs[n]=htest
            else:
                print 'No information about exclusive %s jet for histogram %s (with suffix %s) in file %s' % (n,plotName,inputSuffix,filesj[n].GetName())
        hjborns[n]=filesjborn[n].Get(fullPlotName)

    if Rebin:
        def doRebin(x): 
            if x :
                return HistogramTools.RebinHist(x,Rebin,x.GetName()+"rebinned") 
            else  :
                return x

        hjexs = [ doRebin(h) for h in hjexs ]
        
        hjs = [ doRebin(h) for h in hjs ]
        hjborns = [ doRebin(h) for h in hjborns ]

    
    bins=list()
    validhjs=[h for h in hjs if h]
    if not validhjs:
        print 'No proper histograms found'
        sys.exit(1)
    nbrBins=validhjs[0].GetNbinsX()
    names=[ '%s_%s_%s' % (plotName,outputSuffix,i ) for i in range(Nmin,Nmax+1) ]

    if HistogramTools.hasVariableBinSize(validhjs[0]):
        bins=validhjs[0].GetXaxis().GetXbins()
        bs=[ bins[i] for i in range(nbrBins+1)]
        b=array.array('d',bs)
        hist = TH1D( outputHistogramName+'_'+outputSuffix, histogramDescription,nbrBins ,b )
        hists= [ TH1D( name , histogramDescription,nbrBins ,b ) for name in names ]
    else:
        xmin=hjs[2].GetBinLowEdge(1)
        xmax=hjs[2].GetBinLowEdge(nbrBins+1)
        hist = TH1D( outputHistogramName+'_'+outputSuffix, histogramDescription,nbrBins ,xmin,xmax )
        hists= [ TH1D( name , histogramDescription,nbrBins ,xmin , xmax ) for name in names ]


    


    for i in range(1,nbrBins+1):
        #if hjs[2].GetBinCenter(i)!=h3j.GetBinCenter(i):
            #print 'Bins don\'t correspond! h2j: ',h2j.GetBinCenter(i),' h3j:',h3j.GetBinCenter(i)
        data=container()
        data.nj=[None]*6
        data.njborn=[None]*6
        data.njex=[None]*6
        data.njerr=[None]*6
        data.njbornerr=[None]*6
        data.njexerr=[None]*6
        
        for njet in range(Nmin,Nmax+1):
            if hjs[njet]:
                data.nj[njet]=hjs[njet].GetBinContent(i)
                data.njerr[njet]=hjs[njet].GetBinError(i)
            else:
                print 'No info for %s' % njet
                data.nj[njet]=None
                data.njerr[njet]=None
            if hjborns[njet]:
                data.njborn[njet]=hjborns[njet].GetBinContent(i)
                data.njbornerr[njet]=hjborns[njet].GetBinError(i)
            else:
                print 'No info for %s born' % njet
                data.njborn[njet]=None
                data.njbornerr[njet]=None
        
        for njet in range(0,5):
            if hjexs[njet]:
                data.njex[njet]=hjexs[njet].GetBinContent(i)
                data.njexerr[njet]=hjexs[njet].GetBinError(i)
            else:    
                if data.nj[njet]==None or data.njborn[njet+1] == None:
                    data.njex[njet]=None
                    data.njexerr[njet]=None
                else :
                    data.njex[njet]=data.nj[njet]-data.njborn[njet+1]
                    data.njexerr[njet]=math.sqrt(math.pow(data.njerr[njet],2)+math.pow(data.njbornerr[njet+1],2))
                    
        if data.njex[4] and data.nj[4]:
            data.nj[5]=data.nj[4]-data.njex[4]
            data.njerr[5]=math.sqrt(math.pow(data.njerr[4],2)+math.pow(data.njexerr[4],2))
        #print 'nj',data.nj
        #print 'njex',data.njex
        #print 'njborn',data.njborn
        
        hValues = fn(data)
        sumv=sum([ v for v in hValues if v])
        hist.SetBinContent(i,sumv)

        if errfn:
            errValues=errfn(data)
            sumerr=math.sqrt(sum([ v*v for v in errValues if v]))
            hist.SetBinError(i,sumerr)
            #print hValues
        for v in range(len(hValues)):
            if hValues[v]:
                hists[v].SetBinContent(i,hValues[v])
            else :
                hists[v].SetBinContent(i,0)
    if doStack:
        tsName='sh_'+outputHistogramName+'_'+outputSuffix
        #print tsName
        stack=THStack(tsName,'Stacked view of '+histogramDescription)
        for i in range(N):
            hists[i].SetFillColor(colors[i])
            stack.Add(hists[i])

    if rootFile:
        rootFile.cd()
        if doStack:
            stack.Write()
        if doSaveHistograms:
            for h in hists:
                h.Write()
        hist.Write()

    if doStack:
        return (hist,stack)
    else:
        return hist


