import numpy as np
import pylab
import math
import NNLOjetHistogramTool
import raoulHistogramTool

def double(arr):
    """
    returns an array with each entry present twice in the list
    """
    newarr = np.array([(xx,xx) for xx in arr]).ravel()
    return newarr

def makeHist(loc,x,y,**kwargs): 
    loc.plot(double(x)[1:-1],double(y),**kwargs)

def makeHistWithErr(loc,x,y,e,**kwargs): 
    '''
       Try to avoid having the label twice by removing that argument from kwargs when the error bar are drawn
    '''
    kwargsCopy=dict(kwargs)
    if "label" in kwargsCopy.keys():
        del kwargsCopy['label']
    loc.plot(double(x)[1:-1],double(y),**kwargs)
    xmid=[(x[i+1]+x[i])/2 for i in range(len(v))]
    print kwargsCopy
    loc.errorbar(x,y,yerr=e,**kwargsCopy)

def makeFill(loc,x,y1,y2,**kwargs): 
  loc.fill_between(double(x)[1:-1],double(y1),double(y2),**kwargs)

def readSherpaAnalysis(filename,part):
    f=open(filename)
    lines=f.readlines()
    _,histType,nbins,minb,maxb=lines[3].split()[:5]
    index=lines[4].split().index(part)-1
    numlines=[l.split() for l in lines[5:]]
    binEdges=[float(l[0]) for l in numlines]
    values=[ float(l[index]) for l in numlines[:-1] ]
    errors=[ float(l[index+1]) for l in numlines[:-1] ]

    if histType=='11':
        bw = np.array(binEdges[1:])-np.array(binEdges[:-1])
        binEdges=[math.pow(10.0,be) for be in binEdges]
        nbw=np.array(binEdges[1:]) - np.array(binEdges[:-1])
        factors=[old/new for old,new in zip(bw,nbw)]
        values=[v*f for f,v in zip(factors,values)]
        errors = [e * f for f, e in zip(factors, errors)]
    return binEdges,values,errors

def readNNLOjet(filename,histname,part):
    hist=NNLOjetHistogramTool.getHist(filename)
    lower=hist[histname+'_lower']
    upper=hist[histname+'_upper']
    binEdges=list(lower)+[upper[-1]]
    values=hist[part]
    errors=hist[part+'_Err']

    return binEdges,values,errors

def readRaoul(filename,histname):
    x, v, e = raoulHistogramTool.getHist(filename, histname)
    binEdges = np.array(x)
    bw = binEdges[1:]-binEdges[:-1]
    values = v[:-1]/bw
    errors = e[:-1]/bw

    return binEdges,values,errors




