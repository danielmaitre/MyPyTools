import sys





def getXsection(filename):
    f=open(filename,'r')
    lines=f.readlines()

    _,labelsTxt=lines[0].split(':')
    labels=[l.split('[')[0] for l in labelsTxt.split()]
    _,neval=lines[1].split(':')
    neval=int(neval)
    values=list(map(float,lines[2].split()))

    if len(values)!=len(labels):
        print( "labels length ({0}) is not the same as values length ({1})".format(len(labels),len(values)) )

    return dict(zip(labels,values))




def getHist(filename):
    f=open(filename,'r')
    lines=f.readlines()

    _,labelsTxt=lines[0].split(':')
    labels=[l.split('[')[0] for l in labelsTxt.split()]
    _,neval=lines[1].split(':')

    neval=int(neval)
    # old NNLOjet: lines[2] is overflow, not interested yet
    # new, values are in line 2
    okLines = [l for l in lines if l[0]!='#']
    allvalues = [list(map(float,l.split())) for l in okLines]
    for values in allvalues:
        if len(values)!=len(labels):
               print( "labels length ({0}) is not the same as values length ({1})".format(len(labels),len(values)) )

    return dict(zip(labels,zip(*allvalues)))

if __name__=="__main__":
    h=getHist('../NNLOjet/RRa//PDF0_dir/1jet.13R7_RR.RRa.xptj1_y1.s1.dat')
    xs=getXsection('../NNLOjet/RRa//PDF0_dir/1jet.13R7_RR.RRa.cross.s1.dat')
