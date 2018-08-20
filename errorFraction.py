# this should be called from the directory
# with all the histograms_*.root files

import re
import math
import sys 
import ROOT
import pylab as pl
import numpy as np
import numpy.random
import HistogramTools as HT

colors=["MediumSeaGreen","MidnightBlue","Crimson","SteelBlue","Orange","MediumPurple", "DarkGray"]

allColors=['automatic'                 
,   'aliceblue'             
,   'antiquewhite'          
,   'aqua'                  
,   'aquamarine'            
,   'azure'                 
,   'beige'                 
,   'bisque'                
,   'black'                 
,   'blanchedalmond'        
,   'blue'                  
,   'blueviolet'            
,   'brown'                 
,   'burlywood'             
,   'cadetblue'             
,   'chartreuse'            
,   'chocolate'             
,   'coral'                 
,   'cornflowerblue'        
,   'cornsilk'              
,   'crimson'               
,   'cyan'                  
,   'darkblue'              
,   'darkcyan'              
,   'darkgoldenrod'         
,   'darkgray'              
,   'darkgreen'             
,   'darkgrey'              
,   'darkkhaki'             
,   'darkmagenta'           
,   'darkolivegreen'        
,   'darkorange'            
,   'darkorchid'            
,   'darkred'               
,   'darksalmon'            
,   'darkseagreen'          
,   'darkslateblue'         
,   'darkslategray'         
,   'darkslategrey'         
,   'darkturquoise'         
,   'darkviolet'            
,   'deeppink'              
,   'deepskyblue'           
,   'dimgray'               
,   'dimgrey'               
,   'dodgerblue'            
,   'firebrick'             
,   'floralwhite'           
,   'forestgreen'           
,   'fuchsia'               
,   'gainsboro'             
,   'ghostwhite'            
,   'gold'                  
,   'goldenrod'             
,   'gray'                  
,   'green'                 
,   'greenyellow'           
,   'grey'                  
,   'honeydew'              
,   'hotpink'               
,   'indianred'             
,   'indigo'                
,   'ivory'                 
,   'khaki'                 
,   'lavender'              
,   'lavenderblush'         
,   'lawngreen'             
,   'lemonchiffon'          
,   'lightblue'             
,   'lightcoral'            
,   'lightcyan'             
,   'lightgoldenrodyellow'  
,   'lightgray'             
,   'lightgreen'            
,   'lightgrey'             
,   'lightpink'             
,   'lightsalmon'           
,   'lightseagreen'         
,   'lightskyblue'          
,   'lightslategray'        
,   'lightslategrey'        
,   'lightsteelblue'        
,   'lightyellow'           
,   'lime'                  
,   'limegreen'             
,   'linen'                 
,   'magenta'               
,   'maroon'                
,   'mediumaquamarine'      
,   'mediumblue'            
,   'mediumorchid'          
,   'mediumpurple'          
,   'mediumseagreen'        
,   'mediumslateblue'       
,   'mediumspringgreen'     
,   'mediumturquoise'       
,   'mediumvioletred'       
,   'midnightblue'          
,   'mintcream'             
,   'mistyrose'             
,   'moccasin'              
,   'navajowhite'           
,   'navy'                  
,   'oldlace'               
,   'olive'                 
,   'olivedrab'             
,   'orange'                
,   'orangered'             
,   'orchid'                
,   'palegoldenrod'         
,   'palegreen'             
,   'paleturquoise'         
,   'palevioletred'         
,   'papayawhip'            
,   'peachpuff'             
,   'peru'                  
,   'pink'                  
,   'plum'                  
,   'powderblue'            
,   'purple'                
,   'red'                   
,   'rosybrown'             
,   'royalblue'             
,   'saddlebrown'           
,   'salmon'                
,   'sandybrown'            
,   'seagreen'              
,   'seashell'              
,   'sienna'                
,   'silver'                
,   'skyblue'               
,   'slateblue'             
,   'slategray'             
,   'slategrey'             
,   'snow'                  
,   'springgreen'           
,   'steelblue'             
,   'tan'                   
,   'teal'                  
,   'thistle'               
,   'tomato'                
,   'turquoise'             
,   'violet'                
,   'wheat'                 
,   'white'                 
,   'whitesmoke'            
,   'yellow'                
,   'yellowgreen'     
]



#ROOT.gSystem.Load('/home/daniel/workspace/NtuplesAnalysis/build_desktops/install_dir/lib/libAnalysis.so')


import os
files=os.listdir(".")

histRegex=re.compile(r'histograms_(?P<part>.*)\.root\Z')

matches=[histRegex.match(f) for f in files]
parts=[ m.group('part') for m in matches if m ]

print parts

if len(parts)==0:
    print "no histograms found!"
    sys.exit(1)




if len(sys.argv)<=1:
   print "Need one histogram name, choices are:"
   print HT.getHistogramsListWithoutPDFandScale(fc) 
   sys.exit(1)
else:
    histogram=sys.argv[1]

if len(sys.argv)>2:
    parts=sys.argv[2:]
    print "parts: %s" % parts 

fs=[ROOT.TFile('histograms_%s.root' % part) for part in parts]
fc=ROOT.TFile('combinedNLO.root') 


hc=fc.Get(histogram)
hs=[f.Get(histogram) for f in fs]
nbrBins=hs[0].GetNbinsX()+2

errors=[[] for i in range(len(parts))]
centrals=[[] for i in range(len(parts))]
total=[]
totalErrors=[]
bincenters=[[] for i in range(len(parts))]
for i in range(nbrBins):
    total.append(hc.GetBinContent(i))
    totalErrors.append(hc.GetBinError(i))

    for c,e,h,bc in zip(centrals,errors,hs,bincenters):
        e.append(h.GetBinError(i))
        c.append(h.GetBinContent(i))
        bc.append(hc.GetBinCenter(i))



def ratioSq(p,t):
    if t!=0:
        return p*p/(t*t)
    else:
        return 0

ratios=[[ratioSq(p,t) for p,t in zip(errorsPart,totalErrors)] for errorsPart in errors]
cumul=[[ sum(rs[:n]) for n in range(len(rs)+1)]  for rs in zip(*ratios)]

boundaries=[ [ i for i in c for doItTwice in [1,2]] for c in zip(*cumul[1:-1])]

fig=pl.figure()

plt=pl.axes([0.1,0.4,0.8,0.5])
pltr=pl.axes([0.1,0.1,0.8,0.3],sharex=plt)


def normalize(n,d):
    if d==0:
        return 0
    else:
        return n/d

theColors=[]
for i in range(len(parts)):
    if i < len(colors):
        theColors.append(colors[i])
    else:
        theColors.append(numpy.random.rand(3,))

print parts
print total
print errors

for i in range(len(parts)):
    plt.errorbar(bincenters[i],[normalize(c,t) for c,t in zip(centrals[i],total)],yerr=[normalize(c,t) for c,t in zip(errors[i],total)], color=theColors[i],label=parts[i], fmt = '.')


a=hs[0].GetXaxis()
xs=[ fn(i) for i in range(1,nbrBins-1) for fn in [a.GetBinLowEdge,a.GetBinUpEdge]]



for i in range(len(parts)):
    pltr.fill_between(xs,boundaries[i],boundaries[i+1],color=theColors[i],label=parts[i])

pltr.set_ylim([0,1])
legend=plt.legend(loc='best', shadow=True, fancybox=True)

print 'ok'
fig.savefig('error.pdf')




