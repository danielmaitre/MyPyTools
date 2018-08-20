#baseDir='/home/daniel/NtuplesAnalysis'
#studyName='Z1j-7TeV-HTp'
#jetAlgo='anti-kt'
#radius='5'
#ptCut='25'
#etCut='0'

import sys
import os
import string
import re
from array import array
from ROOT import gROOT, TH1D, TFile

import processUtils

templatePath='/home/daniel/NtuplesAnalysis'


def writeHistogram(dataFileName,columnName,histogramName,rootFileName):
	rootfile = TFile(rootFileName,'UPDATE')
	histogramDescription = histogramName
	datafile = open(dataFileName,'r')
	text = datafile.read()
	descrRegex=re.compile('# left_bin_size(?P<Entries>.*)')
	descriptionLine = descrRegex.search(text)
	#print descriptionLine.group()
	entries = re.finditer(r'(\w|-)+', descriptionLine.group('Entries'))
	entriesList=list()
	for match in entries:
			name=	match.group()
			if (name!='er'):
					entriesList.append(name)
	#print entriesList
	index=0
	if columnName in entriesList:
			index=entriesList.index(columnName)
	else: 
			print "No entry called ",columnName
			print 'entries are: ',entriesList
			return False
	#print index

	doubleRegex=r'-?[0-9]*\.?[0-9]+(e(\+|-)\d+)?'


	dataLineString=r'^\s*(?P<bin>'+doubleRegex+')'
	for i in range(0,index):	 # the index is 0-based
			dataLineString+=r'\s*'
			dataLineString+=doubleRegex # this is the normal entry
			dataLineString+=r'\s*'
			dataLineString+=doubleRegex # this is the error

	dataLineString+=r'\s*'
	dataLineString+='(?P<value>'+doubleRegex+')' # this is the normal entry
	dataLineString+=r'\s*'
	dataLineString+='(?P<error>'+doubleRegex+')' # this is the error
	dataLineString+=r'.*$'


	dataLineRegex=re.compile(dataLineString,re.MULTILINE)

	data = re.finditer(dataLineRegex, text)

	bins=list()
	values=list()
	errors=list()

	for match in data:
			bin=match.group('bin')
			value=match.group('value')
			error=match.group('error')
			bins.append(float(bin)) 
			values.append(float(value)) 
			errors.append(float(error)) 
	#	print 'bin: ',bin,' value ',value,' err ',error	 
	#print bins
	#print values
	#print errors
	dx= bins[1]-bins[0]
	variableWidth=False
	for i in range(0,len(bins)-1):
			if (abs((bins[i+1]-bins[i])/dx -1) >0.0001):
					#print "bin spacing is not constant: ",bins[i+1]-bins[i],'!=',	dx	
					#print "relative difference: ",abs((bins[i+1]-bins[i])/dx	) -1
					variableWidth=True

							


	if variableWidth:
		print "Variable bin width!"
		b=array('d',bins)
		hist = TH1D( histogramName, histogramDescription,len(bins)-1 ,b )
	else:
		hist = TH1D( histogramName, histogramDescription,len(bins)-1 ,bins[0] , bins[-1] )
	#print "bin 0: ",bins[0] ,"last bin: ", bins[-1], "nbr: ",len(bins)-1 

	for i in range(0,len(bins)):
			hist.SetBinContent(i+1,values[i])
			hist.SetBinError(i+1,errors[i])

	hist.Write()
	rootfile.Close()


class LogPlot(Exception):
	pass

def findHistogramInfo(dataFileName):
	datafile = open(dataFileName)
	text = datafile.read()
	doubleRegex=r'-?[0-9]*\.?[0-9]+(e(\+|-)\d+)?'
	regextext=r'#\s+(?P<plotType>\d+)\s+(?P<nbin>\d+)\s+'
	regextext+=r'(?P<min>'+doubleRegex+')\s+'
	regextext+=r'(?P<max>'+doubleRegex+')'
	info=re.compile(regextext)
	m=info.search(text)
	if m:
		if m.group('plotType') == '1':
			nbin=int(m.group('nbin'))-2
			minx=float(m.group('min'))
			maxx=float(m.group('max'))
			return nbin,minx,maxx
		elif  m.group('plotType') == '11':
			print "log plot, ignoring..."
			raise LogPlot
	else :
		print "Could not find histogram information"
		return None


def isSuitable(f):
	keyWords=string.split(f,'_')
	return cutsSpecs in keyWords and keyWords[0]=='all' 


particles = {
	'e+':'positron',
	'e-':'electron',
	'nueb':'neutrino',
	'nue':'neutrino'
}

