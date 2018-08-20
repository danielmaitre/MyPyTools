#!/usr/bin/python
import sys
import re
import os
import os.path

oldRootPath="/usr/local/root-5.26.00/lib/root"
if oldRootPath in sys.path:
    sys.path.remove(oldRootPath)
sys.path.append('/opt/root/lib')

#print sys.path

import ROOT
from ROOT import TFile
import HistogramTools

#ROOT.gSystem.Load('/home/daniel/workspace/NtupleAnalysis/build_fedora/install_dir/lib/libAnalysis.so')

suffix='HT'

def getScaleVariation(rootFile,suffix):
    f=TFile(rootFile)
    keyList=f.GetListOfKeys()
    nKeys=keyList.GetSize()
    res=[]
    for i in range(nKeys):
        hist=keyList.At(i).GetName()
        xsRegex=re.compile(r'xsection_%s_S(?P<n>\d)$' % suffix)
        match=xsRegex.match(hist) 
        if match:
            n=match.group('n')
            if not n in res: res.append(n)
    return res



def getXsectionInfo(histFile,suffix,part,pdfFileName='pdfErrorsCombined.root',doPDF=False):
    f = TFile( histFile )
    histogram=f.Get('xsection_%s' % suffix)
    upperHist=f.Get('xsection_%s_S0' % suffix)
    lowerHist=f.Get('xsection_%s_S3' % suffix)
    
    central=histogram.GetBinContent(1)
    error=histogram.GetBinError(1)
    upper,lower=0,0
    res=''
    ScaleVariationIndices=getScaleVariation(histFile,suffix)
    if ScaleVariationIndices:
        values=[central]
        for i in ScaleVariationIndices:
            tempHist=f.Get('xsection_%s_S%s' % (suffix,i))
            binValue=tempHist.GetBinContent(1)
            values.append(binValue)
        res+= '%s: %f (%f) +%f -%f' % (part,central,error,max(values)-central,central-min(values))
    else:
        res+= '%s: %f (%f) ' % (part,central,error)
    
    if doPDF:
        if os.path.isfile(pdfFileName): 
            pdfFile=TFile(pdfFileName)
            g = pdfFile.Get("xsection_%s_PDFE" % suffix)
            if g:
                upperPDF=g.GetErrorYhigh(0)
                lowerPDF=g.GetErrorYlow(0)
                res+=' [pdf: +%f -%f ] ' % (upperPDF,lowerPDF)

    return res


def getSuffixes(rootFile):
    f=TFile(rootFile)
    keyList=f.GetListOfKeys()
    nKeys=keyList.GetSize()
    res=[]
    for i in range(nKeys):
        hist=keyList.At(i).GetName()
        xsRegex=re.compile(r'xsection_(?P<suffix>[^_]+)$')
        match=xsRegex.match(hist) 
        if match:
            suffix=match.group('suffix')
            if not suffix in res: res.append(suffix)
        xsSelectorRegex=re.compile(r'xsection_(?P<suffix>.*%.*_.*)')
        match=xsSelectorRegex.match(hist) 
        if match:
            suffix=match.group('suffix')
            if not suffix in res: res.append(suffix)
        xsSelectorRegex=re.compile(r'xsection_(?P<suffix>.*_[qg][qg])')
        match=xsSelectorRegex.match(hist) 
        if match:
            suffix=match.group('suffix')
            if not suffix in res: res.append(suffix)
    return res

import os.path


possibleFiles={
    'combinedNLO.root' : 'NLO',
    'histograms_bornLO.root': 'LO',
    'histograms_born.root': 'born',
    'histograms_real.root': 'real',
    'histograms_real-2q.root': 'real',
#    'histograms_real-4q.root': 'real',
    'histograms_real-6q.root': 'real-6q',
    'histograms_real-BH-2q-gg.root': 'real-2q-gg',
    'histograms_real-BH-4q-gg.root': 'real-4q-gg',
    'histograms_real-BH-6q-gg.root': 'real-6q-gg',
    'histograms_real-BH-2q-qg.root': 'real-2q-qg',
    'histograms_real-BH-4q-qg.root': 'real-4q-qg',
    'histograms_real-BH-6q-qq.root': 'real-6q-qg',
    'histograms_real-BH-2q-qq.root': 'real-2q-gg',
    'histograms_real-BH-4q-qq.root': 'real-4q-qg',
    'histograms_real-BH-6q-qq.root': 'real-6q-qq',
    'histograms_vsub.root': 'vsub',
    'histograms_vsub-qq.root': 'vsub',
    'histograms_vsub-qg.root': 'vsub',
    'histograms_vsub-gg.root': 'vsub',    
    'histograms_loop.root': 'loop',
    'histograms_loop-lc.root': 'loop-lc',        
    'histograms_loop-fmlc.root': 'loop-fmlc',
    'histograms_loop-lc-4q-gg.root': 'loop-lc-4q-gg',        
    'histograms_loop-lc-4q-qg.root': 'loop-lc-4q-qg',        
    'histograms_loop-lc-4q-qq.root': 'loop-lc-4q-qq',        
    'histograms_loop-lc-2q-gg.root': 'loop-lc-2q-gg',        
    'histograms_loop-lc-2q-qg.root': 'loop-lc-2q-qg',        
    'histograms_loop-lc-2q-qq.root': 'loop-lc-2q-qq'        
    }

doPDFList={'combinedNLO.root':True}

import sys

infos={}
    
if len(sys.argv) >1 :
    files=sys.argv[1:]
else:
    files=possibleFiles.keys()


for f in files:
    if os.path.isfile(f):
        #print f

#        if len(sys.argv) > 1:
#            suffixes=sys.argv[1:]
#        else:
#
        suffixes = getSuffixes(f)
        for suffix in suffixes:
            #print suffix
            #print getXsectionInfo(f,suffix,possibleFiles[f])
            displayName=possibleFiles.get(f,f)
            infos[suffix]=infos.get(suffix,'')+'\n'+getXsectionInfo(f,suffix,displayName,doPDF=doPDFList.get(f,False))


#    print getXsectionInfo('histograms_vsub.root',suffix,'vsub')


for key in infos.keys():
    print key
    print infos[key]
    print '------'

