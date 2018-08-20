#!/usr/bin/env python

import convertHelper

treesDir='/home/daniel/workspace/BHlib/src/trees_eval/'

def convert_A0_2q2l():
    inputFile = open("../../src/trees_eval/A0_2q2l_eval.cpp","r")
    outputFile = open("SA_2q2l.hpp","w")

    convertHelper.processFile(
        'A2q2l',
        4,
        outputFile,inputFile,

        processList=[   #don't use all permutations for space
                'qqll'
        ],
        rotationList= {
        #      'llqqgg':4,   # SSLC 
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
        }
        )


def convert_A0_2q3g2l():
    inputFile = open("../../src/trees_eval/A0_2q3g2l_eval.cpp.old","r")
    outputFile = open("SA_2q3g2l_new_compare.hpp","w")

    convertHelper.processFile(
        'A2q3g2l',
        7,
        outputFile,inputFile,

        processList=[   #don't use all permutations for space
                'qgggqll',
                'qggqgll',
                'qgqggll',
                'qqgggll'
        ],
        rotationList= {
        #      'llqqgg':4,   # SSLC 
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
             'qgggqll': [ 
                          [0,1,2,3,4,5,6],
                          [0,1,2,3,4,6,5],
                          [4,3,2,1,0,5,6],
                          [4,3,2,1,0,6,5]
                          ],
            'qggqgll': [ 
                          [0,1,2,3,4,5,6],
                          [0,1,2,3,4,6,5],
                          [3,2,1,0,4,5,6],
                          [3,2,1,0,4,6,5]
                          ],
            'qgqggll': [ 
                          [0,1,2,3,4,5,6],
                          [0,1,2,3,4,6,5],
                          [2,1,0,4,3,5,6],
                          [2,1,0,4,3,6,5]
             ],
            'qqgggll': [ 
                          [0,1,2,3,4,5,6],
                          [0,1,2,3,4,6,5],
                          [1,0,4,3,2,5,6],
                          [1,0,4,3,2,6,5]
             ]
        }
        )


def convert_A0_2q2Q():
    inputFile = open("../../src/trees_eval/A0_2q2Q_eval.cpp","r")
    outputFile = open("SA_2q2Q.hpp","w")

    convertHelper.processFile(
        'A2q2Q',
        4,
        outputFile,inputFile,

        processList=[   #don't use all permutations for space
                'qqQQ'
        ],
        rotationList= {
        #      'llqqgg':4,   # SSLC 
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
#             'qqQQ': [ 
#                          [0,1,2,3,4]
#                          ],
#            'qgqQQ': [ 
#                          [0,1,2,3,4]
#                          ]
        }
        )

def convert_A0_2q1g2Q():
    inputFile = open("../../src/trees_eval/A0_2q1g2Q_eval.cpp","r")
    outputFile = open("SA_2q1g2Q.hpp","w")

    convertHelper.processFile(
        'A2q1g2Q',
        5,
        outputFile,inputFile,

        processList=[   #don't use all permutations for space
                'gqqQQ',
                'qgqQQ'
        ],
        rotationList= {
        #      'llqqgg':4,   # SSLC 
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
             'gqqQQ': [ 
                          [0,1,2,3,4]
                          ],
            'qgqQQ': [ 
                          [0,1,2,3,4]
                          ]
        }
        )

def convert_A0_2q2g2Q():
    inputFile = open("../../src/trees_eval/A0_2q2g2Q_eval.cpp","r")
    outputFile = open("SA_2q2g2Q.hpp","w")

    convertHelper.processFile(
        'A2q2g2Q',
        6,
        outputFile,inputFile,

        processList=[  
                'ggqqQQ',
                'gqgqQQ',
                'qgqgQQ',
                'qgqQgQ',
                'qggqQQ',
                'gqqgQQ'
        ],
        rotationList= {
        #      'llqqgg':4,   # SSLC 
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
        }
        )

