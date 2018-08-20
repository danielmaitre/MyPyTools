import ROOT
import sys

for f in sys.argv[1:]:
    rf=ROOT.TFile(f)
    t=rf.Get('BHSntuples')
    t.GetEntry(1)
    print t.part
