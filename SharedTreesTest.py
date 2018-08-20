import sys
sys.path.append('/home/daniel/workspace/BHlib/build/lib')

import BH
import rambo
import itertools
import re

stringToParticleMap={
    'm' : BH.cvar.m ,
    'p' : BH.cvar.p ,
    'qm' : BH.cvar.qm ,
    'qp' : BH.cvar.qp ,
    'Qm' : BH.cvar.q2m ,
    'Qp' : BH.cvar.q2p ,
    'qbm' : BH.cvar.qbm ,
    'qbp' : BH.cvar.qbp ,
    'Qbm' : BH.cvar.qb2m ,
    'Qbp' : BH.cvar.qb2p ,
    'ym' : BH.cvar.ym ,
    'yp' : BH.cvar.yp ,
    'lp' : BH.cvar.lp ,
    'lm' : BH.cvar.lm ,
    'lbp' : BH.cvar.lbp,
    'lbm' : BH.cvar.lbm
}

particleToTypeString_withoutg={
    BH.cvar.qm : 'q',
    BH.cvar.qp : 'q',
    BH.cvar.q2m : 'Q',
    BH.cvar.q2p : 'Q',
    BH.cvar.qbm : 'qb',
    BH.cvar.qbp : 'qb',
    BH.cvar.qb2m : 'Qb',
    BH.cvar.qb2p : 'Qb',
    BH.cvar.ym : 'y',
    BH.cvar.yp : 'y',
    BH.cvar.lp : 'l',
    BH.cvar.lm : 'l',
    BH.cvar.lbp : 'lb',
    BH.cvar.lbm : 'lb'
}

particleToTypeString_withoutg[BH.cvar.m]=''
particleToTypeString_withoutg[BH.cvar.p]=''


particleToTypeString={}

particleToTypeString.update(particleToTypeString_withoutg)

particleToTypeString[BH.cvar.m]='g'
particleToTypeString[BH.cvar.p]='g'

def helicityPM(pID):
    if pID.helicity()==1:
        return 'p'
    elif pID.helicity()==-1:
        return 'm'
    else:  return '0' 
    
    
def noString(*args):
    return ''

def typesString(iterable,withBar=False,separator='',withoutg=False, withHelicity=False,withType=True):
    if withoutg:
        map=particleToTypeString_withoutg
    else:
        map=particleToTypeString

    if withType:
        if withBar:
            typeFn=lambda x: map[p]
        else:
            typeFn=lambda x: map[p][0] if len(map[p])>0 else '' 
    else :
        typeFn=noString
        
    if withHelicity:
        helicityFn=helicityPM
    else:
         helicityFn=noString

    return separator.join([ typeFn(p)+helicityFn(p) for p in iterable ])


def stringToParticles(st):
    ps=st.split(' ')
    return [ stringToParticleMap[p] for p in ps ]


def processTypesString(PRO,**kwargs):
    return typesString(PRO.particle_IDs(),**kwargs)


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def genProcessList(PRO,excludedList=[],requiredList=[],verbose = False):    
    excluded= [ re.compile(ex) for ex in excludedList ]
    required= [ re.compile(ex) for ex in requiredList ]
    for ps in unique_everseen( itertools.permutations(PRO.particle_IDs()), lambda x: typesString(x, True) ):
        ts=typesString(ps, True)
        exclude=False
        for ex in excluded:
            if ex.search(ts+ts):
                exclude=True
                if verbose: print "%s excluded" % ts
                break
        if exclude: continue
        exclude=False
        for req in required:
            if not req.search(ts+ts):
                exclude=True
                if verbose: print "%s excluded" % ts
                break
        if exclude: continue
        # neither excluded nor missing requirement
        if verbose: print "%s accepted" % ts        
        yield ps


def genAllHelicities(PRO):
    for hel in itertools.product([-1,1],repeat=len(PRO)):
        yield  map( lambda p,h: BH.particle_ID(p.type(),h,p.flavor(),p.is_anti_particle()) , PRO, hel ) 
    

