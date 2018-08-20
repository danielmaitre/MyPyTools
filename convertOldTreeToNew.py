#!/usr/bin/env python

"""
file = open("../../src/trees_eval/A0_2q2g1y_eval.cpp","r")
outputFile = open("SA_2q2g1y.hpp","w")
processSize=5
processList=[
             "qggyq",
             "qggqy",
             "qgqgy",
             "qqggy"
]
rotationList= {
    #   this needs to be commented becaue of a redundency in the A0_2q2g1y file 
    #         'qqggy':4 
}

process = 'A2q2g1y'

"""

"""
file = open("../../src/trees_eval/A0_2q1g2l_eval.cpp","r")
outputFile = open("SA_2q1g2l.hpp","w")
processSize=5
processList=[
#             "qgqll",
#             "qqgll"
]
rotationList= {
    #   this needs to be commented becaue of a redundency in the A0_2q2g1y file 
    #         'qqggy':4 
}

permutationList= {
             'qgqll':[0,1,2,4,3], 
             'qqgll':[0,1,2,4,3] 
}

permutationSignList= [
             'qgqll' ,             
             'qqgll' 
]


process = 'A2q1g2l'


"""

"""

THIS IS OBSOLETE SEE BELOW

file = open("../../src/trees_eval/A0_2q2g2l_eval.cpp.old","r")
#file = open("test.txt","r")
outputFile = open("SA_2q2g2l_slc.hpp","w")
#outputFile = open("test.out","w")
processSize=6
processList=[

]
rotationList= {
      'llqqgg':4,   # SSLC 
      'qllqgg':3 ,  # LC 
      'qgllqg':2    # SLC

}

permutationList= {
      'llqqgg':[2,3,4,5,1,0],   # SSLC 
#     need to invert quarks and gluons -> - sign   
      'gllqqg':[4,3,0,5,1,2],   # SSLC use the redundant cyclic permutations to do different permutations
#     need to invert quarks and gluons -> - sign invert l+l- --> sign   
      'ggllqq':[5,4,1,0,3,2],   # SSLC use the redundant cyclic permutations to do different permutations

      'qllqgg':[3,4,5,0,2,1],  # LC 

      'qgllqg':[4,5,0,1,3,2],    # SLC
#     need to invert quarks and gluons -> - sign   
      'gqgllq':[1,0,5,2,3,4],   # SLC
#     need to invert quarks and gluons -> - sign   invert l+l- --> sign
      'qgqgll':[2,1,0,3,5,4]    # SLC
}

permutationSignList= [
      'llqqgg',   # SSLC 
      'gllqqg',   # SSLC 
      'qllqgg',  # LC 
      'qgllqg',    # SLC
      'gqgllq'    # SLC
]

MinPC=1
MaxPC=44829

process = 'A2q2g2l'

"""

"""

THIS IS OBSOLETE SEE BELOW

file = open("../../src/trees_eval/A0_2q3g2l_eval.cpp.old","r")
#file = open("test.txt","r")
outputFile = open("SA_2q3g2l_slc.hpp","w")
#outputFile = open("test.out","w")
processSize=7
processList=[
            'qgggqll',
            'qggqgll',
            'qgqggll',
            'qqgggll' 
]
rotationList= {
#      'llqqgg':4,   # SSLC 
#      'qllqgg':3 ,  # LC 
#      'qgllqg':2    # SLC

}

permutationList= {
      'llqgggq':[2,3,4,5,6,1,0],   # LC
      'llqggqg':[2,3,4,5,6,1,0],  # LC
      'llqgqgg':[2,3,4,5,6,1,0],   # LC
      'llqqggg':[2,3,4,5,6,1,0],   # LC

      'gggllqq':[6,5,2,1,0,3,4],   # SSSLC
      'ggllqqg':[5,4,1,0,6,3,2],   # SSSLC

      'qggllqg':[0,6,5,2,1,3,4],   # SSSLC
      'ggllqgq':[6,5,4,1,0,3,2],   # SSSLC

      'gqgllqg':[1,0,6,5,2,3,4],   # SSSLC
      'qgllqgg':[0,6,5,4,1,3,2]   # SSSLC

       
}

permutationSignList= [
                      'llqgggq',                      
                      'llqggqg',                      
                      'llqgqgg',                      
                      'llqqggg',                      

                      'ggllqqg',
                      
                      'ggllqgq',                      
                      'qgllqgg'
]

MinPC=1
MaxPC=44829

process = 'A2q3g2l'

"""
"""

file = open("../../src/trees_eval/A0_2q1g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_2q1g.hpp","w")
#outputFile = open("test.out","w")
processSize=3
processList=[   #use all permutations for speed
            'qgq',
            'gqq',
            'qqg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A2q1g'

"""

"""

file = open("../../src/trees_eval/A0_2q2g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_2q2g.hpp","w")
#outputFile = open("test.out","w")
processSize=4
processList=[   #use all permutations for speed
            'qggq',
            'qqgg',
            'gqqg',
            'ggqq',
            
            'qgqg',
            'gqgq'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A2q2g'

"""

"""
file = open("../../src/trees_eval/A0_2q3g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_2q3g.hpp","w")
#outputFile = open("test.out","w")
processSize=5
processList=[   #use all permutations for speed
            'qgggq',
            'qqggg',
            'gqqgg',
            'ggqqg',
            'gggqq',
            
            'qgqgg',
            'gqgqg',
            'ggqgq',
            'qggqg',
            'gqggq'


]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A2q3g'


"""

