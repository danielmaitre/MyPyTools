#! /usr/bin/env python

import sys, os, copy
from math import sqrt
from subprocess import Popen
import lighthisto
import ROOT
import HistogramTools

## Try to load faster but non-standard cElementTree module
try:
    import xml.etree.cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        try:
            import xml.etree.ElementTree as ET
        except:
            sys.stderr.write("Can't load the ElementTree XML parser: please install it!\n")
            sys.exit(1)

from optparse import OptionParser
parser = OptionParser(usage="%prog aidafile [aidafile2 ...]")

parser.add_option("-o", "--outfile", dest="OUTFILE",
                  default="merged.aida", help="file for merged aida output.")
parser.add_option("-t", "--template", dest="TEMPLATE",
                   help="template aida file for converted aida output.")
opts, args = parser.parse_args()
headerprefix = ""

if len(args) < 1:
    sys.stderr.write("Must specify at least one ROOT histogram file\n")
    sys.exit(1)


try:
    outaida = open(opts.OUTFILE, "w")
except:
    sys.stderr.write("Couldn't open outfile %s for writing." % opts.OUTFILE)


try:
    outdat = open(opts.OUTFILE.replace(".aida", ".dat"), "w")
except:
    sys.stderr.write("Couldn't open outfile %s for writing." % opts.OUTFILE.replace(".aida", ".dat"))

rootFile=ROOT.TFile(args[0])

rootFile.ls()


def getTotalCrossSection(name):
    hs=histos['/MC_LES_HOUCHES_SYSTEMATICS_ATLAS/%s' % name ]
    a=sum([hs.getBin(i).val for i in range(hs.numBins())])
    r=hs.getBin(0).getXRange()
    width=r[1]-r[0]
    return a*width

## Get histos

weights = {}



histos={}

tree = ET.parse(opts.TEMPLATE)
for dps in tree.findall("dataPointSet"):
    h = lighthisto.Histo.fromDPS(dps)
    histos[h.fullPath()] = h


## Merge histos

suffix='HTp'

nameMap={
         'jetpt0':'h_jet_pt1_%s' % suffix,
         'jeteta0':'h_jet_eta1_%s' % suffix,
         'jetpt1':'h_jet_pt2_%s' % suffix,
         'jeteta1':'h_jet_eta2_%s' % suffix,
         'jetpt2':'h_jet_pt3_%s' % suffix,
         'jeteta2':'h_jet_eta3_%s' % suffix,
         'jetpt3':'h_jet_pt4_%s' % suffix,
         'jeteta3':'h_jet_eta4_%s' % suffix,
         'jetpt4':'h_jet_pt5_%s' % suffix,
         'jeteta4':'h_jet_eta5_%s' % suffix,
         'sigmatot':'xsection_%s' % suffix,
         'Wpt':'h_pt_W_%s' % suffix,
         'Wmt':'h_mt_W_%s' % suffix,
         'Wmass':'h_m_W_%s' % suffix,
         'Weta':'h_eta_W_%s' % suffix,
         'leptonpt':'h_pt_e_%s' % suffix,
         'leptoneta':'h_eta_e_%s' % suffix,
         'HTall1':'h_HTall_%s' % suffix,
         'HTjet1':'h_HTjet_%s' % suffix,
         'sumET0':'h_sumET_%s' % suffix,         
         'sumET0':'h_sumETnoLepton_%s' % suffix,         
         'sumET1':'h_sumETnoLepton1_%s' % suffix,         
         'njet':'h_njets_%s' % suffix,
         'dEtaj0j1':'h_dEtaj1j2_%s' % suffix,
         'dPhij0j1':'h_dPhij1j2_%s' % suffix,
         'dRj0j1':'h_dRj1j2_%s' % suffix,
         'dRj0l':'h_dRj1l_%s' % suffix,
         'dPhij0l':'h_dPhij1l_%s' % suffix,
         'dEtaj0l':'h_dEtaj1l_%s' % suffix,
         'mj0l':'h_Mj1l_%s' % suffix,
         'mj0j1':'h_dMj1j2_%s' % suffix,
         'mj0j1W':'h_Mj1j2W_%s' % suffix,
         'beamthrustparticles':'h_beamThrust_%s' % suffix,
         'beamthrustjets':'h_beamThrustJets_%s' % suffix,
         'ptratioj1j0':'h_ptJetRatio_%s' % suffix

         
}


outhistos = {}

#totalCrossSection=rootFile.Get('xsection_%s' % suffix).GetBinContent(1)
#print totalCrossSection
#sys.exit(0)

for path, hs in histos.iteritems():
    if nameMap.get(hs.name,False):
        print '%s found'% hs.name
        rootHist=rootFile.Get(nameMap[hs.name])
        #print rootHist
        if rootHist:
            outhistos[path] = copy.deepcopy(hs)
            for i, b in enumerate(outhistos[path].getBins()):
                #print 'aida val: ',outhistos[path].getBin(i).val 
                #print 'aida err: ',outhistos[path].getBin(i).err
                #print 'root val: ',rootHist.GetBinContent(i+1)
                #print 'root err: ',rootHist.GetBinError(i+1)

                if rootHist.ClassName()=='TGraphAsymmErrors':
                    outhistos[path].getBin(i).yval = rootHist.GetY()[i]
                    print outhistos[path].getBin(i).yval
                    outhistos[path].getBin(i).yerrminus=rootHist.GetErrorYlow(i)
                    outhistos[path].getBin(i).yerrplus=rootHist.GetErrorYhigh(i)
                else:
                    outhistos[path].getBin(i).yval = rootHist.GetBinContent(i+1)
                    outhistos[path].getBin(i).yerrminus=rootHist.GetBinError(i+1)
                    outhistos[path].getBin(i).yerrplus=rootHist.GetBinError(i+1)
                    #outhistos[path].getBin(i).setErr(rootHist.GetBinError(i+1))

        else:
            print 'no hostogram %s in root file' % nameMap[hs.name]
    else:
        print '%s not found'% hs.name
## Write out merged histos
#print sorted(outhistos.values())
outdat.write("\n\n".join([h.asFlat() for h in sorted(outhistos.values())]))
outdat.write("\n")
outdat.close()

Popen(["flat2aida", opts.OUTFILE.replace(".aida", ".dat")], stdout=outaida).wait()

os.unlink(opts.OUTFILE.replace(".aida", ".dat"))
