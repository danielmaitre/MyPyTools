import sys
import math
import BHtools as BHT
import BH





p = BH.cvar.p
m = BH.cvar.m
PRO = BH.process(p,m,p,m,p,p)
A=BH.TreeHelAmpl(PRO)
ind = BH.vectori([1,2,3,4,5,6])

RG=BH.GMP_random()
RGr = RG.random

import rambo 




def treetest():
    nbr=20
    r=[None]*nbr
    for i in range(1,nbr):
        RG.seed(123456)
        BH.RGMP_set_precision(200*i)
        ps =rambo.PS(6,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
        cms = [ BH.Cmomgmp(*p) for p in ps ]
        mc = BH.mcgmp(*cms)
        r[i-1] = A.eval(mc,ind)

    for i in range(nbr-2):
        d=abs(r[i+1]-r[i])
        prec=-BH.log10(d)
        print "%s: %s" % (i,prec.to_double())

nbr=15
r=[None]*nbr
print "   "

AA=BH.One_Loop_Helicity_Amplitude(PRO,BH.nf)

cc=AA.cut_part()
cp=cc.makeDarrenCutPart()

bub=[x[:] for x in [ [None]*nbr]*cp.nbr_bubbles()]
tri=[x[:] for x in [ [None]*nbr]*cp.nbr_triangles()]
box=[x[:] for x in [ [None]*nbr]*cp.nbr_boxes()]


def printCutInfo():
    for i in range(1,nbr):
        RG.seed(123456)
        BH.RGMP_set_precision(75*i)
        ps =rambo.PS(6,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
        cms = [ BH.Cmomgmp(*p) for p in ps ]
        mc = BH.mcgmp(*cms)
        for b in range(1,cp.nbr_bubbles()+1):
            #print " Bubble %s" % b
            bb=cp.bubble(b)
            res=bb.eval(mc,ind)
            bub[b-1][i-1] = res 
        for b in range(1,cp.nbr_triangles()+1):
            #print " Triangle %s" % b
            bb=cp.triangle(b)
            res=bb.eval(mc,ind)
            tri[b-1][i-1] = res 
        for b in range(1,cp.nbr_boxes()+1):
            #print " Box %s" % b
            bb=cp.box(b)
            res=bb.eval(mc,ind)
            box[b-1][i-1] = res 

    for b in range(1,cp.nbr_bubbles()+1):
        print "bubble %s" % b
        for i in range(nbr-2):
            d=abs(bub[b-1][i+1]-bub[b-1][i])
            prec=-BH.log10(d)
            print "%s: %s" % (i,prec.to_double())
    for b in range(1,cp.nbr_triangles()+1):
        print "triangle %s: %s" % (b,(tri[b-1][0]))
        for i in range(nbr-2):
            d=abs(tri[b-1][i+1]-tri[b-1][i])
            prec=-BH.log10(d)
            print "%s: %s" % (i,prec.to_double())
    for b in range(1,cp.nbr_boxes()+1):
        print "box %s" % b
        for i in range(nbr-2):
            d=abs(bub[b-1][i+1]-bub[b-1][i])
            prec=-BH.log10(d)
            print "%s: %s" % (i,prec.to_double())


for i in range(1,nbr):
    RG.seed(123456)
    BH.RGMP_set_precision(200*i)
    ps =rambo.PS(6,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
    cms = [ BH.Cmomgmp(*p) for p in ps ]
    mc = BH.mcgmp(*cms)
    res=AA.eval(mc,ind)
    print res[0]
    rr=res[-2].real()
    r[i-1] =res 


print "Double pole:"
for i in range(nbr-2):
    d=abs(r[i+1][-2]-r[i][-2])
    prec=-BH.log10(d)
    print "%s: %s" % (i,prec.to_double())
print "Single pole:"
for i in range(nbr-2):
    d=abs(r[i+1][-1]-r[i][-1])
    prec=-BH.log10(d)
    print "%s: %s" % (i,prec.to_double())
print "finite:"
for i in range(nbr-2):
    d=abs(r[i+1][0]-r[i][0])
    prec=-BH.log10(d)
    print "%s: %s" % (i,prec.to_double())

