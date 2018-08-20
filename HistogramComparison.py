import ROOT
import math
import sys

import HistogramTools
#analysisInstallPath='/home/daniel/workspace/NtupleAnalysis/build/.libs'
#ROOT.gSystem.Load(analysisInstallPath+'/libAnalysis.so')
templatePath='/home/daniel/workspace/NtupleAnalysis'

def showPlots(h1,h2,psFileName='comp.ps',scaleSecond=1.0):
    c1 = ROOT.TCanvas("c1", "First canvas", 800, 600);
    c1.SetBorderMode(0);
    ROOT.gStyle.SetPadBorderMode(0);
    ROOT.gStyle.SetFrameBorderMode(0);
    ROOT.gStyle.SetOptStat("0")
    p1=ROOT.TPad("pad1","pad 1",0.0,0.4,1.0,1.0,0)
    p2=ROOT.TPad("pad2","pad 2",0.0,0.0,1.0,0.4,0)
    p1.SetBottomMargin(0.0)
    p2.SetTopMargin(0.0)
    p1.SetTickx(2)
    p2.SetTickx(1)
    p1.SetBorderMode(0)
    p2.SetBorderMode(0)
    p1.Draw()
    p2.Draw()
    p1.cd()
    h1.SetLineColor(1)
    h2.SetLineColor(2)
    h2.Scale(scaleSecond)
    h1.Draw('HISTE')
    h2.Draw("SAMEHIST")


    h0=h1.Clone();
    h=h2.Clone();
    min=h1.GetNbinsX()	
    for j in range(1,min+1) :
        value=h.GetBinContent(j)
        error=h.GetBinError(j)
        value1=h1.GetBinContent(j)
        error1=h1.GetBinError(j)
        if  value1!=0 :
            h.SetBinContent(j,value/value1);
            h.SetBinError(j,error/value1);
            h0.SetBinContent(j,value1/value1);
            h0.SetBinError(j,error1/value1);
        else:
            h.SetBinContent(j,1);
            h.SetBinError(j,0);
            h0.SetBinContent(j,1);
            h0.SetBinError(j,0);
    h.SetLineColor(2)
    h.SetLineStyle(0)
    h.SetTitle("")
    h.SetLineWidth(2)
    h0.SetLineColor(1)
    h0.SetLineStyle(1)
    h0.SetTitle("")
    h0.SetLineWidth(2)
    p2.cd()
    h.Draw('EHIST')
    h0.Draw("SAME")
    c1.Print(psFileName)
 



def compare(file1,file2,name,psFileName='comp.ps',scaleSecond=1.0):
    f1=ROOT.TFile(file1)
    f2=ROOT.TFile(file2)
    h1 = f1.Get(name)
    h2 = f2.Get(name)
    showPlots(h1,h2,psFileName,scaleSecond)

def compareHist(h1,h2):
    totalSigma=0
    n = h1.GetNbinsX()
    for i in range(1,n+1):
        v1,v2=h1.GetBinContent(i),h2.GetBinContent(i)
        e1,e2=h1.GetBinError(i),h2.GetBinError(i)
        if v1!=v2 and (e1+e2)!=0.0 :
            sigma=abs(v1-v2)/(e1+e2)
            totalSigma+=sigma
    return math.log(totalSigma/float(n))
            
                