def convert_A0_2q3g2Q():
    print "A0_2q3g2Q file is incomplete!!!"
    inputFile = open(treesDir+"/A0_2q3g2Q_eval.cpp","r")
    outputFile = open("SA_2q3g2Q.hpp","w")

    convertHelper.processFile(
        'A2q3g2Q',
        7,
        outputFile,inputFile,

        processList=[  
#                'gggqqQQ',
#                'qgggQQq',  # needs to ge rotated to gggQQgg

                'ggqgqQQ',
                'ggqqgQQ',
                'ggqqQgQ',
                'ggQgQqq',  # this one is needed to get the xxpm

                'gqggqQQ',
                'gqgqgQQ',
                'gqgqQgQ',

                'qgggqQQ',
                'qggqgQQ',
                'QggQgqq',
                'qggqQgQ'
                

        ],
        rotationList= {
              'qgggQQq':6
            },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
        },
        finalReplacements=[
            (r'gggQQqq',r'gggqqQQ'),
            (r'ggQgQqq',r'ggqgqQQ')
            ]
        )



def convert_A0_2q2g1y():
    inputFile = open("../../src/trees_eval/A0_2q2g1y_eval.cpp","r")
    outputFile = open("SA_2q2g1y_new.hpp","w")

    convertHelper.processFile(
        'A2q2g1y',
        5,
        outputFile,inputFile,

        processList=[   #don't use all permutations for space
#                'qggyq',
#                'qggqy',
#                'qgqgy'
                'qggyq'
        ],
        rotationList= {
              'qyggq':4
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
             'qggyq': [ 
                          [0,1,2,3,4]
                          ],
            'qgqgy': [ 
                          [0,1,2,3,4]
                          ]
        }
        )



def convert_A0_2q2Q1y():
    inputFile = open("../../src/trees_eval/A0_2q2Q1y_eval.cpp","r")
    outputFile = open("SA_2q2Q1y.hpp","w")

    convertHelper.processFile(
        'A2q2Q1y',
        5,
        outputFile,inputFile,

        processList=[ 
                'qqQQy'
        ],
        rotationList= {
#              'qyggq':4
        #      'qllqgg':3 ,  # LC 
        #       'qgllqg':2    # SLC
        },

        permutationList= {
        #      'llqgggq':[2,3,4,5,6,1,0],   # LC
        },

        permutationSignList= [
        ],

        equivalentlist = {
        }
        )


import re
import string
import BH
import rambo

nameMap = {'ga':'y' , 'q':'q' , 'e':'l','Q':'Q'}

from SharedTreesTest import genProcessList,genAllHelicities,quarkFlavorHelicities,processTypesString,typesString,stringToParticles

def getAvailable(inputFile,processSize):
    f=open(inputFile)
    text=f.read()
    particlePattern= '(?P<part>((?P<type>(q|Q|ga|e))?(?P<helicity>m|p)))'
    p2 = re.compile( particlePattern )

    numberPattern = r'(?P<number>\d*)' + r':(?P<process>(\s*'+ particlePattern +'){'+str(processSize)+'})'
    np = re.compile( numberPattern )
    iterator = np.finditer(text)
    return [ string.strip(x.group('process')) for x in iterator]


def getNonZeroTree(PRO,excludedList=[],requiredList=[],verbose=False,processTest=lambda x: True):    
    ps =rambo.PS(len(PRO))
    cms = [ BH.Cmomd(*p) for p in ps ]
    mc = BH.mcd(*cms)
    ind = BH.vectori(range(1,len(PRO)+1))
    for ps in genProcessList(PRO, excludedList, requiredList):
        if verbose : print typesString(ps, True)
        for phs in genAllHelicities(ps):
            pro=BH.process(BH.vectorpID(phs))
            if not processTest(pro): continue
            A=BH.TreeHelAmpl(pro)
            ca = A.eval(mc,ind)
            if abs(ca) != 0.:
                yield pro


def show_2qng2Q(n,**kwargs):
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
    it = getNonZeroTree(PRO, excludedList=excluded, requiredList=required, processTest=qh)
    print len(list(it))
#    for i in it:
#            print i

available=getAvailable('/home/daniel/workspace/BHlib/src/trees_eval/A0_2q3g2Q_eval.cpp',7)