class ratioPlot:
    def __init__(self,title='unnamed'):
        self.bb=[]
        self.values=[]
        self.ratios=[]
        self.valuesE=[]
        self.ratiosE=[]
        self.title=title
        self.types=[]
        self.kwargs=[]
    def checkXs(self,xs,values,binWidths):
        if len(self.bb)==0:
            if len(xs)==len(values):  # these are bin centers
                self.mid=np.array(xs)
                if len(binWidths)==len(xs):
                    self.widths=np.array(binWidths)
                    self.bb=np.array([c-bw/2 for c,bw in zip(self.mid,self.widths) ]+[self.mid[-1]+0.5*self.widths[-1]])
                else:
                    print "Can't guess bin boundaries from bin centers, you need to provide a binWidth argument!"
                    raise
            if len(xs)==len(values)+1:  # these are bin boundaries
                self.bb=np.array(xs)
                self.mid=0.5*(self.bb[1:]+self.bb[:-1])
                self.widths=(self.bb[1:]-self.bb[:-1])
            self.ref=np.array(values)
        else:
            if len(xs)==len(values):  # these are bin centers
                if not (xs==self.mid).all():
                    print "can't plot things with different coordinates"
                    print "current: %s" % self.mid
                    print "other  : %s" % xs
                    print "individual :",xs==self.mid
                    
            if len(xs)+1==len(values):  # these are bin boundaries
                if not (xs==self.bb).all():
                    print "can't plot things with different coordinates"


    def addValues(self,xs,values,errors,t,binWidths,**kwargs):
        self.checkXs(xs,values,binWidths)
        self.values.append(np.array(values))
        self.valuesE.append(np.array(errors))
        self.ratios.append(np.array(values)/self.values[0])
        self.ratiosE.append(np.array(errors)/self.values[0])
        self.types.append(t)
        self.kwargs.append(kwargs)
        
    def addData(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'data',binWidths,**kwargs) 
    def addLine(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'line',binWidths,**kwargs) 
    def addFill(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'fill',binWidths,**kwargs) 

        
    def makePlot(self):
        self.fig=pylab.figure(figsize=(8,10))
        self.axrat=self.fig.add_axes([0.1,0.1,0.8,0.3])   #left, bottom, width, height
        self.ax=self.fig.add_axes([0.1,0.4,0.8,0.5])   #left, bottom, width, height

        for v,ve,r,re,t,kwargs in zip(self.values,self.valuesE,self.ratios,self.ratiosE,self.types,self.kwargs):
            if t=='line':
                styleDic = {}
                styleDic.update({
                    'linestyle':'none',
                })
                styleDic.update(kwargs)
                ret=self.ax.errorbar(self.mid,v,yerr=ve,**styleDic)
                retr=self.axrat.errorbar(self.mid,r,yerr=re,**styleDic)
                if 'color' in kwargs.keys():
                    makeHist(self.ax,self.bb,v,**kwargs)
                    makeHist(self.axrat,self.bb,r,**kwargs)
                else:
                    makeHist(self.ax,self.bb,v,color=ret[0].get_color(),**kwargs)
                    makeHist(self.axrat,self.bb,r,color=retr[0].get_color(),**kwargs)
            if t=='data':
                ret=self.ax.errorbar(self.mid,v,xerr=0.5*self.widths,yerr=ve,linestyle='none',**kwargs)
                retr=self.axrat.errorbar(self.mid,r,xerr=0.5*self.widths,yerr=re,linestyle='none',**kwargs)
            if t=='fill':
                if len(ve.shape)==1:
                    makeFill(self.ax,self.bb,v+ve,v-ve,**kwargs)
                    makeFill(self.axrat,self.bb,r+re,r-re,**kwargs)
                if len(ve.shape)==2 and ve.shape[0]==2 :
                    makeFill(self.ax,self.bb,v+ve[0],v-ve[1],**kwargs)
                    makeFill(self.axrat,self.bb,r+re[0],r-re[1],**kwargs)

                    
        self.ax.legend()
        self.ax.set_title(self.title)
        
        

    def addLineFromRoot(self,filename,histname,restrict=None,**kwargs):
        import HistogramTools as HT
        x,v,e=HT.getData(filename,histname)
        if restrict:
            i,f=restrict
            self.addLine(x,v[i:f],e[i:f],**kwargs)  # don't include over and underflow
        else:
            self.addLine(x,v[1:-1],e[1:-1],**kwargs)  # don't include over and underflow

    def addLineFromSherpa(self,filename,part,restrict=None,**kwargs):
        x,v,e=readSherpaAnalysis(filename,part)
        if restrict:
            i,f=restrict
            self.addLine(x,v[i:f],e[i:f],**kwargs)  # don't include over and underflow
        else:
            self.addLine(x,v,e,**kwargs)  # don't include over and underflow

    def addLineFromNNLOjet(self,filename,hist,part,restrict=None,**kwargs):
        x,v,e=readNNLOjet(filename,hist,part)
        if restrict:
            i,f=restrict
            self.addLine(x,v[i:f],e[i:f],**kwargs)  # don't include over and underflow
        else:
            self.addLine(x,v,e,**kwargs)  # don't include over and underflow

    def addLineFromRaoul(self,filename,hist,restrict=None,**kwargs):
        x, v, e = readRaoul(filename, hist)
        if restrict:
            i,f=restrict
            self.addLine(x,v[i:f],e[i:f],**kwargs)  # don't include over and underflow
        else:
            self.addLine(x,v,e,**kwargs)  # don't include over and underflow

            

    def saveIn(self,place):
        place.savefig(self.fig)


    def show(self):
        self.fig.show()

    def setXLim(self,lim):
        self.ax.set_xlim(lim)
        self.axrat.set_xlim(lim)

    def setYLim(self,lim):
        self.ax.set_ylim(lim)

    def setRatioYLim(self,lim):
        self.axrat.set_ylim(lim)