def compareAllPlots(histogramFileNames,SaveAs=None):
	
	allfs=[ROOT.TFile(name) for name in histogramFileNames ]
	failed = [ f for f in allfs if not f.IsOpen()]
	if failed:
		print 'not all files could be found, missing:'
		for f in failed:
			print f.GetName()
	fs = [ f for f in allfs if f.IsOpen()]
	if fs:
		print 'files found:'
		for f in fs:
			print f.GetName()
	else:
		return None
	hnames=set()
	for f in fs:
		names= [ x.GetName() for x in list(f.GetListOfKeys()) if x.GetClassName() == 'MyHist' ]
		if len(hnames) ==0:
			hnames.update(set(names))
		else:
			hname=hnames.intersection(set(names))
	#print hnames
	
	
	CtestData=[]
	KtestData=[]
	SdData=[]
	
	filesPairs=[ (f1,f2) for f1 in fs for f2 in fs if f1<f2 ]
	
	for name in list(hnames)[-5:]:
		for fp in filesPairs:
			h1 = fp[0].Get(name)
			h2 = fp[1].Get(name)
			Ktest = h1.KolmogorovTest(h2)
			chi=ROOT.Double(0.0);ndf=ROOT.Long();igood=ROOT.Long()
			Ctest=h1.Chi2TestX(h2,chi,ndf,igood,'WW')
			sd = compareHist(h1,h2)
			print name,': ', Ktest , ' chi^2 test: ', Ctest,' chi2:' , chi ,' ndf: ',ndf,' igood: ',igood,' average sigma diff:',sd
			CtestData.append(Ctest)
			KtestData.append(Ktest)
			SdData.append(sd)
	
	
	import numpy as np
	import matplotlib.pyplot as plt
	
	fig = plt.figure()
	fig.subplots_adjust(wspace=0.8)
	fig.subplots_adjust(hspace=0.8)
	
	ax1 = fig.add_subplot(3,3,1)
	ax1.scatter(KtestData, SdData)
	ax1.set_xlabel('K')
	ax1.set_ylabel('Sd')
	
	ax2 = fig.add_subplot(3,3,2)
	ax2.scatter(KtestData, CtestData)
	ax2.set_xlabel('K')
	ax2.set_ylabel('Chi')
	
	ax3 = fig.add_subplot(3,3,3)
	ax3.scatter(CtestData, SdData)
	ax3.set_xlabel('Chi')
	ax3.set_ylabel('Sd')
	if not SaveAs==None:	
		plt.savefig(SaveAs)
	
	return fig

histogramFileNames=[
    'analysis_Wm1j7TeV_Joey/histograms_loop.root_00',
    'analysis_Wm1j7TeV_Joey/histograms_loop.root_01',
    'analysis_Wm1j7TeV_Joey/histograms_loop.root_02',
    'analysis_Wm1j7TeV_Joey/histograms_loop.root_03',
    'analysis_Wm1j7TeV_Joey/histograms_loop.root_04'
#    'analysis_Wm1j7TeV_Joey/histograms_vsub.root_00',
#    'analysis_Wm1j7TeV_Joey/histograms_vsub.root_01',
#    'analysis_Wm1j7TeV_Joey/histograms_born.root_00',
#    'analysis_Wm1j7TeV_Joey/histograms_born.root_01'
#    'analysis_Wm1j7TeV_Joey/histograms_bornLO.root_00',
#    'analysis_Wm1j7TeV_Joey/histograms_bornLO.root_01'
    ]

#compareAllPlots(histogramFileNames)

def makePScomparison(file1,file2,exclude=None,scaleSecond=1.0):
    import HistogramTools as HT
    h1=HT.getHistogramsList(file1)
    h2=HT.getHistogramsList(file2)
    hists=set(h1).intersection(set(h2))
    if exclude:
        import re
        excl=re.compile(exclude)
        hists=[h for h in hists if not excl.match(h)]
    psFiles=[]
    for h in hists:
        psFileName='%s.ps' % h
        psFiles.append(psFileName)
        compare(file1,file2,h,psFileName,scaleSecond)
    import subprocess
    import os
    import shlex
    Cmd='psmerge -oall.ps %s ' % ' '.join(psFiles)
    args=shlex.split(Cmd)

    p=subprocess.Popen(args)
    p.wait()
    for f in psFiles:
        os.remove(f)
    p=subprocess.Popen('gv all.ps',shell=True )
    p.wait()
    


if __name__ == '__main__':
	if len(sys.argv)==1:
		print 'Usage HistogramCompare FILES'
		sys.exit(0)
	fig=compareAllPlots(sys.argv[1:])
	fig.show()
	raw_input()



