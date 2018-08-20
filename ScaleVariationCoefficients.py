import sys
import math
sys.path.append('/home/daniel/workspace/BHlib/build/lib/')
sys.path.append('/home/daniel/workspace/BHlib/my_programs')
import BH


import rambo 
from fractions import Fraction

BHI=BH.BH_interface()



class res(): pass

def getCoeffs(A,ps,mu=100):
    bi=BH.BHinput(BH.vectorm(ps),mu)
    bi1=BH.BHinput(BH.vectorm(ps),math.e*mu)
    bi2=BH.BHinput(BH.vectorm(ps),math.e*math.e*mu)
    bi3=BH.BHinput(BH.vectorm(ps),math.e*math.e*math.e*mu)

    BHI(bi1)
    a0_1=A.get_finite()
    a1_1=A.get_single_pole()
    a2_1=A.get_double_pole()

    BHI(bi2)
    a0_2=A.get_finite()
    a1_2=A.get_single_pole()
    a2_2=A.get_double_pole()

    BHI(bi3)
    a0_3=A.get_finite()
    a1_3=A.get_single_pole()
    a2_3=A.get_double_pole()

    #compute this one last

    BHI(bi)
    A(bi)
    a0=A.get_finite()
    a1=A.get_single_pole()
    a2=A.get_double_pole()

    # fit coefficients
    c1=(a0_2-4*a0_1+3*a0)/(-4)
    c2=(a0_2-2*a0_1+a0)/4

    print "Check of the fit..."
    fitOK=True
    if ((a0+2*c1+2*c2)-(a0_1))/a0_1 > 0.0000001:
        print "These should be the same: %s , %s" % (a0+2*c1+2*c2,a0_1)
        fitOK=False
    if ((a0+4*c1+8*c2)-(a0_2))/a0_2 > 0.0000001:
        print "These should be the same: %s , %s" % (a0+4*c1+8*c2,a0_2)
        fitOK=False
    if ((a0+6*c1+18*c2)-(a0_3))/a0_3 > 0.0000001:
        print "These should be the same: %s , %s" % (a0+6*c1+18*c2,a0_3)
        fitOK=False

    if fitOK:
            print "Fit OK"

    r = res()

    r.a0=a0
    r.a1=a1
    r.a2=a2
    r.c1=c1
    r.c2=c2
    r.C0=A.getScaleVariationCoefficient(0)
    r.C1=A.getScaleVariationCoefficient(1)
    r.C2=A.getScaleVariationCoefficient(2)
    return r


def genMomenta(n):
    psAllIncoming =rambo.PS(n)
    ps=[
        [-x for x in psAllIncoming[0]],
        [-x for x in psAllIncoming[1]]
         ] +psAllIncoming[2:]
    return ps

colorModeMap={
    'full' : 'full_color',
    'lc' : 'leading_color',
    'fmlc' : 'full_minus_leading_color',
    }

def findCoeffsColor(pdgCode,nAlphas,color):
    BH.use_setting("NUMBER_OF_WARMUP_POINTS 0")
    BH.use_setting("SET_ALL_RAT_TO_ZERO yes")
    BH.use_setting("COLOR_MODE %s" % colorModeMap[color])
    A=BHI.new_ampl(BH.vectori(pdgCode))

    Nps=len(pdgCode)

    ps=genMomenta(Nps)
    r=getCoeffs(A,ps)
    ps2=genMomenta(Nps)
    r2=getCoeffs(A,ps2)
    diff = abs((r.c1-r.a1)-(r2.c1-r2.a1))
    scale = (abs(r.c1)+abs(r.a1)+abs(r2.c1)+abs(r2.a1))/4
    if ( abs(diff)/scale ) < 0.00000001 :
        # constant shift
        c0=0
    else:
        c0=(diff)/(r.a2-r2.a2)
    c1=(r.c1-r.a1)-c0*r.a2
    print "%s: c_1= a_1 + %s + %s * a_2" % (color,Fraction(c0).limit_denominator(100000),Fraction(c1).limit_denominator(100000))

def findCoeffs(pdgCode,nAlphas,onlyLC=False):
    if onlyLC:
        findCoeffsColor(pdgCode,nAlphas,'lc')
    else:
        findCoeffsColor(pdgCode,nAlphas,'full')
        findCoeffsColor(pdgCode,nAlphas,'lc')
        findCoeffsColor(pdgCode,nAlphas,'fmlc')