def testTrees(PRO,excludedList=[],requiredList=[],verbose=False,tolerance=0.00000000001,processTest=lambda x: True,StopOnFirstError=False):    
    ntests=0
    nzero=0
    nfailed=0
    npass=0
    nnotpresent=0
    ps =rambo.PS(len(PRO))
    cms = [ BH.Cmomd(*p) for p in ps ]
    mc = BH.mcd(*cms)
    ind = BH.vectori(range(1,len(PRO)+1))
    for ps in genProcessList(PRO, excludedList, requiredList):
        if verbose : print typesString(ps, True)
        for phs in genAllHelicities(ps):
            pro=BH.process(BH.vectorpID(phs))
            if not processTest(pro): continue
            ntests+=1
            A=BH.TreeHelAmpl(pro)
            ca = A.eval(mc,ind)
            if abs(ca) != 0.:
                try:
                    ST = BH.SharedTree(pro)
                    cst = ST.eval(mc,ind)
                    acc=abs((cst-ca)/ca)
                    if acc > tolerance:  
                        print '%s NOT OK, Values are st: %s a: %s ' % ( pro,cst,ca )
                        nfailed+=1               
                    else:
                        if verbose: print '%s OK' % pro
                        npass+=1
                except:    
                    print "Failed to generate SharedTree for process %s" % pro
                    nnotpresent+=1
                    if StopOnFirstError: return pro
            else :
                if verbose: print '%s zero' % pro
                nzero+=1
    print """
    tested: %s
    zero: %s
    passed: %s
    failed: %s
    not present: %s
    """ % (ntests,nzero,npass,nfailed,nnotpresent)
    return (ntests,nzero,nfailed,npass,nnotpresent)



def gluonHelicities(PRO):
    helicities = [ p.helicity() for p in PRO.particle_IDs() if p.is_a(BH.cvar.gluon)]    
    return helicities

def quarkHelicities(PRO):
    helicities = [ p.helicity() for p in PRO.particle_IDs() if p.is_a(BH.cvar.quark)]    
    return helicities

def quarkFlavorHelicities(PRO,flavor):
    helicities = [ p.helicity() for p in PRO.particle_IDs() if p.is_a(BH.cvar.quark) and p.flavor()==flavor]    
    return helicities

def leptonHelicities(PRO):
    helicities = [ p.helicity() for p in PRO.particle_IDs() if p.is_a(BH.cvar.lepton)]    
    return helicities



def test_ng(n):
    print 'Testing %s g: ' %n
    p = BH.cvar.p
    PRO = BH.process(*((p,)*n))
    testTrees(PRO)
    print '- - - - - - - - - - - - - - - - - - -     '

def test_2q1yng(n):
    print 'Testing 2q 1y %sg: ' %n
    p = BH.cvar.p
    yp = BH.cvar.yp
    qp = BH.cvar.qp
    qbp = BH.cvar.qbp
    PRO = BH.process(qbp,qp,yp,*((p,)*(n)))
    testTrees(PRO)
    print '- - - - - - - - - - - - - - - - - - -     '

def test_2qng(n):
    print 'Testing 2q %sg: ' %n
    p = BH.cvar.p
    qp = BH.cvar.qp
    qbp = BH.cvar.qbp
    PRO = BH.process(qbp,qp,*((p,)*(n)))
    testTrees(PRO)
    print '- - - - - - - - - - - - - - - - - - -     '



def test_2qng2l(n,**kwargs):
    print 'Testing 2q %sg 2l: ' %n
    p = BH.cvar.p
    yp = BH.cvar.yp
    qp = BH.cvar.qp
    qbp = BH.cvar.qbp
    lp = BH.cvar.lp
    lbp = BH.cvar.lbp
    PRO = BH.process(qbp,qp,lp,lbp,*((p,)*(n)))
    excluded=[
              'l(g*)q(g*)l' 
              ]
    required=[
              'lb?l' 
              ]
    def qh(PRO):
        helq=quarkHelicities(PRO)
        hell=leptonHelicities(PRO)
        return helq.count(-1) == 1 and helq.count(1) == 1 and hell.count(-1) == 1 and hell.count(1) == 1
    
    testTrees(PRO,excludedList=excluded,requiredList=required,processTest=qh,**kwargs)
    print '- - - - - - - - - - - - - - - - - - -     '


