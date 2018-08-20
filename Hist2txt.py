import math
import HistogramTools
import array
from ROOT import TFile,TH1D

import sys

if len(sys.argv)<3:
	print 'Usage %s filename histogram1 [histogram...]' % sys.argv[0]
	sys.exit(1)

filename=sys.argv[1]


f=TFile(filename)

if not f:
	print 'Could not open file %s' % filename
	sys.exit(1)
for histogramName in sys.argv[2:]:
	h=f.Get(histogramName)

	
	if not h:
		print 'Could not find histogram %s in file %s' % (histogramName,filename)
		continue

	
	nbrBins=h.GetNbinsX()
	print '\n=== %s (%d bins) ===\n' % (histogramName,nbrBins)
	
	if HistogramTools.hasVariableBinSize(h):
		bins=h.GetXaxis().GetXbins()
		bs=[ bins[i] for i in range(nbrBins+1)]
		b=array.array('d',bs)
	else :
		b=[ h.GetBinLowEdge(i) for i in range(1,nbrBins+2) ]

        totalXS=0
        totalXSe2=0
        totalN=0
	for i in range(nbrBins):
		if h.ClassName()=='MyHist':
                        if h.hasNbrEntries():
                                nbrInfo='(%d)'% h.getNbrEntries(i+1)
                        else:
                                nbrInfo='(no nbr entries info)'
			print '%.3f-%.3f | %.5e  +- %.3e %s ' % (b[i],b[i+1],h.GetBinContent(i+1),h.GetBinError(i+1),nbrInfo)

		else: 
			print '%.3f-%.3f | %.3e  +- %.2e  ' % (b[i],b[i+1],h.GetBinContent(i+1),h.GetBinError(i+1))
	
                totalXS+=(b[i+1]-b[i])*h.GetBinContent(i+1)
                totalXSe2+=((b[i+1]-b[i])*h.GetBinError(i+1))**2
                if h.ClassName()=='MyHist' and h.hasNbrEntries():
                        totalN+=h.getNbrEntries(i+1)

        print 'total XS | %.5e  +- %.3e (%d) error is overestimated' % ( totalXS , math.sqrt(totalXSe2) , totalN )
        under,over=(h.GetBinContent(0)*h.GetBinWidth(0),h.GetBinContent(nbrBins+1)*h.GetBinWidth(nbrBins+1))
        underE,overE=(h.GetBinError(0)*h.GetBinWidth(0),h.GetBinError(nbrBins+1)*h.GetBinWidth(nbrBins+1))
        if h.ClassName()=='MyHist' and h.hasNbrEntries():
                underN,overN=h.getNbrEntries(0),h.getNbrEntries(nbrBins+1)
        else:
                underN,overN=0,0
        print 'total XS with under/overflow | %.5e  +- %.3e (%d) ' % ( totalXS+under+over , math.sqrt(totalXSe2+underE**2+overE**2) , totalN+underN+overN )
        
