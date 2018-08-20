import ROOT
ROOT.gROOT.SetBatch(True)
import HistogramTools as HT
import sys
import math
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!

import pylab 
import numpy as np

#ratio limit of central/error, if this is small, this is a 
#sign that there is  not much statistic in this bin
centralToErrorRatioCutoff=5
#averageMethod='errorWeighted'
averageMethod='relativeErrorWeighted'
#averageMethod='normal'


#to use root  to plot
useROOT=False


from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--process", dest="process",
                  help="sets the process name")
parser.add_option("-s", "--part", dest="part",
                  help="sets the part")
parser.add_option("-e", "--energy", dest="energy",
                  help="sets the energy")

(options, args) = parser.parse_args()


rootFilenames=args

firstHistogramsList=HT.getHistogramsListWithoutPDFandScale(rootFilenames[0])

histogramsList=[h for h in firstHistogramsList if h[0]=='h' or h[0]=='x']



#print histogramsList


def fs(rootFilenames):
    for f in rootFilenames:
        rf=ROOT.TFile(f)
        yield rf
        rf.Close()


if useROOT:
    errors=ROOT.TH1D('errors','errors',50,-10,10)
    can=ROOT.TCanvas("c1") 


histograms={}

logsigmas=[]
lss=[list() for f in rootFilenames ]

for hist in histogramsList:
    histograms[hist]=list()

outfile=ROOT.TFile('dump','recreate')

for n,f in enumerate(fs(rootFilenames)):
    for hist in histogramsList:
        outfile.cd()
        histtype=type(f.Get(hist))
        newh=histtype(f.Get(hist))
        histograms[hist].append(newh)


try:
    PROCESS,ENERGY,PART=tuple(rootFilenames[0].split('_')[:-2]) 
except:
    PROCESS,ENERGY,PART=['unknown']*3

if (options.process):
    PROCESS=options.process
if (options.part):
    PART=options.part
if (options.process):
    ENERGY=options.energy

#print ENERGY,PROCESS,PART
#sys.exit(1)


for hindex,hist in enumerate(histogramsList):
    Nbins=histograms[hist][0].GetNbinsX()
    local_lss=[]
    for ibin in range(1,Nbins+1):
        s=0
        s2=0
        ws=0
        ces=[]
        for ih,h in enumerate(histograms[hist]):
            try:
                c,e,n=h.GetBinContent(ibin),h.GetBinError(ibin),h.getNbrEntries(ibin)
            except:
                c,e,n=h.GetBinContent(ibin),h.GetBinError(ibin),0
            ces.append( (c,e,n,ih))
            #print c,e

            if c!=0:
                if e!=0:
                    if averageMethod=='errorWeighted':
                        weight=abs(1/e)
                    if averageMethod=='relativeErrorWeighted':
                        weight=abs(c/e)
                    if averageMethod=='normal':
                        weight=1
                    s+=c*weight
                    ws+=weight
                    s2+=c*c
                else:
                    if n==1:  # take the error to be the central value
                        s+=c*abs(1/c)
                        ws+=abs(1/c)
                    else:    
                        print "zero error for: c: %e e: %e n: %d" % (c,e,n)
        if ws!=0:
            average=s/ws
        else:
            average=s/len(ces)
        #var=math.sqrt(s2/len(ces)-math.pow(s/len(ces),2))
        #print s,average
        for c,e,n,ih in ces:
            if e==0:
                sigma=0
            else:
                errorRatio=abs(c)/abs(e)
                #if this ratio is small, it is a sign that the statistics is poor for this bin
                if errorRatio<centralToErrorRatioCutoff:
                    sigma=0
                else:
                    sigma=abs(c-average)/float(e)
                if sigma >5:
                    print "%s: bin %d  file: %s" % (hist,ibin,rootFilenames[ih].split('_')[-1].split('.')[0])
                    print "c: %e e: %e average: %e sigma: %f (n: %d)" % (c,e,average,sigma,n)
#                else:
#                    print "GOOD: c: %e e: %e average: %e sigma: %f (n: %d)" % (c,e,average,sigma,n)       
            if sigma!=0 and c!=0: 
                if useROOT:
                    errors.Fill(math.log(sigma))
                logsigmas.append(math.log(sigma))
                lss[ih].append(math.log(sigma))
                local_lss.append(math.log(sigma))
    matplotlib.rc('xtick', labelsize=5) 
    matplotlib.rc('ytick', labelsize=5)     
    ax=pylab.subplot(8,4,hindex+1)
    ax.set_title(hist,fontsize=5)

     #pylab.set_tick_params(axis='both',labelsize=5)
    if local_lss:
        n, bins, patches = pylab.hist(local_lss, np.arange(-7,4,0.2), normed=1, histtype='step',label='all')
    #print 'lenght local_lss',len(local_lss)
    xs=np.arange(-7,4,0.02)
    ys = [ math.sqrt(2.0/math.pi)*math.exp(y)*math.exp(-math.exp(2*y)/2.0)  for y in xs]
    pylab.plot(xs, ys, 'r-')
    pylab.ylim(ymin=0)

pylab.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.5)    
pylab.suptitle('Process: %s  Energy: %s  part: %s ' % (PROCESS,ENERGY,PART))


#pylab.tick_params(axis='both', which='minor', labelsize=5)
pylab.draw()
pylab.savefig('errors_hist.pdf')
pylab.close()
#l = pylab.plot(bins, y, 'k--', linewidth=1.5)
pylab.draw()

    


if useROOT:
    errors.Draw()
    can.Print('errors.pdf')

matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15)     
        
pylab.suptitle('Process: %s  Energy: %s  part: %s '  % (PROCESS,ENERGY,PART))

if logsigmas:
    n, bins, patches = pylab.hist(logsigmas, np.arange(-7,4,0.2), normed=1, histtype='step',label='all')
xs=np.arange(-7,4,0.02)
ys = [ math.sqrt(2.0/math.pi)*math.exp(y)*math.exp(-math.exp(2*y)/2.0)  for y in xs]
pylab.plot(xs, ys, 'r--')
pylab.legend(loc='upper left')

#l = pylab.plot(bins, y, 'k--', linewidth=1.5)
pylab.draw()
pylab.savefig('errors.pdf')

for i,lssi in enumerate(lss):
    if lssi:
        n, bins, patches = pylab.hist(lssi, np.arange(-7,4,0.4), normed=1, histtype='step',label=rootFilenames[i].split('_')[-1].split('.')[0])

pylab.legend(loc='upper left')


pylab.savefig('errors_detailed.pdf')


