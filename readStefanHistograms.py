
from ROOT import gROOT, TH1D, TFile
import re
import sys


gROOT.Reset()


if (len(sys.argv) != 4):
        print "Usage: ",sys.argv[0]," INPUTFILE HISTNAME ROOTFILE"
        sys.exit(1)     
         


dataFileName=sys.argv[1]
file = TFile(sys.argv[3],'UPDATE')
histogramName = sys.argv[2]
histogramDescription = histogramName
datafile = open(dataFileName)

text = datafile.read()

#print text



def doubleRegex(name):
    return r'(?P<%s>-?[0-9]*\.?[0-9]+(e(\+|-)\d+)?)' % name


dataLineString = r'^'+doubleRegex(r'bin') +r'\s+' + doubleRegex('value') +r'\s+' + doubleRegex('error') +r'.*$' 

dataLineRegex=re.compile(dataLineString,re.MULTILINE)

data = re.finditer(dataLineRegex, text)

bins=list()
values=list()
errors=list()

if data:
    next(data)

for match in data:
        bin=match.group('bin')
        value=match.group('value')
        error=match.group('error')
        bins.append(float(bin)) 
        values.append(float(value))     
        errors.append(float(error))     
        print match.group().__repr__()
	print 'bin: ',bin,' value ',value,' err ',error  
	



#print bins
#print values
#print errors
dx= bins[1]-bins[0]
for i in range(0,len(bins)-1):
        if (abs((bins[i+1]-bins[i])/dx -1) >0.0001):
                print "bin spacing is not constant: ",bins[i+1]-bins[i],'!=',   dx      
                print "relative difference: ",abs((bins[i+1]-bins[i])/dx        ) -1
                #sys.exit(1)             
		raise



hist = TH1D( histogramName, histogramDescription,len(bins)-1 ,bins[0] , bins[-1] )
print "bin 0: ",bins[0] ,"last bin: ", bins[-1], "nbr: ",len(bins)-1 

for i in range(0,len(bins)):
        hist.SetBinContent(i+1,values[i])
        hist.SetBinError(i+1,errors[i])

hist.Write()