"""

file = open("../../src/trees_eval/A0_2q4g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_2q4g.hpp","w")
#outputFile = open("test.out","w")
processSize=6
processList=[   #don't use all permutations for space
            'qggggq',
            'qgggqg',
            'qggqgg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]


process = 'A2q4g'



"""

"""

file = open("../../src/trees_eval/A0_7g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_7g.hpp","w")
#outputFile = open("test.out","w")
processSize=7
processList=[   #don't use all permutations for space
            'ggggggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]

equivalentlist = {
         'ggggggg': [ 
                      [1,2,3,4,5,6,0],
                      [2,3,4,5,6,0,1],
                      [3,4,5,6,0,1,2],
                      [4,5,6,0,1,2,3],
                      [5,6,0,1,2,3,4],
                      [6,0,1,2,3,4,5],
                      [0,1,2,3,4,5,6]
                      ]         
}


process = 'A7g'


"""

"""

file = open("../../src/trees_eval/A0_8g_eval.cpp","r")
#file = open("test.txt","r")
outputFile = open("SA_8g.hpp","w")
#outputFile = open("test.out","w")
processSize=8
processList=[   #don't use all permutations for space
            'gggggggg'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]

equivalentlist = {
         'gggggggg': [ 
                      [1,2,3,4,5,6,7,0],
                      [2,3,4,5,6,7,0,1],
                      [3,4,5,6,7,0,1,2],
                      [4,5,6,7,0,1,2,3],
                      [5,6,7,0,1,2,3,4],
                      [6,7,0,1,2,3,4,5],
                      [7,0,1,2,3,4,5,6]
                      ]         
}

process = 'A8g'

"""

"""



file = open("../../src/trees_eval/A0_2q2g2l_eval.cpp.old","r")
#file = open("test.txt","r")
outputFile = open("SA_2q2g2l_new.hpp","w")
#outputFile = open("test.out","w")
processSize=6
processList=[   #don't use all permutations for space
            'qggqll',
            'qgqgll',
            'qqggll'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
#      'qllqgg':3 ,  # LC 
#       'qgllqg':2    # SLC
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]

equivalentlist = {
         'qggqll': [ 
                      [0,1,2,3,4,5],
                      [0,1,2,3,5,4],
                      [3,2,1,0,4,5],
                      [3,2,1,0,5,4]
                      ],
        'qgqgll': [ 
                      [0,1,2,3,4,5],
                      [0,1,2,3,5,4],
                      [2,1,0,3,4,5],
                      [2,1,0,3,5,4]
                      ],
        'qqggll': [ 
                      [0,1,2,3,4,5],
                      [0,1,2,3,5,4],
                      [1,0,3,2,4,5],
                      [1,0,3,2,5,4]
         ]
}




process = 'A2q2g2l'



"""



file = open("../../src/trees_eval/A0_2q3g2l_eval.cpp.old","r")
#file = open("test.txt","r")
outputFile = open("SA_2q3g2l_new.hpp","w")
#outputFile = open("test.out","w")
processSize=7
processList=[   #don't use all permutations for space
            'qgggqll',
            'qggqgll',
            'qgqggll',
            'qqgggll'
]
rotationList= {
#      'llqqgg':4,   # SSLC 
#      'qllqgg':3 ,  # LC 
#       'qgllqg':2    # SLC
}

permutationList= {
#      'llqgggq':[2,3,4,5,6,1,0],   # LC
}

permutationSignList= [
]

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




process = 'A2q3g2l'




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

alreadyComputed = {
}

for i in equivalentlist:
    alreadyComputed[i]=list()





numberOfOldFunctions=0
numberOfNewFunctions=0
nameMap = {'ga':'y' , 'q':'q' , 'e':'l'}

particlePattern= '(?P<part>((?P<type>(q|q|ga|e))?(?P<helicity>m|p)))'
p2= re.compile( particlePattern )

numberPattern = r'(?P<number>\d*)' + r':(?P<process>(\s*'+ particlePattern +'){'+str(processSize)+'})'
np = re.compile( numberPattern )
iterator = np.finditer(text)
for match in iterator:
    number=int(match.group('number'))
    pattern = r'\b' + str(number) + r':(?P<process>(\s*'+ particlePattern +'){'+str(processSize)+'})'
    p = re.compile( pattern )
    
    m = p.search( text )
    if m:
        print 'Match found: ', m.group()
        numberOfOldFunctions+=1
        iterator = p2.finditer(m.group('process'))
        typeString = ""
        helicityString = ""
        for match in iterator:
            ty = match.group('type')
            if ( ty == None ):
                typeString+='g'
            else :
                typeString+=nameMap[ty]
            he = match.group('helicity')    
            helicityString+=he    
        print typeString
        print helicityString
        if (typeString in processList) or (typeString in rotationList) or (typeString in permutationList):
            needed=True
            if typeString in equivalentlist:
                allowedPerm=equivalentlist[typeString]
                if allowedPerm != None:
                    for i in range(0,len(allowedPerm)):
                        permuted=permute(helicityString,allowedPerm[i])
    #                    print typeString
     #                   print alreadyComputed
                        if permuted in alreadyComputed[typeString]:
                            needed=False
                            print 'No need for ' , typeString ,'_',helicityString,' since I have ', permuted
            if (needed == False):
                continue
            if typeString in equivalentlist:
                alreadyComputed[typeString].append(helicityString)
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
print 'Number of old functions: ', numberOfOldFunctions , '\n'
print 'Number of new functions: ', numberOfNewFunctions , '\n'