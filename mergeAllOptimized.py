#!/usr/bin/python
import re
import sys
import getopt
from math import sqrt
sys.path.append('/opt/root/lib')
import ROOT
from ROOT import TFile
import array
import HistogramTools

#ROOT.gSystem.Load('/home/daniel/workspace/NtupleAnalysis/build/.libs/libAnalysis.so')

ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load('/home/daniel/workspace/NtupleAnalysis/build_fedora/install_dir/lib/libAnalysis.so')

#f=ROOT.TFile("histograms_born_test.root")
#mh=f.Get("h_pt_p_HTscale")
#mh.SetFillColor(2)
#mh.Draw("E2")

quitIfNoAnalysisDat=False

def combine(rootFile,inFiles,histogram,useNbFormula=True):
    mhs=list()
    N=0
    WSum=list()
    WSquaredSum=list()
    n=list()
    for i in inFiles:
         ff=ROOT.TFile(i)
         h=ff.Get(histogram)
         h.SetDirectory(0)
         mhs.append(h)
         N+=h.getNbrEvents()
    if type(h) in [ROOT.MyHist,ROOT.MyHistRCumul,ROOT.MyHistLCumul]:
        nbrBins=h.GetNbinsX()+2
        average=[0]*nbrBins
        errors=[0]*nbrBins
        for i in range(nbrBins):
            for h in mhs:
                v=h.GetBinContent(i)
                e=h.GetBinError(i)
                if e==0:
                    if v!=0:
                        print "Zero error but non-zero average, don't know what to do about that..."
                else:
                    #print 'v:',v
                    #print 'e:',e
                    average[i]=average[i]+v/(e*e)
                    errors[i]=errors[i]+1/(e*e)
            if errors[i]==0:
                if average[i]!=0:
                    print "Zero error but non-zero average, don't know what to do about that..."
            else:
                #print average[i]
                #print errors[i]
                average[i]=average[i]/errors[i]
                errors[i]=sqrt(1/errors[i])
                #print average[i]
                #print errors[i]
    elif type(h)==ROOT.MyHist2D:
        #print "2D Histogram"
        nbrBinsX=h.GetNbinsX()+2
        nbrBinsY=h.GetNbinsY()+2
        WSum=[[0]*nbrBinsY for i in range(nbrBinsX) ]
        WSquaredSum=[[0]*nbrBinsY for i in range(nbrBinsX) ]
        n=[[0]*nbrBinsY for i in range(nbrBinsX) ]
        for i in range(nbrBinsX):
            for j in range(nbrBinsY):
                for h in mhs:
                    Nbr=h.getNbrEvents()
                    n[i][j]+=h.getNbrEntries(i,j)
                    area=h.GetXaxis().GetBinWidth(i)*h.GetYaxis().GetBinWidth(i)
                    WSum[i][j]+=(h.GetBinContent(i,j)*area*Nbr)
                    WSquaredSum[i][j]+=h.getWgtSqr(i,j)
    else:
        print 'Histogram is neither a 1D or 2D histogram'
        raise
    rootFile.cd()             
    if type(h)  in [ROOT.MyHist,ROOT.MyHistRCumul,ROOT.MyHistLCumul]:
        nbins=h.GetXaxis().GetNbins()
        nbrBins=mhs[0].GetNbinsX()+2
        binWidths=[ h.GetBinWidth(i) for i in range(nbins) ]
        if len(set(binWidths))==1  :  #constant bin width
            total=type(h)(mhs[0].GetName(),mhs[0].GetTitle(),mhs[0].GetNbinsX(),mhs[0].GetBinLowEdge(1),mhs[0].GetBinLowEdge(nbrBins-1))
        else:   # variable bin width
            bins=h.GetXaxis().GetXbins()
            bs=[ bins[i] for i in range(nbins+1)]
            b=array.array('d',bs)
            total=type(h)(mhs[0].GetName(),mhs[0].GetTitle(),nbrBins-2,b)

        for i in range(nbrBins):
            #print 'bin %d, Wsum: %.4f, WS: %.4f, n: %d ' % (i,WSum[i],WSquaredSum[i],n[i])
            total.SetBinContent(i,average[i])
            total.SetBinError(i,errors[i])
            #print average[i],errors[i]
            #print total.GetBinContent(i),total.GetBinError(i)

    elif type(h)==ROOT.MyHist2D:
        total=ROOT.MyHist2D(mhs[0].GetName(),mhs[0].GetTitle(),mhs[0].GetNbinsX(),mhs[0].GetXaxis().GetXmin(),mhs[0].GetXaxis().GetXmax(),mhs[0].GetNbinsY(),mhs[0].GetYaxis().GetXmin(),mhs[0].GetYaxis().GetXmax())
        nbrBinsX=mhs[0].GetNbinsX()+2
        nbrBinsY=mhs[0].GetNbinsY()+2
        for i in range(nbrBinsX):
            for j in range(nbrBinsY):
                total.setBin(i,j,WSum[i][j],WSquaredSum[i][j],n[i][j])

    #if useNbFormula:
    #    total.ComputeErrorsNb()
    #else:
#	total.ComputeErrorsN(N) 	
    #total.normaliseByNumberOfEvents(N)
    #total.RemoveBinWidth()
    total.Write()
#    total.Draw("SAMEE1")





def usage():
    print 'usage: merge -o OUTPUTFILE FILE...'

def main(argv):
    foutName="merged.root"
    args=list()
    try:
        opts,args = getopt.getopt(argv,'o:')
        if len(args)<2:
            print "Need at least two files to merge!"
            raise
        for o,a in opts:
            if o == '-o':
                foutName=a
    except:
        usage()
        sys.exit(2) 
        
    fout=TFile(foutName,"RECREATE")
    files=args
    #hist="h_pt_p_HTscale"
    f=TFile(files[0])
    hasAnalysisDat=False
    useNbFormula=True
    if 'analysis.dat' in HistogramTools.getInfoList(f):
        hasAnalysisDat=True
        originalAnalysisDat=HistogramTools.getInfo(rootFile=f,name='analysis.dat')

        for ff in files[1:]:
            if 'analysis.dat' in HistogramTools.getInfoList(ff):
                otherAnalysisDat=HistogramTools.getInfo(rootFileName=ff,name='analysis.dat') 			   
                if otherAnalysisDat!=originalAnalysisDat:
                    print 'Analysis.dat not the same for %s and %s' % (files[0],ff)
                    sys.exit(1)
            else:
                if quitIfNoAnalysisDat:
                    print 'ERROR: No Analysis.dat in %s' % (ff)              
                    sys.exit(1)
                else:
                    print 'Warning: No Analysis.dat in %s (assume all is fine...)' % (ff)              
        print 'All files have the same analysis.dat: good.'

		
	useNbFormulaRegex=re.compile(r'^UseNbFormula\s+(?P<answer>\w+)',re.M)
	# cycle over all matches, in case there are more than one
	for m in useNbFormulaRegex.finditer(originalAnalysisDat):
		if m.group('answer') in ['yes','Yes']:
                    print "found entry: %s" % m.group()
                    useNbFormula=True
		else:
                    print "found entry: %s" % m.group()
                    useNbFormula=False

    keyList=f.GetListOfKeys()
    nKeys=keyList.GetSize()
    print nKeys
    for i in range(nKeys):
        hist=keyList.At(i).GetName()
        histType=keyList.At(i).GetClassName() 
        if histType in ['MyHist','MyHist2D','MyHistRCumul','MyHistLCumul' ] :  
            print 'Combining histogram %s' % hist
            combine(rootFile=fout,inFiles=files,histogram=hist,useNbFormula=useNbFormula)
        else:
            print "Cannot combine %s of type %s, ignoring..." % (hist,histType )
    fout.Close()
    if hasAnalysisDat:
        import tempfile
        tmp=tempfile.NamedTemporaryFile()
        tmp.write(originalAnalysisDat)
        tmp.file.flush()
        import subprocess
		
        cmd='/home/daniel/workspace/NtupleAnalysis/build_fedora/install_dir/bin/storeInfo --add --root-file=%s --name=analysis.dat --file=%s' % (foutName,tmp.name)
        print cmd
        p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        out=p.stdout.read().strip()

if __name__ == "__main__":
    main(sys.argv[1:])
