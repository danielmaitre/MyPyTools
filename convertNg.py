#!/usr/bin/env python


"""
file = open("../../src/trees_eval/A0_5g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_5g.hpp","w")
#outputFile = open("test.out","w")
processSize=5
processList=[   #don't use all permutations for space
            'ggggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A5g'

nbrFunctions=32  # 2^n
DoRemovePermutations=False

"""

"""
file = open("../../src/trees_eval/A0_6g_eval.cpp","r")
outputFile = open("SA_6g.hpp","w")
processSize=6
processList=[   #don't use all permutations for space
            'gggggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A6g'

nbrFunctions=64  # 2^n

DoRemovePermutations=True

"""

"""

file = open("../../src/trees_eval/A0_4g_eval.cpp","r")
outputFile = open("SA_4g.hpp","w")
processSize=4
processList=[   #don't use all permutations for space
            'gggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A4g'

nbrFunctions=16  # 2^n

DoRemovePermutations=False

"""


file = open("../../src/trees_eval/A0_3g_eval.cpp","r")
outputFile = open("SA_3g.hpp","w")
processSize=3
processList=[   #don't use all permutations for space
            'ggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A3g'

nbrFunctions=8  # 2^n

DoRemovePermutations=False


import re

def rotateRight(l,offset):
    return l[-offset:] + l[:-offset] 
def rotateLeft(l,offset):
    return l[offset:] + l[:offset] 
    
spabPattern = '((?P<fn>ep.spab)\(\s*(?P<i>\d)\s*,\s*ep.Sum\(\s*(?P<j>\d)\s*,\s*(?P<k>\d)\s*\)\s*,\s*(?P<l>\d)\s*\))'
spabP = re.compile(spabPattern)
def spabExpand(match):
    i=match.group('i')
    j=match.group('j')
    k=match.group('k')
    l=match.group('l')
    newtext= '(ep.spa('+i+','+j+')*ep.spb('+j+','+l+')'
    newtext+=' +ep.spa('+i+','+k+')*ep.spb('+k+','+l+'))'
    return newtext

spab3Pattern = '((?P<fn>ep.spab)\(\s*(?P<i>\d)\s*,\s*ep.Sum\(\s*(?P<j1>\d)\s*,\s*(?P<j2>\d)\s*,\s*(?P<j3>\d)\s*\)\s*,\s*(?P<l>\d)\s*\))'
spab3P = re.compile(spab3Pattern,re.DOTALL)

def spab3Expand(match):
    i=match.group('i')
    j1=match.group('j1')
    j2=match.group('j2')
    j3=match.group('j3')
    l=match.group('l')
    newtext= '('
    newtext+= '  ep.spa('+i+','+j1+')*ep.spb('+j1+','+l+')'
    newtext+=' +ep.spa('+i+','+j2+')*ep.spb('+j2+','+l+')'
    newtext+=' +ep.spa('+i+','+j3+')*ep.spb('+j3+','+l+')'
    newtext+=')'
    return newtext


indPattern=r'ind.at\(\s*(?P<index>\d)\s*\)'

def expandSpab(text):
    text1=re.sub(indPattern,'\g<index>',text)
    text2=re.sub(spabP,spabExpand,text1)
    return re.sub(spab3P,spab3Expand,text2)

spinorFunctionPattern = '((?P<fn>spb|spa|s|Sum)\(\s*(?P<i>\d)\s*,\s*(?P<j>\d)\s*\))'
spinorFunctionRegex = re.compile( spinorFunctionPattern )
spinorFunction3Pattern = '((?P<fn>s)\(\s*(?P<i>\d)\s*,\s*(?P<j>\d)\s*,\s*(?P<k>\d)\s*\))'
spinorFunction3Regex = re.compile( spinorFunction3Pattern )
spinorFunction4Pattern = '((?P<fn>s)\(\s*(?P<i>\d)\s*,\s*(?P<j>\d)\s*,\s*(?P<k>\d)\s*,\s*(?P<l>\d)\s*\))'
spinorFunction4Regex = re.compile( spinorFunction4Pattern )


def makeRotator(rotated): return lambda matchobj: matchobj.group('fn') +'(' +str(rotated[int(matchobj.group('i'))])+','+str(rotated[int(matchobj.group('j'))])+')'
def makeRotator3(rotated): return lambda matchobj: matchobj.group('fn') +'(' +str(rotated[int(matchobj.group('i'))])+','+str(rotated[int(matchobj.group('j'))])+','+str(rotated[int(matchobj.group('k'))])+')'
def makeRotator4(rotated): return lambda matchobj: matchobj.group('fn') +'(' +str(rotated[int(matchobj.group('i'))])+','+str(rotated[int(matchobj.group('j'))])+','+str(rotated[int(matchobj.group('k'))])+','+str(rotated[int(matchobj.group('l'))])+')'

def rotateFunction(text,offset):  # rotates argument to the right : spa(1,2) -> spa(2,3) which correspond to a shift of tyoes to the right: qggyq  -> qqggy -> yqqgg -> gyqqg -> ggyqq -> qggyq
    #print p
    rotated = rotateLeft( range(0,processSize),offset)
    newText1=spinorFunctionRegex.sub(makeRotator(rotated),text)
    newText2=spinorFunction3Regex.sub(makeRotator3(rotated),newText1)
    newText3=spinorFunction4Regex.sub(makeRotator4(rotated),newText2)
    return newText3

def permute(text,perm):
    l=list(text)
    n = len( text )
    for i in range(0,n):
        l[i]=text[perm[i]]
        newtext="".join(l)
    return newtext

def permuteList(list,perm):
    n = len( list )
    l=list[:]
    for i in range(0,n):
        l[i]=list[perm[i]]
    return l

def permuteListInverse(ll,perm):
    n = len( ll )
    l=ll[:]
    for i in range(0,n):
        l[perm[i]]=ll[i]
    return l


def makePermutator(perm): 
    permuted=permuteListInverse(range(0,len(perm)),perm) 
    return lambda matchobj: matchobj.group('fn') +'(' +str(permuted[int(matchobj.group('i'))])+','+str(permuted[int(matchobj.group('j'))])+')'
def makePermutator3(perm): 
    permuted=permuteListInverse(range(0,len(perm)),perm) 
    return lambda matchobj: matchobj.group('fn') +'(' +str(permuted[int(matchobj.group('i'))])+','+str(permuted[int(matchobj.group('j'))])+','+str(permuted[int(matchobj.group('k'))])+')'
def makePermutator4(perm): 
    permuted=permuteListInverse(range(0,len(perm)),perm) 
    return lambda matchobj: matchobj.group('fn') +'(' +str(permuted[int(matchobj.group('i'))])+','+str(permuted[int(matchobj.group('j'))])+','+str(permuted[int(matchobj.group('k'))])+','+str(permuted[int(matchobj.group('l'))])+')'


def permuteFunction(text,perm):  # rotates argument to the right : spa(1,2) -> spa(2,3) which correspond to a shift of tyoes to the right: qggyq  -> qqggy -> yqqgg -> gyqqg -> ggyqq -> qggyq
    #print p
    newText1=spinorFunctionRegex.sub(makePermutator(perm),text)
    newText2=spinorFunction3Regex.sub(makePermutator3(perm),newText1)
    newText=spinorFunction4Regex.sub(makePermutator4(perm),newText2)
    return newText
      
output=""
text = file.read()






numberOfOldFunctions=0
numberOfNewFunctions=0
nameMap = {'ga':'y' , 'q':'q' , 'e':'l'}

particlePattern= '(?P<part>((?P<type>(q|q|ga|e))?(?P<helicity>m|p)))'
p2= re.compile( particlePattern )

numberPattern = r'(?P<number>\d*)' + r':(?P<process>(\s*'+ particlePattern +'){'+str(processSize)+'})'
np = re.compile( numberPattern )
iterator = np.finditer(text)

helicities=list()

for i in range(1,nbrFunctions):
    ii=i;
    l=list()
    print i 
    for j in range(0,processSize):
        if ii%2 == 0:
            l.append('m')
        else:
            l.append('p')       
        ii=ii/2
    print l
    needed=True
    if DoRemovePermutations:
        for k in range(1,processSize):
            rot=rotateRight(l,k)
            if rot in helicities:
                print 'no need to compute ' , l , ' because I have ' , rot
                needed=False
    if needed==False :
        continue
    helicities.append(l)
    number=i
    numberOfOldFunctions+=1
    typeString = processList[0]
    helicityString = ''.join(l)
    print typeString
    print helicityString
    if (typeString in processList) or (typeString in rotationList) or (typeString in permutationList):
        treePattern = r'template <class T> complex<T> ' + process + str(number) + r'(?P<function>(?P<beforeReturn>_eval(.*?))return(?P<afterReturn>.*?);\s*\})'
        ptree=re.compile(treePattern,re.DOTALL)
        mtree = ptree.search( text )
        if mtree:
            function=expandSpab(mtree.group('function'))
            #print 'Match found: ', function
            if (typeString in processList):    
                newFunction= 'complex<T> A_' + typeString + '_' + helicityString + function +'\n\n'
                print 'New function generated for: ', typeString + '_' + helicityString
                output+=newFunction
                numberOfNewFunctions+=1


            if typeString in rotationList:
                offset = rotationList[typeString]
                newTypeString = rotateRight(typeString,offset)
                newHelicityString = rotateRight(helicityString,offset)
                print 'Need to do some rotation for ',typeString, ' to ', newTypeString
                newFunction= 'complex<T> A_' + newTypeString + '_' + newHelicityString + rotateFunction(function,offset) +'\n\n'
                print 'New function generated for: ', newTypeString + '_' + newHelicityString
                output+=newFunction
                numberOfNewFunctions+=1
                
            if typeString in permutationList:
                perm = permutationList[typeString]
                newTypeString = permute(typeString,perm)
                newHelicityString = permute(helicityString,perm)
                print 'Need to do a permutation for ',typeString, ' to ', newTypeString
                if typeString in permutationSignList:
                    beforeReturn=expandSpab(mtree.group('beforeReturn'))
                    afterReturn=expandSpab(mtree.group('afterReturn'))
                    newFunction= 'complex<T> A_' + newTypeString + '_' + newHelicityString;
                    newFunction+= permuteFunction(beforeReturn,perm) 
                    newFunction+= r' return complex<T>(-1,0) * ('
                    newFunction+= permuteFunction(afterReturn,perm) 
                    newFunction+=');}\n\n'
                else:
                    newFunction= 'complex<T> A_' + newTypeString + '_' + newHelicityString + permuteFunction(function,perm) +'\n\n'
                print 'New function generated for: ', newTypeString + '_' + newHelicityString
                output+=newFunction
                numberOfNewFunctions+=1
        else:
            print 'No function match for ',process+ str(number)
    
#        else:
#            print typeString,' not in processList '

outputFile.write(output)
#print 'Number of old functions: ', numberOfOldFunctions , '\n'
print 'Number of new functions: ', numberOfNewFunctions , '\n'