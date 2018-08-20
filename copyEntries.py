import re
import sys

import ROOT

sys.path.append('/mt/data-grid/daniel/NtuplesAnalysis/install_dir/lib')

import NtuplesAnalysis as NA
import analysisTools as AT


if len(sys.argv)!=4:
    print 'usage: %s INPUTFILE ENTRIESFILE OUTPUTFILE ' 
    sys.exit(1)
inFile=sys.argv[1]
outFile=sys.argv[3]
#analysisFile='Sebastian.m4' #could be taken from the rootFile
entriesFile=sys.argv[2]

entriesFile=open(entriesFile)
lines=entriesFile.readlines()
entries=[]

completeLineRegex=re.compile('(?P<iEntry>\d+)\s+(?P<LSi>\d+)\s+(?P<Evid>\d+)')
simpleLineRegex=re.compile('(?P<entry>\d+)')

lastDone=-1

for l in lines:
    matchC=completeLineRegex.match(l)
    matchS=simpleLineRegex.match(l)
    if matchC:
        ii=int(matchC.group('LSi'))
        if ii !=lastDone:
            entries.append(ii)
            lastDone=ii
    if matchS:
        ii=int(matchS.group('entry'))
        if ii !=lastDone:
            entries.append(ii)
            lastDone=ii



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

ms=ROOT.MyStruct()

tree.SetBranchAddress('nuwgt',ROOT.AddressOf(ms,'n'))
tree.SetBranchAddress('weight',ROOT.AddressOf(ms,'w'))
tree.SetBranchAddress('weight2',ROOT.AddressOf(ms,'w2'))
tree.SetBranchAddress('me_wgt',ROOT.AddressOf(ms,'mw'))
tree.SetBranchAddress('me_wgt2',ROOT.AddressOf(ms,'mw2'))
tree.SetBranchAddress('usr_wgts',ROOT.AddressOf(ms,'uw'))f
actor=float(len(entries)/float(tree.GetEntries()))

for i in entries:
    tree.GetEntry(i)
    ms.w=factor*ms.w
    ms.w2=factor*ms.w2
    ms.mw=factor*ms.mw
    ms.mw2=factor*ms.mw2
    for i in range(ms.n):
        ms.uw[i]=factor*ms.uw[i]
    newTree.Fill()
    #print 'copy enty: %s ' % i


    

newTree.Write()
fout.Close()




#PD = NA.ProcessDescription()
#NA.getProcessDescriptionFromFile(analysisFile,PD)

#print list(PD.particleNames)
#Ev = NA.Event(PD)
#PD,Ev,RR=AT.prepareAnalysis(analysisFile,inFile)



#runInfo = NA.runInfoStruct() 
#runInfo.filename = inFile
#runInfo.isFilelist = False

#RR = NA.RootFileReader(runInfo,Ev)


