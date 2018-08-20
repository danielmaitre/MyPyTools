import re
import sys

import ROOT

sys.path.append('/mt/data-grid/daniel/NtuplesAnalysis/install_dir/lib')

import NtuplesAnalysis as NA
import analysisTools as AT


#if len(sys.argv)!=4:
#    print 'usage: %s INPUTFILE ENTRIESFILE OUTPUTFILE ' 
#    sys.exit(1)

inFile="/home/daniel/Minlo/small.root"
outFile="/home/daniel/Minlo/test.root"
#analysisFile='Sebastian.m4' #could be taken from the rootFile






fin=ROOT.TFile(inFile)
tree=fin.Get('BHSntuples')

fout=ROOT.TFile(outFile,'recreate')

newTree=tree.CloneTree(0)

#weight1=ROOT.Double_t(0.0)
weight1=float(0.0)


ROOT.gROOT.ProcessLine(\
  "struct MyStruct{\
  Int_t n;\
    Double_t w;\
        Double_t w2;\
        Double_t mw;\
                Double_t mw2;\
        Double_t uw[18];\
        };")

ROOT.gROOT.ProcessLine(\
"struct NtupleInfo {\
	double wgt;\
	double wgt2;\
	double muF;\
	double muR;\
	double muF2;\
	double muR2;\
	Int_t id;\
	float px[100];\
	float py[100];\
	float pz[100];\
	float E[100];\
	int kf[100];\
	int nparticle;\
	int id1,id2;\
	double x1,x2;\
	double x1p,x2p;\
	double me_wgt,me_wgt2;\
	int numgt;\
	double usr_wgts[18];\
  double alphas;\
	int alphasPower;\
 };\
")

ni=ROOT.NtupleInfo()

tree.SetBranchAddress('id',ROOT.AddressOf(ni,'id'))
tree.SetBranchAddress('nuwgt',ROOT.AddressOf(ni,'numgt'))
tree.SetBranchAddress('nparticle',ROOT.AddressOf(ni,'nparticle'))
tree.SetBranchAddress('px',ROOT.AddressOf(ni,'px'))
tree.SetBranchAddress('py',ROOT.AddressOf(ni,'py'))
tree.SetBranchAddress('pz',ROOT.AddressOf(ni,'pz'))
tree.SetBranchAddress('E',ROOT.AddressOf(ni,'E'))
tree.SetBranchAddress('kf',ROOT.AddressOf(ni,'kf'))
tree.SetBranchAddress('x1',ROOT.AddressOf(ni,'x1'))
tree.SetBranchAddress('x2',ROOT.AddressOf(ni,'x2'))
tree.SetBranchAddress('id1',ROOT.AddressOf(ni,'id1'))
tree.SetBranchAddress('id2',ROOT.AddressOf(ni,'id2'))
tree.SetBranchAddress('alphasPower',ROOT.AddressOf(ni,'alphasPower'))
tree.SetBranchAddress('weight',ROOT.AddressOf(ni,'wgt'))
tree.SetBranchAddress('weight2',ROOT.AddressOf(ni,'wgt2'))
tree.SetBranchAddress('me_wgt',ROOT.AddressOf(ni,'me_wgt'))
tree.SetBranchAddress('me_wgt2',ROOT.AddressOf(ni,'me_wgt2'))
tree.SetBranchAddress('alphas',ROOT.AddressOf(ni,'alphas'))
tree.SetBranchAddress('fac_scale',ROOT.AddressOf(ni,'muF'))
tree.SetBranchAddress('ren_scale',ROOT.AddressOf(ni,'muR'))


#sys.exit(1)


infile=open("PSpoints")

txt=infile.read()



dr=r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
ir=r"[+-]? *(\d+)"
ParticleRegex=r"Particle \d\s+:\s+%s\s+%s\s+%s\s+%s" % (dr,dr,dr,dr) 
FlavorsRegex=r"Flavours:\s*(?:\s+-?\d+)+$" 
pspoint=re.compile('New born event.*?inlofac',re.DOTALL)

iEntry=1

for m in pspoint.finditer(txt): 
    ni.id=iEntry
#    print iEntry
    iEntry+=1
    particles=re.findall(ParticleRegex,m.group())
    flavors=re.findall(FlavorsRegex,m.group(),re.M)

    psstring = [ re.findall(dr, p)[1:] for p in particles ]
    fsstring = re.findall(dr, flavors[0])
    ps =[ [float(s) for s in p ] for p in psstring ]
    fs1 =[int(s) for s in  fsstring ]
    fs=[ 21 if x==0 else x for x in fs1]

    for n,p in enumerate(ps[2:]):
        ni.E[n]=p[0]
        ni.px[n]=p[1]
        ni.py[n]=p[2]
        ni.pz[n]=p[3]
        for n,f in enumerate(fs[2:]):
            ni.kf[n]=f
    
    ni.id1=fs[0]
    ni.id2=fs[1]
    ni.x1=ps[0][0]/3500
    ni.x2=ps[1][0]/3500

    ni.nparticle=len(ps)-2

    ni.wgt=1
    ni.wgt2=1
    ni.me_wgt=1
    ni.me_wgt2=1
    ni.alphas=0.118

    ni.alphasPower=1

    ni.muF=91
    ni.muR=91
    
    ni.numgt=0
    newTree.Fill()

newTree.Write()
fout.Close()