def findParticles(text):
	res=[]
	rest=text
	for p in particles:
		if p in rest:
			#print particles[p],' found'
			res.append(particles[p])
			rest=rest.replace(p,'',1)
			#print rest
	return res







histoTypes=[]
#----------------------------
massRegex=re.compile(r'Mass(?P<particles>.*)\s*[ABCDEFGH0-9]*\.dat')
def massHistogram(match):
	ps=findParticles(match.group('particles'))
	if len(ps)==2:
		return 'Histogram 2Mass %s %s' % (ps[0],ps[1])
	else:
		return None

histoTypes.append( (massRegex,massHistogram) )
#----------------------------
ptRegex=re.compile(r'PT(?P<particles>.*)\s*[ABCDEFGH0-9]*\.dat')
def ptHistogram(match):
	ps=findParticles(match.group('particles'))
	if len(ps)==1:
		return 'Histogram Pt %s' % ps[0]
	elif len(ps)==2:
		return 'Histogram 2Pt %s %s' % (ps[0],ps[1])
	else :
		return None
histoTypes.append( (ptRegex,ptHistogram) )
#----------------------------
mtRegex=re.compile(r'MT2(?P<particles>.*)\s*[ABCDEFGHIJKLMN0-9]*\.dat')
def mtHistogram(match):
	ps=findParticles(match.group('particles'))
	if len(ps)==2:
		return 'Histogram 2Mt %s %s' % (ps[0],ps[1])
	else:
		return None
histoTypes.append( (mtRegex,mtHistogram) )
#----------------------------
jetPtRegex=re.compile(r'jetsjet11pt[ABCDEFGHIJKLMN]*(?P<n>\d)\.dat')
def jetPtHistogram(match):
	return 'Histogram JetPt %s ' % match.group('n')

histoTypes.append( (jetPtRegex,jetPtHistogram) )
#----------------------------
allpHTRegex=re.compile(r'AllpHT[ABCDEFGHIJKLMN0-9]*\.dat')
def allpHTHistogram(match):
	return 'Histogram HT ' 

histoTypes.append( (allpHTRegex,allpHTHistogram) )

#----------------------------
jetsHTRegex=re.compile(r'jetsHT[ABCDEFGHIJKLMN0-9]*\.dat')
def allpHTHistogram(match):
	return 'Histogram HT { }' 

histoTypes.append( (allpHTRegex,allpHTHistogram) )

#----------------------------
jetEtRegex=re.compile(r'jetsjet11Et[ABCDEFGHIJKLMN]*(?P<n>\d)\.dat')
def jetEtHistogram(match):
	return 'Histogram JetEt %s ' % match.group('n')

histoTypes.append( (jetEtRegex,jetEtHistogram) )
#----------------------------
jetEtaRegex=re.compile(r'jetsjet11eta[ABCDEFGHIJKLMN]*(?P<n>\d)\.dat')
def jetEtaHistogram(match):
	njet=int(match.group('n'))
	if njet == 0:
		# this is when all jets are booked into the histogram, the same information is contained in the separate jet histos
		return None
	else:
		return 'Histogram JetEta %s ' % match.group('n')

histoTypes.append( (jetEtaRegex,jetEtaHistogram) )
#----------------------------
etaRegex=re.compile(r'Eta(?P<particles>.*)\s*[ABCDEFGHIJKLMN0-9]*\.dat')
def etaHistogram(match):
	ps=findParticles(match.group('particles'))
	if len(ps)==1:
		return 'Histogram Eta %s' % ps[0]
	elif len(ps)==2:
		return 'Histogram DeltaEta %s %s' % (ps[0],ps[1])
	else:
		None
histoTypes.append( (etaRegex,etaHistogram) )
#----------------------------
threeJetMassRegex=re.compile(r'3Massjjj[ABCDEFGHIJKLMN0]*\.dat')
def threeJetMassHistogram(match):
	return 'Histogram JetsMass { 1 , 2 , 3 }'
histoTypes.append( (threeJetMassRegex,threeJetMassHistogram) )
#----------------------------
threeJetMass2Regex=re.compile(r'3Mass2jjj[ABCDEFGHIJKLMN0]*\.dat')
def threeJetMass2Histogram(match):
	return 'Histogram JetsMass2 { 1 , 2 , 3 }'
histoTypes.append( (threeJetMass2Regex,threeJetMass2Histogram) )
#----------------------------
threeJetPtRegex=re.compile(r'PTjjj[ABCDEFGHIJKLMN0]*\.dat')
def threeJetPtHistogram(match):
	return 'Histogram JetsPt { 1 , 2 , 3 }'
