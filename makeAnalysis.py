import re

jetPtCut=25
jetEtaCut=4.5
jetAlgorithm='AntiKt'
nonPartonPtCut=20

from optparse import OptionParser
parser = OptionParser(usage="%prog NJETS PART")

parser.add_option("-p", "--pdf", dest='pdfSet',
                  default="CT10.LHgrid", help="pdf set to be used")
parser.add_option("-r", "--radius", dest="radius",
                   default=0.4,help="radius of the jet algorithm",type=float)
parser.add_option("-n", "--nonparton", dest="nonparton",
                   default='electron,positron',help="non-partons",type=str)

opts, args = parser.parse_args()

njets=int(args[0])
part=args[1]

nonpartons=opts.nonparton.split(',')

runPartTemplate='''
<Run>

JET_PT_CUT %(jetPtCut)s
JET_ET_CUT -25
JET_ETA_CUT %(jetEtaCut)s
MinJets %(njets)d
MaxJets %(njetsplus1)d
JetAlgorithm %(jetAlgorithm)s
ConeRadius %(radius)f
FileName in.root
UseNbFormula no
MaxWeight 1e15
</Run>
'''

processTemplate='''
<Process>

ParticlesNames { %(nonpartons)s }
NbrPartons %(npartons)d
NonPartons { %(nonPartonsIndices)s }
AlphasPower %(njets)d

</Process>
'''

cutsTemplate='''
<Cuts>
%(additionalCuts)s

</Cuts>

'''

observablesTemplate='''
<Observables>
Njets: NJet ;
%(additionalObservables)s
</Observables>

'''

scalesTemplate='''
<Scales>
OriginalWeight Orig
%(weightType)s HTallp  ObservableScale HTallp 

</Scales>
'''

pdfTemplate='''
<PDF>
PdfSetName %(pdfSet)s
</PDF>
'''

histogramsTemplate='''
<Histograms>

CrossSection xsection
%(additionalHistograms)s
</Histograms>
'''


obsText=''
histText=''
#go to njets + 1 
for j in range(1,njets+2):
    obsText=obsText+'Jpt%d: JetPt %d ;\n' % (j,j)
    histText=histText+'Histogram JetPt %d 50 [ 0,1000 ] h_pt_j%d "Pt of jet %d"\n' % (j,j,j)
    histText=histText+'Histogram JetEta %d 22 [ -4.4 , 4.4 ] h_eta_j%d "eta of jet %d"\n' % (j,j,j)

cutText=''

values={}

values['nonPartonsIndices']=''


if '' in nonpartons: 
    nonpartons.remove('')

#non partons come first:
if len(nonpartons)==0:
    values['nonPartonsIndices']=''
if len(nonpartons)==1:
    values['nonPartonsIndices']='0'
if len(nonpartons)==2:
    values['nonPartonsIndices']='0,1'


for np in nonpartons:
    print "np: '%s'"%np
    if np != '' and np != ' ':
        histText=histText+'Histogram Pt %s 200 [ 0,2000 ] h_pt_%s "Pt of the %s"\n' % (np,np,np)
        cutText=cutText+'PtCut %s %f 20000\n' % (np,nonPartonPtCut)



weightTypes={
    'loop':'LoopWeight',
    'real':'RealWeight',
    'born':'BornWeight',
    'vsub':'VsubWeight',
    'V':'LoopWeight',
    'R':'RealWeight',
    'B':'BornWeight',
    'I':'VsubWeight'
    }




newPartRegex=re.compile('[BIRV]\d\d\d')

values['njets']=njets
values['njetsplus1']=njets+1
values['npartons']=njets+1
values['additionalObservables']=obsText
values['additionalHistograms']=histText
values['additionalCuts']=cutText
if newPartRegex.match(part):
    values['weightType']=weightTypes[part[0]]
else:
    values['weightType']=weightTypes[part[:4]]
values['pdfSet']=opts.pdfSet
values['radius']=opts.radius
values['nonpartons']=','.join(nonpartons)
values['jetAlgorithm']=jetAlgorithm
values['jetPtCut']=jetPtCut
values['jetEtaCut']=jetEtaCut
values['nonPartonPtCut']=nonPartonPtCut


allText=(
    runPartTemplate+
    processTemplate+
    cutsTemplate+
    observablesTemplate+
    scalesTemplate+
    pdfTemplate+
    histogramsTemplate
    ) % values
analysisFile=open('analysis.dat','w')
analysisFile.write(allText)
analysisFile.close()
histInfo='''
Jet algorithm:        %(jetAlgorithm)s
Radius:               %(radius)s
Jet pt cut:           %(jetPtCut)s
Jet Eta cut:          %(jetEtaCut)s
''' % values
for np in nonpartons:
    histInfo=histInfo+'''
%s pt cut:        %s
''' %  (np,nonPartonPtCut)
histInfo+='''
PDF set (for HTallp): %(pdfSet)s
''' % values

hif=open('HistogramInfo.info','w')

hif.write(histInfo)
hif.close()
