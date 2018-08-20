import sys
import NtuplesAnalysis
import math


def getMom(Ev,i):
    return (
        NtuplesAnalysis.floatArray_getitem(Ev.E,i),
        NtuplesAnalysis.floatArray_getitem(Ev.px,i),
        NtuplesAnalysis.floatArray_getitem(Ev.py,i),
        NtuplesAnalysis.floatArray_getitem(Ev.pz,i)
        )

def printPtEtaYPhi(Ev,i):
	e = NtuplesAnalysis.floatArray_getitem(Ev.E, i)
	x = NtuplesAnalysis.floatArray_getitem(Ev.px, i)
	y = NtuplesAnalysis.floatArray_getitem(Ev.py, i)
	z = NtuplesAnalysis.floatArray_getitem(Ev.pz, i)    
	Y = 0.5 * math.log((e + z) / (e - z))
	p = math.sqrt(x * x + y * y + z * z)
	eta = 0.5*math.log((p + z) / (p - z))
	pt = math.sqrt(x*x+y*y)
	if x == 0:
		if y > 0 :
			phi = math.pi / 2 
		else:
			phi = -math.pi / 2
	else:
		if y > 0 :
			phi = math.atan(y / x) 
		else:
	 		phi = math.pi + math.atan(y / x)

	print "eta: ",eta  
	print "y: ",Y  
	print "phi: ",phi  
	print "pt: " , pt
 	 	      


def prepareAnalysis(analysisFileName,rootFileName='',iEntry=1,treeName='t3'):
	PD = NtuplesAnalysis.ProcessDescription()
	NtuplesAnalysis.getProcessDescriptionFromFile(analysisFileName,PD)

	print list(PD.particleNames)
	Ev = NtuplesAnalysis.Event(PD)


	PDFR=NtuplesAnalysis.PDFReader()
	PDFR.readFromFile(analysisFileName)
	PDFR.init()
	if rootFileName!='':
		runInfo = NtuplesAnalysis.runInfoStruct() 
	 	runInfo.filename = rootFileName
                NtuplesAnalysis.setDefaults(runInfo)
		RR = NtuplesAnalysis.RootFileReader(runInfo,Ev,treeName)
		for i in range(0,iEntry):
			RR.readNext(Ev)
	else:
		RR=None
	return PD,Ev,RR,PDFR



def applyJetAlgo(Ev,nmin,nmax,etamax,ymax=1000,ptcut=0,etcut=0,algo='AntiKt',radius=0.4,overlapThreshold=0.75,IsolationIndex=-1,IsolationRadius=0.0):

	jcs = NtuplesAnalysis.JetCutSpecification(nmin, nmax, etamax, ymax, ptcut, etcut,nmax)

	AK = {
        'AntiKt': NtuplesAnalysis.AntiKtJetAlgo(radius),
        'Kt': NtuplesAnalysis.KtJetAlgo(radius),
        'Siscone': NtuplesAnalysis.SisconeJetAlgo(radius, overlapThreshold)
        }[algo]
	AK.fill(Ev.preliminaryJets,Ev, Ev)
	hasRightNumberOfJets = Ev.applyJetCut(jcs)
# if this fails, we still want to populate the jets and have the number of jets set	
	if not hasRightNumberOfJets:
		Ev.findJets(AK, etamax, ptcut, etcut)

