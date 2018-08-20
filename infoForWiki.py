#need to do :
#   sshfs daniel@ui.phyip3.dur.ac.uk:/mt/data-grid/daniel $HOME/ui

import Location
location=Location.whereAmI()
import sys

if location=='HOFFMAN2' or location=='HOFFMAN2_NTUPLES':
    sys.path.append('/u/home/bern/maitreda/NtuplesAnalysis/scripts/')
else:
    sys.path.append('/u/home/bern/maitreda/workspace/NtuplesAnalysis/scripts/')


import getNtupleInfo as gni

def printInfo(process,part,location='CERN',energy='',pattern=None,files=[],out=sys.stdout,dropAnomalous=True):
    res=gni.getInfo(process,part,location,energy=energy,pattern=pattern,output=out,dropAnomalous=dropAnomalous)
    res['part']=part
    #print res
    eventsPerFile=gni.getEventNumberList(process,part,location,energy=energy,files=files,output=out)
    #print eventsPerFile
    if len(eventsPerFile.keys())==1:
        for epf,number in eventsPerFile.items():
            if epf !=0 :
                res['eventsPerFile']=gni.humanReadable(epf)
                res['totalEvents']=gni.humanReadable(epf*number)
                res['diskPerMevent']=gni.humanReadable(int(1000000*res['averageSize']/epf))
                out.write("|| %(part)s || %(nbrFiles)s || %(eventsPerFile)s || %(totalEvents)s || %(averageSizeHR)s || %(diskPerMevent)s || %(totalSize)s ||\n" % res)
            else:
                out.write( "|| %(part)s || %(nbrFiles)s || 0 || 0 || 0 || N/A || 0 ||\n" % res)

    else:
        totevents=0
        for epf,number in eventsPerFile.items():
            if epf !=0 :
                res['eventsPerFile']=gni.humanReadable(epf)
                totevents=totevents+epf*number
                res['totalEvents']=gni.humanReadable(epf*number)
                res['diskPerMevent']=gni.humanReadable(int(1000000*res['averageSize']/epf))
                res['n']=number
            #print res
                out.write("|| %(part)s || %(n)s || %(eventsPerFile)s || %(totalEvents)s || --- || --- || --- ||\n" % res)
            else:
                out.write( "|| %(part)s || %(nbrFiles)s || 0 || 0 || 0 || N/A || 0 ||\n" % res)
        res['totalEvents']=gni.humanReadable(totevents)
        out.write("|| %(part)s (tot) || %(nbrFiles)s || --- || %(totalEvents)s || %(averageSizeHR)s || %(diskPerMevent)s || %(totalSize)s ||\n" % res)


normalNoLO=['born','loop','vsub','real']
normal=['born','bornLO','loop','vsub','real']
lcfmlc=['born','bornLO','loop-lc','loop-fmlc','vsub','real']
lcfmlcNoLO=['born','loop-lc','loop-fmlc','vsub','real']
lcNoLO=['born','loop-lc','vsub','real']
lconly=['born','bornLO','loop-lc','loop-fmlc','vsub','real']

z1=['born','bornLO','loop-2q-qq','loop-2q-qg','real-2q-qg','real-4q-qq','real-2q-gg','real-2q-qq','vsub-qg','vsub-qq']

z2=['born', 'bornLO', 'loop-2q-gg', 'loop-2q-qg', 'loop-2q-qq', 'loop-4q-qq', 'real-2q-gg', 'real-2q-qg', 'real-2q-qq', 'real-4q-qg', 'real-4q-qq', 'vsub-gg', 'vsub-qg','vsub-qq']

z3=['born', 'bornLO', 'loop-lc-2q-gg', 'loop-lc-2q-qg', 'loop-lc-2q-qq',
 'loop-lc-4q-qg', 'loop-lc-4q-qq', 'real-BH-2q-gg', 'real-BH-2q-qg', 'real-BH-2q-qq',
 'real-BH-4q-gg', 'real-BH-4q-qg', 'real-BH-4q-qq', 'real-BH-6q-qq', 'vsub-gg', 'vsub-qg',
 'vsub-qq']

