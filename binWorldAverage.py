import math 
import HistogramTools
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!  



import pylab
import HistogramTools
def makePlot(data,err,name):
    av=sum(data)/len(data)
    averr=math.sqrt(sum([(x-av)*(x-av) for x in data])/len(data))
    avopterr=math.sqrt(1/sum([1/(s*s) for s in err]))
    avopt=sum([x/(s*s) for x,s in zip(data,err)])*avopterr*avopterr
    pylab.ylim(0,len(data)+1)
    pylab.axvspan(av-averr,av+averr, facecolor='g', alpha=0.5)
    pylab.axvline(x=av,color='g')
    pylab.axvspan(avopt-avopterr,avopt+avopterr, facecolor='b', alpha=0.5)
    pylab.axvline(x=avopt,color='b')
    pylab.errorbar(data,range(1,len(data)+1),xerr=err,fmt='.',color='k')
    pylab.savefig(name)
    pylab.clf()


#data=[3.25378,3.90576,3.12582,2.10956*10,3.64638,3.70496,3.46274,3.64618]
#err=[0.3347,0.3093,0.3294, 17.50,0.2242,0.4325,0.2302,0.4379]

import sys
import ROOT

if len(sys.argv)<5:
    print 'Usage: binWorldAverage HISTNAME BINNBR NAME_OF_RESULTING_PNG_WITHOUT_SUFFIXES FILES_TO_CONSIDER'
    sys.exit(1)

histname=sys.argv[1]
binnbr=int(sys.argv[2])
name=sys.argv[3]
files=sys.argv[4:]

print sys.argv


rootFiles=[ROOT.TFile(f) for f in files]
hs=[f.Get(histname) for f in rootFiles ]

dataerr=[(h.GetBinContent(binnbr),h.GetBinError(binnbr)) for h in hs]
dataerr=[ (d,e) for d,e in dataerr if e>0 ]
data=[de[0] for de in dataerr]
err=[de[1] for de in dataerr]

print dataerr

name='%s_bin-%s-%s.png' % (name,hs[0].GetBinLowEdge(binnbr),hs[0].GetBinLowEdge(binnbr+1))

makePlot(data,err,name)