sourceFilePath='/home/daniel/workspace/BHlib/src/trees_eval/A0_2q3g2Q_eval.cpp'
sourceFile=open(sourceFilePath,'r').read()

#convert_A0_2q2Q()
#convert_A0_2q1g2Q()
#convert_A0_2q2g2Q()
#convert_A0_2q3g2Q()
#convert_A0_2q2g1y()
p = BH.cvar.p
m = BH.cvar.m
yp = BH.cvar.yp
qp = BH.cvar.qp
qm = BH.cvar.qm
qbp = BH.cvar.qbp
qbm = BH.cvar.qbm
q2p = BH.cvar.q2p
qb2p = BH.cvar.qb2p
q2m = BH.cvar.q2m
qb2m = BH.cvar.qb2m
PRO = BH.process(qbp,qp,q2p,qb2p,*((p,)*(3)))
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
NZT = getNonZeroTree(PRO, excludedList=excluded, requiredList=required, processTest=qh)

protest=BH.process(qbm,q2m,qb2p,m,qp,m,m)
protest2=BH.process(qb2m,qm,qbp,m,q2p,m,m)

needed=[]
preferredOrder= [
                 'gggqqQQ',
                 'ggqgqQQ',
                 'ggqqgQQ',
                 'ggQgqqQ'    # needed for some helicities
                 ]


def isThere(pro):
    ts=processTypesString(pro,withHelicity=True,withoutg=True,separator=' ')
    if ts in needed: return (True,ts)
    tss=ts.split(' ')
    permutations= [ tss[n:]+tss[:n] for n in range(1,len(tss)) ]
    for perm in permutations:
        fnString=' '.join(perm)
        if fnString in needed:
            return (True,fnString)
    return (False,'')

def FindNormalSolution(pro,notPreferredOK=False,verbose=False,**kwargs):
    ts = processTypesString(pro,withHelicity=False,withoutg=False,separator=' ')
    tsfull=processTypesString(pro,withHelicity=True,withoutg=True,separator=' ')
    tss=ts.split(' ')
    tssfull=tsfull.split(' ')
    permutations= [ tss[n:]+tss[:n] for n in range(len(tss)) ]
    for perm in permutations:
        if verbose: print 'testing: %s %s' % (''.join(perm),''.join(perm) in preferredOrder)
        isPreferred = (''.join(perm) in preferredOrder)
        if verbose: print 'isPreferred: %s' % isPreferred
        if  isPreferred or notPreferredOK :
            ind = permutations.index(perm)
            ts_permuted=tssfull[ind:]+tssfull[:ind]
            fnString=' '.join(ts_permuted)
            if fnString in available:
                if isPreferred :
                    print 'found permutation with preferred order for ',ts,' index ',ind,' (mapped to %s)'%ts_permuted
                else:
                    print 'found permutation without preferred order for ',ts,' index ',ind,' (mapped to %s)'%ts_permuted
                needed.append(' '.join(ts_permuted))
                return (True,'normal',fnString)
            else:
                if verbose : print '%s not available' %fnString
    return (False,'normal','')

N=7

ps =rambo.PS(7)
cms = [ BH.Cmomd(*p) for p in ps ]
mc = BH.mcd(*cms)
ind = BH.vectori(range(1,N+1))
indRev = BH.vectori(range(N,0,-1))

def FindReverseSolution(pro,notPreferredOK=False,**kwargs):
    ps=list(pro.particle_IDs())
    ps.reverse()
    inversePro=BH.process(BH.vectorpID(ps))
    print pro
    print inversePro
    found,fnString = isThere(inversePro)
    if found:
        A1=BH.TreeHelAmpl(pro)
        A2=BH.TreeHelAmpl(inversePro)
        a1 = A1.eval(mc,ind)
        a2 = A2.eval(mc,indRev)
        #print a1
        #print a2
        return (True,'reverse',fnString,a1/a2)
    else: 
        found,normalString,fnString = FindNormalSolution(inversePro, notPreferredOK,**kwargs)
        if found:
            A1=BH.TreeHelAmpl(pro)
            A2=BH.TreeHelAmpl(inversePro)
            a1 = A1.eval(mc,ind)
            a2 = A2.eval(mc,indRev)            
            return (True,'reverse',fnString,a1/a2)
    return (False,'')
    