class Plot:
    def __init__(self,title='unnamed'):
        self.bb=[]
        self.values=[]
        self.valuesE=[]
        self.title=title
        self.types=[]
        self.kwargs=[]
    def checkXs(self,xs,values,binWidths):
        if len(self.bb)==0:
            if len(xs)==len(values):  # these are bin centers
                self.mid=np.array(xs)
                if len(binWidths)==len(xs):
                    self.widths=np.array(binWidths)
                    self.bb=np.array([c-bw/2 for c,bw in zip(self.mid,self.widths) ]+[self.mid[-1]+0.5*self.widths[-1]])
                else:
                    print "Can't guess bin boundaries from bin centers, you need to provide a binWidth argument!"
                    raise
            if len(xs)==len(values)+1:  # these are bin boundaries
                self.bb=np.array(xs)
                self.mid=0.5*(self.bb[1:]+self.bb[:-1])
                self.widths=(self.bb[1:]-self.bb[:-1])
            self.ref=np.array(values)
        else:
            if len(xs)==len(values):  # these are bin centers
                if not (xs==self.mid).all():
                    print "can't plot things with different coordinates"
                    print "current: %s" % self.mid
                    print "other  : %s" % xs
                    print "individual :",xs==self.mid
                    
            if len(xs)+1==len(values):  # these are bin boundaries
                if not (xs==self.bb).all():
                    print "can't plot things with different coordinates"


    def addValues(self,xs,values,errors,t,binWidths,**kwargs):
        self.checkXs(xs,values,binWidths)
        self.values.append(np.array(values))
        self.valuesE.append(np.array(errors))
        self.types.append(t)
        self.kwargs.append(kwargs)
        
    def addData(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'data',binWidths,**kwargs) 
    def addLine(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'line',binWidths,**kwargs) 
    def addFill(self,xs,values,errors,binWidths=[],**kwargs):
        self.addValues(xs,values,errors,'fill',binWidths,**kwargs) 

        
    def makePlot(self):
        self.fig=pylab.figure(figsize=(6,6))
        self.ax=self.fig.add_axes([0.1,0.1,0.8,0.8])   #left, bottom, width, height

        for v,ve,t,kwargs in zip(self.values,self.valuesE,self.types,self.kwargs):
            if t=='line':
                kwargsCopy=dict(kwargs)
                if "label" in kwargsCopy.keys():
                    del kwargsCopy['label']
                ret=self.ax.errorbar(self.mid,v,yerr=ve,linestyle='none',**kwargsCopy)
                if 'color' in kwargs.keys():
                    makeHist(self.ax,self.bb,v,**kwargs)
                else:
                    makeHist(self.ax,self.bb,v,color=ret[0].get_color(),**kwargs)
            if t=='data':
                ret=self.ax.errorbar(self.mid,v,xerr=0.5*self.widths,yerr=ve,linestyle='none',**kwargs)
            if t=='fill':
                makeFill(self.ax,self.bb,v+ve,v-ve,**kwargs)
            
        self.ax.legend()
        self.ax.set_title(self.title)
        
        

    def addLineFromRoot(self,filename,histname,restrict=None,**kwargs):
        import HistogramTools as HT
        x,v,e=HT.getData(filename,histname)
        if restrict:
            i,f=restrict
            self.addLine(x,v[i:f],e[i:f],**kwargs)  # don't include over and underflow
        else:
            self.addLine(x,v[1:-1],e[1:-1],**kwargs)  # don't include over and underflow

        
    def saveIn(self,place):
        place.savefig(self.fig)


    def show(self):
        self.fig.show()

