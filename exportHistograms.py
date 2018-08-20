from optparse import OptionParser
import ROOT
import HistogramTools

parser = OptionParser(usage="exportHistograms -f INPUT_FILE -o OUTPUT_FILE HISTOGRAMS")
parser.add_option("-o", "--output", dest="outfile",
                  help="write histograms to FILE", metavar="FILE")
parser.add_option("-f", "--file", dest="infile",
                  help="write histograms to FILE", metavar="FILE")
parser.add_option("-a", "--add",
                  action="store_true", dest="add", default=False,
                  help="add to the output root file instead of recreating it")

(options, args) = parser.parse_args()



f=ROOT.TFile(options.infile,'READONLY')

if options.add:
  out=ROOT.TFile(options.outfile,"UPDATE")
else:
  out=ROOT.TFile(options.outfile,"RECREATE")

for hist in args:
  h=f.Get(hist)
  if not h:
      print 'no histogram %s' % hist
      continue
  hh=ROOT.TH1D(h)
  out.cd()
  hh.Write()