def flipParticleHelicity(p):
    return BH.particle_ID(p.type(),-p.helicity(),p.flavor(),p.is_anti_particle())
    
def flipHelicities(pro):
    ps = [ flipParticleHelicity(p) for p in pro.particle_IDs() ]
    return BH.process(BH.vectorpID(ps))

def swapParticleFlavour(p,particle,f1,f2):
    if p.is_a(particle):
        if p.flavor()==f1:
            return BH.particle_ID(particle,p.helicity(),f2,p.is_anti_particle())
        if p.flavor()==f2:
            return BH.particle_ID(particle,p.helicity(),f1,p.is_anti_particle())
    else: return p

def swapFlavour(pro,particle,f1,f2):
    ps = [ swapParticleFlavour(p, particle, f1, f2) for p in pro.particle_IDs() ]
    return BH.process(BH.vectorpID(ps))

def reverseProcess(pro):
    ps=list(pro.particle_IDs())
    ps.reverse()
    return BH.process(BH.vectorpID(ps))
        
def tryNormalReverse(pro):
    res = FindNormalSolution(pro,notPreferredOK=False)
    if res[0]:
        print 'Solution found (normal, with preferred order)'
        return res 
    res = FindReverseSolution(pro,notPreferredOK=False)
    if res[0]:
        print 'Solution found (reverse, with preferred order)'
        return res 
    
    res= FindNormalSolution(pro,notPreferredOK=True)
    if res[0]:
        print 'Solution found (normal, without preferred order)'
        return res 
    res= FindReverseSolution(pro,notPreferredOK=True)
    if res[0]:
        print 'Solution found (reverse, without preferred order)'
        return res 
    return (False,'')
            
def FindSolution(pro):
    res = isThere(pro)
    if res[0] : 
        print 'Solution already there'
        return (True,'there')

    inversePro=reverseProcess(pro)
    res=isThere(pro)
    if res[0] : 
        print 'Solution there with reversal'
        return (True,'reversal')
    
    swappedPro=swapFlavour(pro, BH.cvar.quark, 1, 2);
    res = isThere(pro)
    if res[0] : 
        print 'Solution there with quark swap'
        return (True,'QuarkSwap')
    
    res = tryNormalReverse(pro)
    if res[0]: return res

    res = tryNormalReverse(swappedPro)
    if res[0]: return res
        
    hflipPro=flipHelicities(pro);
    res=tryNormalReverse(hflipPro)
    if res[0]: return res
    
    return (False,'')

# this is needed because the shared tree code will always build the
# type string such that q is first

wrongQorder=re.compile(r'A_[^q]*Q.*_eval')
wrongQorderProcess=re.compile(r'[^q]*Q.*?(q|Q).*?(q|Q).*?(q|Q).*?')

def orderQs(txt):
    match=wrongQorder.search(txt)
    if match:
        st = match.group()
        newst=st.replace('Q','X').replace('q','x').replace('x','Q').replace('X','q')

        newtxt=txt.replace(st,newst)
        #print 'old %s    new: %s' % (txt,newtxt)
        return newtxt   
    else:
        match=wrongQorderProcess.search(txt)
        if match:
            st = match.group()
            #print st
            newst=st.replace('Q','X').replace('q','x').replace('x','Q').replace('X','q')

            newtxt=txt.replace(st,newst)
            return newtxt   
        else:
            return txt

import shelve

db=shelve.open('2q3g2Q_db')
    
def findNextProblem(imax=-1):
    pp=next(NZT)
    ii=0
    if imax>0:
        fullRange=False
    else:
        fullRange=True
    output=''
    res=FindSolution(pp)
    try:
        while res[0]  and (fullRange or ii<imax) :
            pp=next(NZT)
            ii+=1
            print '---- ',pp
            res=FindSolution(pp)
            db[str(pp)]= res
            newFn=generateFile(res)
            if newFn != '':
                output+=orderQs(newFn)
                output+='\n'
    except StopIteration:
        fout=open('test2.hpp','w')
        fout.write(output)
        return pp
    else:
        fout=open('test2.hpp','w')
        fout.write(output)
    
    
