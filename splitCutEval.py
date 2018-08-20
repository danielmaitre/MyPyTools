#
#  This has been used to split files such as PRO_wCI.cpp
#  for the processes: include R_6g_eval.inc
#
#  C_2q2g1y
#  C_2q2Q1y
#  C_5g_wCI
#  C_2q2g2l
#  C_2q3g
#  C_6g_wCI
#  C_2q2Gl2l
#  C_4g1ph
#
#  the script creates a .inc file to be included in the Makefile.am 
#  and a header PRO_split.hpp to be included in a modified 
#  PRO_wCI.cpp file that needs to be named PRO_wCI_split.cpp. 
#  In this file all the templates need to be removed along with the 
#  #define's 


import re
import sys

templateRegex=r'template <class T> (?P<type>[\w<>]+) (?P<name>\w+)\s*\((?P<args>.*?)\)\s*\{(?P<body>.*?;)\s*\}'

simpleTemplateRegex=r'(?P<decl>template <class T>\s*(?P<type>[^\(]*?)\s*(?P<name>\w*?)\s*\((?P<args>[^{]*?)\))\s*\{(?P<body>\s*return (?P<callee>[^\(]+)\([^{]*?\)\s*;\s*)\}'

defineRegex=r'#define (?P<name1>_C_\w+)\s+(?P<name2>\w+)'

defineCASERegex=r'#define (?P<name1>_CASE_\w+)\s+case (?P<name2>\d+)\s+:\s*\\\s*return\s+&\w+'
#defineCASERegex=r'#define (?P<name1>_CASE_\w+)\s+case (?P<name2>\d+)\s+:\s*\\'




instRegex=r'template SeriesC<(?P<type>\w+)> \( \*(?P<name>\w+)_eval\(int hc\)\)\n\s*\(const eval_param<\w+>&, const \w+&\);'
#instRegex=r'template SeriesC<(?P<type>\w+)> \( \*(?P<name>\w+)_eval'

fnRegex=r'template <class T> SeriesC<T> (?P<name>\w+)\s*\(const eval_param<T>& ep,\s*const T& mu\){.*?return.*?}'

fn2Regex=r'template <class T> SeriesC<T> (?P<name>_C_\w+)\s*\(\s*const eval_param<T>& ep,\s*const T& mu\){.*?return.*?}'


fn3Regex=r'template <class T> SeriesC<T> \(\s*\*(?P<name>\w+)_Ptr_eval\( int hc\)\).*?default:.*?}\s*}'


process=sys.argv[1]

fin=open('%s_eval.cpp' % process,'r')
txt=fin.read()

names=[]
suffixes=set()

inst={}
fns={}
defines={}
fn2s={}
fn3s={}


print 'names'
for m in re.finditer(instRegex,txt,re.DOTALL):
    print m.group('name')
    names.append(m.group('name'))
    suffix='_'.join(m.group('name').split('_')[1:-1])
    print suffix
    suffixes.add(suffix)

for suffix in suffixes:
    fns[suffix]=[]
    defines[suffix]=[]
    fn2s[suffix]=[]
    fn3s[suffix]=[]


for m in re.finditer(instRegex,txt,re.DOTALL):
    name=m.group('name')
    suffix='_'.join(m.group('name').split('_')[1:-1])
    inst[suffix]=m.group()

for m in re.finditer(fnRegex,txt,re.DOTALL):
    name=m.group('name')
    suffix='_'.join(name.split('_')[2:])
    print suffix
    fns[suffix].append(m.group())

for m in re.finditer(defineRegex,txt,re.DOTALL):
    name=m.group('name1')
    suffix='_'.join(name.split('_')[3:])
    print suffix
    defines[suffix].append(m.group())

for m in re.finditer(defineCASERegex,txt,re.DOTALL):
    name=m.group('name1')
    suffix='_'.join(name.split('_')[3:])
    print suffix
    defines[suffix].append(m.group())

for m in re.finditer(fn2Regex,txt,re.DOTALL):
    name=m.group('name')
    suffix='_'.join(name.split('_')[3:])
    print suffix
    fn2s[suffix].append(m.group())

for m in re.finditer(fn3Regex,txt,re.DOTALL):
    name=m.group('name')
    suffix='_'.join(name.split('_')[1:])
    print suffix
    fn3s[suffix].append(m.group())


    

    

cppFileHead='''

#include "C_2q2g2l_eval.h"
#include "integrals_ep.h"
 
using namespace std;
 
namespace BH  {
 
 
#define _VERBOSE 0
 
#define SPA(i,j) ep.spa(i-1,j-1)
#define SPB(i,j) ep.spb(i-1,j-1)
#define S(i,j) ep.s(i-1,j-1)
#define SS(i,j,k) ep.s(i-1,j-1,k-1)

template<class T> static inline complex<T> square(complex<T> x) 
{return(x*x);}
template<class T> static inline complex<T> cube(complex<T> x) 
{return(x*x*x);}


'''

cppFileFoot='''



} /* BH */

'''


for suffix in suffixes:
    fout=open('%(process)s_eval_%(suffix)s.cpp' % locals(),'w')
    fout.write(
        cppFileHead
    )
    fout.write('\n\n')
    fout.write(
        '\n'.join(fns[suffix])
    )
    fout.write('\n\n')
    fout.write(
        '\n'.join(defines[suffix])
    )
    fout.write('\n\n')
    fout.write(
        '\n'.join(fn2s[suffix])
    )
    fout.write('\n\n')
    fout.write(
        '\n'.join(fn3s[suffix])
    )
    fout.write('\n\n')
    fout.write(
        inst[suffix]
    )
    fout.write(
        cppFileFoot
    )
 
    fout.close()




incfile=open('%s_split.inc' % process ,'w')
incfile.write('ALL_%s=' % process)
incfile.write(' '.join(['%s_eval_%s.cpp' %(process,suffix)  for suffix in suffixes ]))
incfile.close()