##    BH.use_setting("NUMBER_OF_WARMUP_POINTS 0")
##    BH.use_setting("SET_ALL_RAT_TO_ZERO yes")
##
##    if not onlyLC:
##        BH.use_setting("COLOR_MODE full_color")
##        A=BHI.new_ampl(BH.vectori(pdgCode))
##
##    BH.use_setting("COLOR_MODE leading_color")
##    Alc=BHI.new_ampl(BH.vectori(pdgCode))
##    if not onlyLC:
##        BH.use_setting("COLOR_MODE full_minus_leading_color")
##        Afmlc=BHI.new_ampl(BH.vectori(pdgCode))
##
##    Nps=len(pdgCode)
##
##    ps=genMomenta(Nps)
##    if not onlyLC: r=getCoeffs(A,ps)
##    rlc=getCoeffs(Alc,ps)
##    if not onlyLC: rfmlc=getCoeffs(Afmlc,ps)
##
##    ps2=genMomenta(Nps)
##    if not onlyLC: r2=getCoeffs(A,ps2)
##    r2lc=getCoeffs(Alc,ps2)
##    if not onlyLC: r2fmlc=getCoeffs(Afmlc,ps2)
##
##    if not onlyLC:
##        f1=Fraction(r.c1-r.a1).limit_denominator(10000)/nAlphas
##
##        if not f1 == Fraction(23,6):
##            print 'Problem, we should get beta_0 here and we get %s' % f1
##
##    c_lc=((rlc.c1-rlc.a1)-(r2lc.c1-r2lc.a1))/(rlc.a2-r2lc.a2)
##    if not onlyLC: c_fmlc=((rfmlc.c1-rfmlc.a1)-(r2fmlc.c1-r2fmlc.a1))/(rfmlc.a2-r2fmlc.a2)
##
##
##    c2_lc=(rlc.c1-rlc.a1)-c_lc*rlc.a2
##    if not onlyLC: c2_fmlc=(rfmlc.c1-rfmlc.a1)-c_fmlc*rfmlc.a2
##    # don't expect the sum to be the full answer as the a_2 are different
##    if not onlyLC: print "full: c_1= a_1 + %s * %s " % (nAlphas,f1)
##    print "lc: c_1= a_1 + %s + %s * a_2" % (Fraction(c2_lc).limit_denominator(100000),Fraction(c_lc).limit_denominator(100000))
##    if not onlyLC: print "fmlc: c_1= a_1 + %s + %s * a_2" % (Fraction(c2_fmlc).limit_denominator(100000),Fraction(c_fmlc).limit_denominator(100000))

def checkCoeffs(pdgCode,nAlphas,onlyLC=False):
    BH.use_setting("NUMBER_OF_WARMUP_POINTS 0")
    BH.use_setting("SET_ALL_RAT_TO_ZERO yes")


    Nps=len(pdgCode)
    ps=genMomenta(Nps)

    if not onlyLC:
        BH.use_setting("COLOR_MODE full_color")
        A=BHI.new_ampl(BH.vectori(pdgCode))
        r=getCoeffs(A,ps)

    BH.use_setting("COLOR_MODE leading_color")
    Alc=BHI.new_ampl(BH.vectori(pdgCode))
    rlc=getCoeffs(Alc,ps)

    if not onlyLC:
        BH.use_setting("COLOR_MODE full_minus_leading_color")
        Afmlc=BHI.new_ampl(BH.vectori(pdgCode))
        rfmlc=getCoeffs(Afmlc,ps)


    print "log^1 "
    if not onlyLC: print 'full: c1 from the fit: %s  from BH: %s' % (r.c1,r.C1)
    print 'LC:   c1 from the fit: %s  from BH: %s' % (rlc.c1,rlc.C1)
    if not onlyLC: print 'fmLC: c1 from the fit: %s  from BH: %s' % (rfmlc.c1,rfmlc.C1)
    print "log^2 "
    if not onlyLC: print 'full: c2 from the fit: %s  from BH: %s' % (r.c2,r.C2)
    print 'LC:   c2 from the fit: %s  from BH: %s' % (rlc.c2,rlc.C2)
    if not onlyLC: print 'fmLC: c2 from the fit: %s  from BH: %s' % (rfmlc.c2,rfmlc.C2)
    



#pdg_2q3g=[-1, 21, 12, -11, 21, 21, -2]

#findCoeffs(pdg_2q3g,3)