histoTypes.append( (threeJetPtRegex,threeJetPtHistogram) )
#----------------------------
deltaEtaRegex=re.compile(r'TwoDEtaj-0j-0[ABCDEFGHIJKLMN0]*\.dat')
def deltaEtaHistogram(match):
	return 'Histogram DeltaEta'
histoTypes.append( (deltaEtaRegex,deltaEtaHistogram) )
#----------------------------
twoptjetRegex=re.compile(r'TwoPTj-(?P<n1>)j-(?P<n2>)[ABCDEFGHIJKLMN0]*\.dat')
def twoptjetHistogram(match):
	return 'Histogram JetsPt { %s , %s }' %(int(match.group('n1'))+1,int(match.group('n2'))+1)
histoTypes.append( (twoptjetRegex,twoptjetHistogram) )
#----------------------------



histogramMode='W4'

def writeAllHistograms(name,dataFile,studyName,jetAlgo,radius,ptCut):
	if histogramMode=='W4':
		rootFileBaseName='%s_%s-R%s_PT%s' % (studyName,jetAlgo,radius,ptCut)
		writeHistogram(dataFile,'LO','h_%s' % name ,rootFileBaseName+'_bornLO.root')
		writeHistogram(dataFile,'NLO','h_%s' % name ,rootFileBaseName+'_NLO.root')
		writeHistogram(dataFile,'born','h_%s' % name ,rootFileBaseName+'_born.root')
		writeHistogram(dataFile,'real-2q','h_%s' % name ,rootFileBaseName+'_real-2.root')
		writeHistogram(dataFile,'real-4q','h_%s' % name ,rootFileBaseName+'_real-4q.root')
		writeHistogram(dataFile,'vsub','h_%s' % name ,rootFileBaseName+'_vsub.root')
		writeHistogram(dataFile,'loop-lc','h_%s' % name ,rootFileBaseName+'_loop-lc.root')
		return True
	if histogramMode in ['Z1j','Z2j']:
		rootFileBaseName='%s_%s-R%s_PT%s' % (studyName,jetAlgo,radius,ptCut)
		writeHistogram(dataFile,'LO','h_%s' % name ,rootFileBaseName+'_bornLO.root')
		writeHistogram(dataFile,'NLO','h_%s' % name ,rootFileBaseName+'_NLO.root')
		writeHistogram(dataFile,'born','h_%s' % name ,rootFileBaseName+'_born.root')
		writeHistogram(dataFile,'vsub','h_%s' % name ,rootFileBaseName+'_vsub.root')
		writeHistogram(dataFile,'loop','h_%s' % name ,rootFileBaseName+'_loop.root')
		return True
	if histogramMode in ['Z3j']:
		rootFileBaseName='%s_%s-R%s_PT%s' % (studyName,jetAlgo,radius,ptCut)
		writeHistogram(dataFile,'LO','h_%s' % name ,rootFileBaseName+'_bornLO.root')
		writeHistogram(dataFile,'NLO','h_%s' % name ,rootFileBaseName+'_NLO.root')
		writeHistogram(dataFile,'born','h_%s' % name ,rootFileBaseName+'_born.root')
		writeHistogram(dataFile,'vsub','h_%s' % name ,rootFileBaseName+'_vsub.root')
		writeHistogram(dataFile,'loop-lc','h_%s' % name ,rootFileBaseName+'_loop-lc.root')
		writeHistogram(dataFile,'loop-slc','h_%s' % name ,rootFileBaseName+'_loop-slc.root')
		return True
	if histogramMode=='None':
		return True		
	print 'No histogram mode specified, assume None...'
	return False

plotTemplate="""
<Plot>
File {hname}.ps
Title \"{hname} {part}\"
DoRatio yes
Errors yes
ErrorsE yes

<Histogram>
Type Histogram
File {rfileF}
Name {hname}
Title \"Fernando\"
</Histogram>

<Histogram>
Type Histogram
File {rfileD}
Name {hname}
Title \"Ntuples\"
</Histogram>

</Plot>
"""

