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
	print '\n# === %s (%d bins) ===\n' % (histogramName,nbrBins)
	
	if HistogramTools.hasVariableBinSize(h):
		bins=h.GetXaxis().GetXbins()
		bs=[ bins[i] for i in range(nbrBins+1)]
		b=array.array('d',bs)
	else :
		b=[ h.GetBinLowEdge(i) for i in range(1,nbrBins+2) ]
	for i in range(nbrBins):
 		print '%.3f %.3f %.9e %.3e ' % (b[i],b[i+1],h.GetBinContent(i+1),h.GetBinError(i+1))
	
