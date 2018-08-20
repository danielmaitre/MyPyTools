#!/usr/bin/env python

"""

file = open("../../src/trees_eval/A0_2q4g2l_eval.cpp","r")
outputFile = open("SA_2q4g2l.hpp","w")
processSize=8
processList=[
             "qggggqll"
]

rotationList= {
    #   this needs to be commented becaue of a redundency in the A0_2q2g1y file 
    #         'qqggy':4 
}

permutationList= {
}

permutationSignList= [
]


process = 'A2q4g2l'

"""


file = open("../../src/trees_eval/A0_2q5g2l_eval.cpp","r")
outputFile = open("SA_2q5g2l.hpp","w")
processSize=9
processList=[
             "qgggggqll"
]

rotationList= {
    #   this needs to be commented becaue of a redundency in the A0_2q2g1y file 
    #         'qqggy':4 
}

permutationList= {
}

permutationSignList= [
]


process = 'A2q5g2l'




text = file.read()
output =""



import re

def makeTemplatetranslator(templateList): 
    translationtable=dict([(templateList[x],str(x)) for x in range(0,len(templateList))]) 
    return lambda matchobj: translationtable[matchobj.group()] 



spinorFunctionPattern = '((?P<fn>spb|spa|s)\((?P<i>\d),(?P<j>\d)\))'


spinorFunctionPattern = '((?P<fn>spb|spa|s)\((?P<i>\d),(?P<j>\d)\))'

particlePattern= '(?P<part>((?P<type>(q|qb|ga|l|lb))?(?P<helicity>m|p)))'
part= re.compile( particlePattern )
nameMap = {'ga':'y' , 'q':'q', 'qb':'q' , 'e':'l', 'l':'l' , 'lb':'l' }

processPattern= particlePattern+'{'+str(processSize)+'}'

treePattern = r'template <(?P<templateParams>(int i\d, ){'+str(processSize)+'})class T> complex<T>\s*'
treePattern += process + '_'  
treePattern += '(?P<process>'+processPattern+')' 
treePattern += r'_eval\(const eval_param<T>& ep, const mass_param_coll& masses\)'
treePattern += r'\s*\{'
treePattern += r'(?P<functionBody>.*?)'
treePattern += r'\}'
ptree=re.compile(treePattern,re.DOTALL)



iterator = ptree.finditer(text)
for match in iterator:
    print '========================='
    print match.group()
    iterator = part.finditer(match.group('process'))
    typeString = ""
    helicityString = ""
    for match2 in iterator:
        ty = match2.group('type')
        if ( ty == None ):
            typeString+='g'
        else :
            typeString+=nameMap[ty]
        he = match2.group('helicity')    
        helicityString+=he    
    print helicityString
    print typeString
    tparams=match.group('templateParams')
    iparams=list()
    tp= re.compile( r'i\d' )
    iterator = tp.finditer(tparams)
    for tmatch in iterator:
        iparams.append(tmatch.group())
#    print iparams
    translateTargs = makeTemplatetranslator(iparams)
    newFunctionBody=re.sub(r'i\d',translateTargs,match.group('functionBody'))
    newFunction =  r'complex<T> ' +  'A_' +typeString + '_'+helicityString+'_eval'
    newFunction +='(const eval_param<T>& ep, const mass_param_coll& masses)'
    newFunction += '{'
    newFunction += newFunctionBody
    newFunction += '}\n\n'
    print newFunction
    output+=newFunction
    print '========================='
outputFile.write(output)