def writePlot(histogramName,FileBaseName):
	text=''
	LOplot= { 'hname' : histogramName, 'rfileF': FileBaseName+'_bornLO.root', 'rfileD':'histograms_bornLO','part':'born LO' }
	text += plotTemplate.format(**LOplot)
	NLOplot= { 'hname' : histogramName, 'rfileF': FileBaseName+'_NLO.root', 'rfileD':'combinedNLO.root' ,'part':'NLO'}
	text += plotTemplate.format(**NLOplot)
	realplot= { 'hname' : histogramName, 'rfileF': FileBaseName+'_real.root', 'rfileD':'histograms_real.root' ,'part':'real'}
	text += plotTemplate.format(**realplot)
	loopplot= { 'hname' : histogramName, 'rfileF': FileBaseName+'_loop.root', 'rfileD':'histograms_loop.root' ,'part':'loop'}
	text += plotTemplate.format(**loopplot)
	vsubplot= { 'hname' : histogramName, 'rfileF': FileBaseName+'_vsub.root', 'rfileD':'histograms_vsub.root' ,'part':'vsub'}
	text += plotTemplate.format(**vsubplot)
	return text


def getHistograms(files,info):
	#print files
	plots=[ string.join(string.split(x,'_')[4:],'') for x in files ]
	print '# of plots: %s ' % len(plots)
	print '# of files: %s ' % len(files)
	histograms=''
	for pl,f in zip(plots,files):
		found=False
		for r,fn in histoTypes:
			match =r.match(pl)
			if match:
				print "found match for : ",pl
				#print fn(match)
				#print f
				histInfo = fn(match)  
				if not histInfo:
					print '    but not a true match... ' 
					continue
				try:
					hinfo= findHistogramInfo(info['workingPath']+f)
				except LogPlot:
					found = True
					break
				binInfo=''
				if hinfo:
					binInfo = ' %s [ %s , %s ] ' %	hinfo
					name=string.split(pl,'.')[0]
					nameInfo = ' h_%s "%s"'	 % ( name , "plot for "+name ) 
					histograms+= histInfo+binInfo+nameInfo+'\n'
					writeAllHistograms(name,info['workingPath']+f,info['studyName'],info['jetAlgo'],info['radius'],info['roundedPtCut'])
					found=True
					break
				else :
					print 'No bin info for file %s ' % ( pl )
		if not found:
			print "don't understand : ",pl
						
						
						
	return histograms
	


algoNames={
	'anti-kt':'AntiKt',
	'kt':'Kt',
	'siscone':'Siscone',
	}

def genAnalysisFile(info,files,workingPath):
	template=open('%s/comparisonAnalysis.template' % templatePath)
	text= template.read()
	jetCutInfo='JET_PT_CUT {ptcut}\nJET_ET_CUT {etcut}'.format(**info)
	process=info['process']
	info.update(processUtils.getInfo(process))
	info['jetCutInfo']=jetCutInfo
	info['processBlock'] = processUtils.getProcessBlock(process)
	info['algoName'] = algoNames[info['jetAlgo']]
	info['algoRadius'] = '0.{radius}'.format(**info)
	info['njetsplusone'] = info['njets']+1
	info['histogramsBlock'] = getHistograms(files,info)
	#print info
	return text.format(**info)

particleFromPdgCodes = {
	'11' : 'electron',
	'-11' : 'positron',
	'12' : 'neutrino',
	'-12' : 'neutrino'
	}

jetModes = {
	'0' : 'kt',
	'20' : 'siscone',
	'40' : 'anti-kt'
	}