z4=['born', 'bornLO', 'loop-lc-2q-gg', 'loop-lc-2q-qg', 'loop-lc-2q-qq', 'loop-lc-4q-gg',
    'loop-lc-4q-qg', 'loop-lc-4q-qq', 'real-BH-2q-gg', 'real-BH-2q-qg', 'real-BH-2q-qq',
    'real-BH-4q-gg', 'real-BH-4q-qg', 'real-BH-4q-qq',  'vsub-gg', 'vsub-qg', 'vsub-qq'] 

w4 = ['born'
'loop-lc',
'real-2q',
'real-4q',
'real-6q',
'vsub-gg',
'vsub-qg',
'vsub-qq'
]

partsCERN={
    'Wm1j7TeV':normal,
    'Wp1j7TeV':normal,
    'Wm2j7TeV':normal,
    'Wp2j7TeV':normal,
    'Wm3j7TeV':lcfmlc,
    'Wp3j7TeV':lcfmlc,
    'Wm4j7TeV':w4,
    'Wp4j7TeV':w4,
    }

partsKelvin={
    'Zee1j7TeV':z1,
    'Zee2j7TeV':z2,
    'Zee1j7TeV_HS':normal,
    'Zee2j7TeV_HS':normal,
    'Zee3j7TeV':z3,
    'Zee4j7TeV':z4
    }

partsHoffman2={
'PureQCD2Jet':normalNoLO,
'PureQCD3Jet':normalNoLO,
'PureQCD4Jet':normalNoLO,
'PureQCD2Jet_ATLAS':normalNoLO,
'PureQCD3Jet_ATLAS':normalNoLO,
'PureQCD4Jet_ATLAS':normalNoLO,
'PureQCD2Jet_ATLAS40':normalNoLO,
'PureQCD3Jet_ATLAS40':normalNoLO,
'PureQCD4Jet_ATLAS40':normalNoLO,


'Wm1j7TeV':normalNoLO,
'Wm2j7TeV':normalNoLO,
'Wm3j7TeV':lcfmlcNoLO,
'Wm4j7TeV':lcNoLO,

'Wp1j7TeV':normalNoLO,
'Wp2j7TeV':normalNoLO,
'Wp3j7TeV':lcfmlcNoLO,
'Wp4j7TeV':['born','loop-lc','real-2q-gg','real-2q-qg','real-2q-qq','real-4q','real-6q','vsub']


}

partsHoffman2={

'Wp1j7TeV':['born','loop','real','vsub'],
'Wm1j7TeV':['born','loop','real','vsub'],
'Wp2j7TeV':['born','loop','real','vsub'],
'Wm2j7TeV':['born','loop','real','vsub'],
'Wp3j7TeV':['born','loop-lc','loop-fmlc','real','vsub'],
'Wm3j7TeV':['born','loop-lc','loop-fmlc','real','vsub'],
'Wp4j7TeV':['born','loop-lc','real-2q-gg','real-2q-qg','real-2q-qq','real-4q','real-6q','vsub'],
'Wm4j7TeV':['born','loop-lc','real-2q-gg','real-2q-qg','real-2q-qq','real-4q','real-6q','vsub']


}

partsMap={
'HOFFMAN2':partsHoffman2,
'CERN': partsCERN,
'KELVIN':partsKelvin
}



parts = partsMap[location]


processFiles={
'Zee.wiki':{    'Zee1j7TeV':z1,
    'Zee2j7TeV':z2,
    'Zee1j7TeV_HS':normal,
    'Zee2j7TeV_HS':normal,
    'Zee3j7TeV':z3,
    'Zee4j7TeV':z4
}
}

if __name__ == '__main__':

    outFile=open('W.wiki','w')
    
    outFile.write('= Files on %s =' % location)

    for process in sorted(parts.keys()):
        outFile.write('\n== %s == \n\n' % process)
        info=open('%s.info' % process)
        ls= info.readlines() 
        for l in ls:
            outFile.write( '* %s' % l )
        outFile.write( '|| part || # of files || # event/file || total events || size of a file || disk/Mevent|| total disk usage||\n')
        for part in parts[process]:
            printInfo(process,part,'HOFFMAN2',out=outFile)
