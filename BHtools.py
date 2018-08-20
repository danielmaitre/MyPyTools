import sys
sys.path.append('/home/daniel/workspace/BHlib/build/lib/')
sys.path.append('/home/daniel/workspace/BHlib/my_programs')
import BH
import re
import itertools

import rambo 

def getRandomBHinput(n,Type=float,**kargs):
    psAllIncoming =rambo.PS(n,Type,**kargs)
    ps=[
        [-x for x in psAllIncoming[0]],
        [-x for x in psAllIncoming[1]]
         ] +psAllIncoming[2:]
    return BH.BHinput(BH.vectorm(ps),n)

def getRandomMC(n):
	ps =rambo.PS(n)
	cms = [ BH.Cmomd(*p) for p in ps ]
	return BH.mcd(*cms)

def mcFromRGMP(mcOrig,mcR):
    for i in range(mcOrig.n()):
        l=mcOrig.L(i+1)
        lt=mcOrig.Lt(i+1)
        L=BH.LambdaR(BH.to_double(l.a1),BH.to_double(l.a2))
        Lt=BH.LambdatR(BH.to_double(lt.a1),BH.to_double(lt.a2))
        mcR.insert(Lt,L)

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
    'lbm' : BH.cvar.lbm,
	'Um' : BH.cvar.Qm ,
	'Up' : BH.cvar.Qp ,
	'Ubm' : BH.cvar.Qbm ,
	'Ubp' : BH.cvar.Qbp ,
'ph': BH.cvar.ph ,
'phd': BH.cvar.phd ,
    'H': BH.cvar.H ,

        'qMm' : BH.cvar.Qm ,
    'qMp' : BH.cvar.Qp ,
        'qMbm' : BH.cvar.Qbm ,
    'qMbp' : BH.cvar.Qbp ,

    


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
    BH.cvar.lbm : 'lb',
	BH.cvar.Qm : 'U',
	BH.cvar.Qp : 'U',
	BH.cvar.Qbm : 'Ub',
	BH.cvar.Qbp : 'Ub',
 BH.cvar.ph:'ph' ,
 BH.cvar.phd:'phd' ,
 BH.cvar.H :'H'
    
    
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

particleTypeMap={
'g':BH.cvar.gluon,
'q':BH.cvar.quark,
'Q':BH.cvar.quark_massive,
'l':BH.cvar.lepton,
'y':BH.cvar.photon,
'G':BH.cvar.gluino,
's':BH.cvar.scalar,
'h':BH.cvar.higgs,
# for some reason not in cvar...
#'Rsc':BH.cvar.gluon_massive_scalar,
'R':BH.cvar.gluon_massive,
'L':BH.cvar.gluino_massive,
'S':BH.cvar.scalar_massive
}

particlePattern=re.compile('(?P<type>\w*?)(?P<antip>b)?(?P<flavour>\d*)(?P<sign>[+-])(?P<mass>\[.*?\])?')

def stringToSingleParticle(st):
    easy=stringToParticleMap.get(st,None)
    if easy: return easy
    match = particlePattern.match(st)
    if match:
        if match.group('sign')=='+':
            sign=1
        else:
            sign=-1
        isAnti=False
        if match.group('antip'):
            isAnti=True
        flavour=1
        if match.group('flavour'):
            flavour=int(match.group('flavour'))

        t=particleTypeMap[match.group('type')]
        return BH.particle_ID(t,sign,flavour,isAnti)

    #not so easy...
    
    

def stringToParticles(st):
    ps=st.split(' ')
    return [ stringToParticleMap[p] for p in ps ]

def stringToProcess(st):
    return BH.process(BH.vectorpID(stringToParticles(st)))


def processTypesString(PRO,**kwargs):
    return typesString(PRO.particle_IDs(),**kwargs)


# PROCESS GENERATION


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
    






def checkForDuplicates(cpd):
    nboxes=cpd.nbr_boxes()
    for i in range(1,nboxes):
        for j in range(i+1,nboxes):
            if BH.unordered_equal_fn(cpd.box(i),cpd.box(j)): print 'boxes %d and %d are equivalent!' % (i,j)
    print '%d boxes checked' % nboxes
    ntris=cpd.nbr_triangles()
    for i in range(1,ntris):
        for j in range(i+1,ntris):
            if BH.unordered_equal_fn(cpd.triangle(i),cpd.triangle(j)): print 'triangles %d and %d are equivalent!' % (i,j)
    print '%d trianges checked' % ntris
    nbubs=cpd.nbr_bubbles()
    for i in range(1,nbubs):
        for j in range(i+1,nbubs):
            if BH.unordered_equal_fn(cpd.bubble(i),cpd.bubble(j)): print 'bubbles %d and %d are equivalent!' % (i,j)
    print '%d bubbles checked' % nbubs



def checkOrder(cpd):
    nboxes=cpd.nbr_boxes()
    for i in range(1,nboxes):
        if BH.unordered_compare_fn(cpd.box(i+1),cpd.box(i)):
            print 'Boxes %d and %d are not correctly ordered' % (i,i+1)
    print '%d boxes checked' % nboxes
    ntris=cpd.nbr_triangles()
    for i in range(1,ntris):
        if BH.unordered_compare_fn(cpd.triangle(i+1),cpd.triangle(i)):
            print 'Triangles %d and %d are not correctly ordered' % (i,i+1)
    print '%d trianges checked' % ntris
    nbubs=cpd.nbr_bubbles()
    for i in range(1,nbubs):
        if BH.unordered_compare_fn(cpd.bubble(i+1),cpd.bubble(i)):
            print 'Bubbles %d and %d are not correctly ordered' % (i,i+1)
    print '%d bubbles checked' % nbubs



def PrintCutCoefficients(cpd):
    for i in range(1,cpd.nbr_boxes()+1):
        bc=cpd.box(i).eval(mc5,ind5)
        print '%d: %s' % (i, bc)

    print 'triangles:'
    for i in range(1,cpd.nbr_triangles()+1):
        bc=cpd.triangle(i).eval(mc5,ind5)
        print '%d: %s' % (i, bc)

    print 'bubbles:'
    for i in range(1,cpd.nbr_bubbles()+1):
        bc=cpd.bubble(i).eval(mc5,ind5)
        print '%d: %s' % (i, bc)



