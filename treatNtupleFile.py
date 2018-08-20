import array
import ROOT
import sys
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="file to process", metavar="FILE",default=None)
parser.add_option( "--files", dest="files",
                  help="file containing the names of the files to process", metavar="FILE",default=None)
parser.add_option("-p", "--part", dest="part",
                  help="type of part")
parser.add_option("-d", "--description", dest="description",
                  help="description")
parser.add_option("-n", "--nbrjets",type="int", dest="nbrjets",
                  help="number of jets")
parser.add_option("-o", "--outfile", dest="outputfile",
                  help="output file")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
parser.add_option("-t", "--treename",
                   dest="treename", default='t3',
                  help="the name of the root tree")


(options, args) = parser.parse_args()

partstrings={
    'born':'B',
    'real':'R',
    'loop':'V',
#    'loop-lc':'V',
 #   'loop-fmlc':'V',
    'vsub':'I',
    }

newPartRegex=re.compile('(?P<letter>[BIRV])\d\d\d')

try:
    partLetter=partstrings[options.part[0:4]]
except:
    match=newPartRegex.match(options.part)
    if match:
        partLetter=match.group('letter')
    else:
        print "part %s not recognized!" % options.part
        sys.exit(1)

process=options.description
if options.part=='born' or options.part=='bornLO' or options.part[0]=='B' :
    ap=options.nbrjets
else:    
    ap=options.nbrjets+1


if options.filename:

    f=ROOT.TFile(options.filename,'READONLY')

    t=f.Get(options.treename)

elif options.files:
    t=ROOT.TChain(options.treename)
    filesfile=open(options.files,'r')
    if not filesfile:
        sys.exit()
    allFiles=filesfile.read().split()
    print allFiles
    RootFiles=[]
    for rf in allFiles: 
        t.Add(rf)
else:
    print "You have to specify --filename or --files."
    sys.exit()

fout=ROOT.TFile(options.outputfile,'RECREATE')




b=t.GetBranch("alphasPower")
if b:
    t.SetBranchStatus("alphasPower",0)
b=t.GetBranch("part")
if b:
    t.SetBranchStatus("part",0)





tt=t.CopyTree('')


print 'after cloneTree'
fout.ls()

tt.SetName('BHSntuples')
tt.SetTitle('BHS ntuples for process %s, %s part' % (process,options.part))

partString=array.array('c','%s\0' % partLetter)
alphasPower=array.array('i',[ap])

b=tt.Branch('part',partString,'part/C')
b2=tt.Branch('alphasPower',alphasPower,'alphasPower/S')

nEntries=tt.GetEntries()

for i in range(nEntries):
    b.Fill()
    b2.Fill()

print 'after fill'
fout.ls() 

fout.Delete('t3;*')

print 'after Delete'
fout.ls() 

tt.Write()
print 'after Write.before closing'
fout.ls()
fout.Close()