def parseAnalysisFile(fileName):
	file=open(fileName)
	text=file.read()
	regex=re.compile(r'BEGIN_ANALYSIS \{(.*?)\} END_ANALYSIS',re.DOTALL)
	partPieceRegex=re.compile(r'PATH_PIECE\s+(?P<name>.*)')
	PTselRegex=re.compile(r'OnePTSel\s+(?P<pdg>-?\d+)\s+0\s+0\s+(?P<min>[+-]?\d*[0-9.]\d*)\s+(?P<max>[+-]?\d*[0-9.]\d*)\s+')
	EtaselRegex=re.compile(r'OneEtaSel\s+(?P<pdg>-?\d+)\s+0\s+0\s+(?P<min>[+-]?\d*[0-9.]\d*)\s+(?P<max>[+-]?\d*[0-9.]\d*)\s+')
	TwoMassselRegex=re.compile(r'TwoMassSel\s+(?P<pdg1>-?\d+)\s+0\s+(?P<pdg2>-?\d+)\s+0\s+(?P<min>[+-]?\d*[0-9.]\d*)\s+(?P<max>[+-]?\d*[0-9.]\d*)\s+')
	jetRegex=re.compile(r'JetMode (?P<mode>\d+)')
	jetParamsRegex=re.compile(r'Finder\s+93\s+(?P<ptcut>[+-]?\d*[0-9.]\d*)\s+(?P<etamin>[+-]?\d*[0-9.]\d*)\s+(?P<etamax>[+-]?\d*[0-9.]\d*)\s+(?P<radius>[+-]?\d*[0-9.]\d*)\s+1\s*(?P<f>[+-]?\d*[0-9.]\d*)?')


	iterator= regex.finditer(text)
	infos=[]
	for match in iterator:
		info={}
                print match.group()
                sys.stdout.flush()
		m= partPieceRegex.search(match.group())
		if m:
			name = m.group('name')
			info['process']=string.split(name,'-')[0]
			
		it= jetRegex.finditer(match.group())
		modes=[ m.group('mode') for m in it]
		if len(modes) != 1:
			print "unexpected length for the modes vector ! "
		info['jetAlgo']=jetModes[modes[0]]
		it= jetParamsRegex.finditer(match.group())
		for m in it :
			info['radius'] = string.split(m.group('radius'),'.')[1]
			etamin=float(m.group('etamin'))
			etamax=float(m.group('etamax'))
			if etamin==-etamax:
				info['etacut']=m.group('etamax')
			else:
				print 'Non symmetric eta cut!'
			info['f'] = m.group('f')
			etorptcut=float(m.group('ptcut'))
			if etorptcut > 0 :
				info['ptcut'] = etorptcut
				info['etcut'] = -etorptcut
			else:
				info['ptcut'] = etorptcut
				info['etcut'] = -etorptcut
			#print info
		cuts=''
		it= PTselRegex.finditer(match.group())
		for m2 in it:
			cuts += 'PtCut {0} {1} {2}\n'.format(particleFromPdgCodes[m2.group('pdg')],m2.group('min'),m2.group('max'))
		it= EtaselRegex.finditer(match.group())
		for m2 in it:
			cuts += 'ObservableCut [ Eta {0} ] {{ {1} , {2} }} \n'.format(particleFromPdgCodes[m2.group('pdg')],m2.group('min'),m2.group('max'))
		it= TwoMassselRegex.finditer(match.group())
		for m2 in it:
			cuts+= 'ObservableCut [ 2Mass {0} {1} ] [[ {2} , {3} }} \n'.format(particleFromPdgCodes[m2.group('pdg1')],particleFromPdgCodes[m2.group('pdg2')],m2.group('min'),m2.group('max'))
		info['cutsBlock']=cuts
		infos.append(info)
	return infos
		
def extractAllPlots(info):
	files=os.listdir(info['workingPath'])
	files.sort()
	cutsSpecs='%s-R%s-Pt%s' % (info['jetAlgo'],info['radius'],info['roundedPtCut'])
	#print cutsSpecs
	suitableFiles=[]
	for f in files:
		keyWords=string.split(f,'_')
		if cutsSpecs in keyWords and keyWords[0]=='all' :
			suitableFiles.append(f)
	analysisFileName='analysis_%s_%s.m4' % ( info['studyName'], cutsSpecs ) 
	analysisText = genAnalysisFile(info,suitableFiles,info['workingPath'])
	af=open(analysisFileName,'w')
	af.write(analysisText)



def analyseAll(Dir,analysisFile):
	fullpath=''
	if Dir[0] == '/' :
		fullpath = Dir
	else:
		fullpath = os.environ['PWD']+'/'+Dir
	dirs = string.split(fullpath,'/')
	baseDir='/'.join(dirs[:-1])
	#removes _plot
	studyName='_'.join(string.split(dirs[-1],'_')[:-1])
	workingPath='%s/html/collected_data/' % (fullpath)

	#print files
#	 SherpaAnalysisFile='%s/data/Analysis_Z1j-7TeV-HTp_bornLO_central-mu.dat' % (fullpath)
#	SherpaAnalysisFile='%s/Analysis_Wm4j-7TeV-HTp_bornLO_central-mu_rand-101-3999.dat' % (fullpath)
	SherpaAnalysisFile='%s/data/%s' % (fullpath,analysisFile)
	infos = parseAnalysisFile(SherpaAnalysisFile)
	print len(infos)
	for info in infos:
		info['roundedPtCut'] = string.split(str(info['ptcut']),'.')[0]
		info['workingPath'] = workingPath
		info['studyName'] = studyName
		extractAllPlots(info)
	

if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-n", "--nohist", action='store_false',dest="nohist",help="don't read histograms into root files")
	parser.add_option("-p", "--process",dest="process", default='W4',help="specify the process")

	(options, args) = parser.parse_args()

	histogramMode=options.process
	if options.nohist:  histogramMode='None' 
	
	
	
	if len(args) == 2:
		print analyseAll(args[0],args[1])
	else:
		print "Usage: FernandoComparison DIR ANALYSIS_FILE"