def findAvailable(pro):
    st=processTypesString(pro,separator=' ',withHelicity=True,withoutg=True)
    stst=st+' '+st
    all=[]
    for s in available:
        if s in stst:
            all.append(s)
    return all


generated=[]
inverseWithMinus=[]
inverseWithPlus=[]

def generateFile(res):
    if res[1] == 'there':
        #nothing needs to be done          
        return ''
    if res[1] == 'normal':
        if not orderQs(res[2]) in generated:
            generated.append(orderQs(res[2]))
            return getFunction(sourceFile,res[2])
        else :
            return ''
    if res[1] == 'reverse':
        if not orderQs(res[2]) in generated:
            generated.append(orderQs(res[2]))
            pids=stringToParticles(res[2])
            typeString=typesString(pids,separator='',withHelicity=False,withoutg=False)
            if abs(res[3]+1)< 0.0000000001:
                if typeString not in inverseWithMinus:
                    inverseWithMinus.append(typeString)
            else :
                if abs(res[3]-1)< 0.0000000001:
                    if typeString not in inverseWithPlus :
                        inverseWithPlus.append(typeString)
                else :
                    print 'Unexpected ratio %s' % res[3]
                    raise SystemError

            return getFunction(sourceFile,res[2])        
        else :
            return ''
        
    print 'no treatment for: ',res
    raise SystemError
        
        
output=''


def getFunction(sourceFile,pro):
    print 'getting function ',pro
    pattern = r'\b' + '(?P<number>\d+)' + r':\s*(?P<process>'+ pro +')'
    nbrCode=re.compile(pattern)
    match = nbrCode.search(sourceFile)
    if match:
        number = match.group('number')
        print 'found process number %s' % number
        pids=stringToParticles(pro)
        typeString=typesString(pids,separator='',withHelicity=False,withoutg=False)
        helicityString=typesString(pids,separator='',withHelicity=True,withoutg=False,withType=False)
        treePattern = r'template <class T> complex<T> \s*' + r'A2q3g2Q'  + str(number) + r'(?P<function>(?P<beforeReturn>_eval(.*?))return(?P<afterReturn>.*?);\s*\})'
        #print treePattern
        ptree=re.compile(treePattern,re.DOTALL)
        mtree = ptree.search( sourceFile )
        if mtree:
            function=convertHelper.expandSpab(mtree.group('function'))
            #print 'Match found: ', function
            fnName=typeString + '_' + helicityString
            print 'fnName : %s' % fnName
            newFunction= 'complex<T> A_' + fnName + function +'\n\n'
            #print 'New function generated for: ', fnName
            return newFunction
    else:
        print 'Could not find a function for %s ' % pro
        raise SystemError

rotations=[
    '6543210',
    '5432106',
    '4321065',
    '3210654',
    '2106543',
    '1065432',
    '0654321',
    ]

def dbInfo(db):
    pss=set()
    minus=set()
    plus=set()
    for key in db:
        value=db[key]
        if len(value)>2:
            #this is the process needed:
            pro=BH.process(BH.vectorpID(stringToParticles(value[2])))
            pS=processTypesString(pro)
            #pss.add(orderQs(pS))
            pss.add(pS)
            keyWithoutB=key.replace('b','')
            rotation='not found'
            for i in range(len(pro)):
                inv=list(pro.particle_IDs())[::-1]
                rotated=BH.process(BH.vectorpID(inv[i:]+inv[:i]))
                if str(rotated) == keyWithoutB:
                    rotation=rotations[i]
            if value[1]=='reverse':
                inv=list(pro.particle_IDs())[::-1]
                if abs(value[3] -1) < 0.000000001:
                    plus.add( (orderQs(pS),rotation)  )                    
                if abs(value[3] +1) < 0.000000001:
                    minus.add( (orderQs(pS),rotation) )                    

    print "provided: %s" % pss,plus,minus
    return pss,plus,minus

            