def test_2qng2l_lc(n,**kwargs):
    print 'Testing 2q %sg 2l only lc configurations: ' %n
    p = BH.cvar.p
    yp = BH.cvar.yp
    qp = BH.cvar.qp
    qbp = BH.cvar.qbp
    lp = BH.cvar.lp
    lbp = BH.cvar.lbp
    PRO = BH.process(qbp,qp,lp,lbp,*((p,)*(n)))
    excluded=[
              'l(g*)q(g*)l' 
              ]
    required=[
              'lb?l' ,
              'q'+'g'*n+'q'
              ]
    def mhv(PRO):
        hel=gluonHelicities(PRO)
        return hel.count(-1) <= 1 or hel.count(1) <= 1  

    testTrees(PRO,excludedList=excluded,requiredList=required,processTest=mhv,**kwargs)
    print '- - - - - - - - - - - - - - - - - - -     '


def test_2qng2Q(n,**kwargs):
    print 'Testing 2q %sg 2Q: ' %n
    p = BH.cvar.p
    yp = BH.cvar.yp
    qp = BH.cvar.qp
    qbp = BH.cvar.qbp
    q2p = BH.cvar.q2p
    qb2p = BH.cvar.qb2p
    PRO = BH.process(qbp,qp,q2p,qb2p,*((p,)*(n)))
    excluded=[
              'qb?(g*)Qb?(g*)qb?(g*)Qb?' 
              ]
    required=[
#              'gQQbqqb' 
              ]
    def qh(PRO):
        helq1=quarkFlavorHelicities(PRO,1)
        helq2=quarkFlavorHelicities(PRO,2)
        return helq1.count(-1) == 1 and helq1.count(1) == 1 and helq2.count(-1) == 1 and helq2.count(1) == 1
    
    res=testTrees(PRO,excludedList=excluded,requiredList=required,processTest=qh,**kwargs)
    if kwargs.get('StopOnFirstError',False): return res
    print '- - - - - - - - - - - - - - - - - - -     '




def test_all():
    test_ng(4)
    test_ng(5)
    test_ng(6)
    test_ng(7)
    test_ng(8)    
    test_2q1yng(1)
    test_2q1yng(2)
    test_2qng2l(1)
    test_2qng2l(2)
    test_2qng2l(3)
    

p=BH.cvar.p
m=BH.cvar.m
qp=BH.cvar.qp
qm=BH.cvar.qm
qbm=BH.cvar.qbm
qbp=BH.cvar.qbp
q2p=BH.cvar.q2p
q2m=BH.cvar.q2m
qb2m=BH.cvar.qb2m
qb2p=BH.cvar.qb2p

#PRO=BH.process(m,m,qbp,qm,q2m,m,qb2p)
PRO=BH.process(qbp,qm,q2m,m,m,qb2p,m)
PRO2=BH.process(m,m,q2m,qm,qbp,m,qb2p)

PROfailed=BH.process(qbp,qm,q2m,qb2p,p,m,m)

#PRO2=BH.process(qbm,qp,q2m,m,m,qb2p)
#PRO2=BH.process(p,qp,qbm,q2p,qb2m)
#PRO3=BH.process(p,q2p,qb2m,qp,qbm)
#PRO4=BH.process(p,qbm,qp,qb2m,q2p)
A1=BH.TreeHelAmpl(PRO)
A2=BH.TreeHelAmpl(PRO2)
#A3=BH.TreeHelAmpl(PRO3)
#A4=BH.TreeHelAmpl(PRO4)

ps =rambo.PS(len(PRO))
cms = [ BH.Cmomd(*p) for p in ps ]
mc = BH.mcd(*cms)
ind = BH.vectori(range(1,len(PRO)+1))
ind2 = BH.vectori([2,1,7,6,5,4,3])

c1=A1.eval(mc,ind)
c2=A2.eval(mc,ind2)
#c3=A3.eval(mc,ind)
#c4=A4.eval(mc,ind2)

print c1,c2


