import sys

import HistogramTools  as HT

x,v,e=HT.getData(sys.argv[1],sys.argv[2])
width=[x[i+1]-x[i] for i in range(len(x)-1)]
bins=[vv*ww for vv,ww in zip(v[1:-1],width)]
#print width
#print v[1:-1]
#print bins
print sum(bins)


