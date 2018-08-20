import infoForWiki as IFW
import subprocess
import HistogramTools
import ROOT
import re
import sys

def checkInfo(process,energy,parts):
    partsdict=dict()
    for part in parts:
        params={'process':process,'part':part,'energy':energy}
        localDataPath='/u/nobackup/bern/maitreda/BHSNtuples/%(process)s/%(energy)s/%(part)s/' % params
        lsCmd='ls -l %s ' % localDataPath
        p=subprocess.Popen(lsCmd, stdout=subprocess.PIPE,shell=True)
        lineRegex=re.compile(r'[lxrw-]+\s+\d+\s+(?P<user>\w+)\s+(?P<group>\w+)\s+(?P<size>\d+)\s+(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<timeoryear>(?P<time>\d+:\d+)|(?P<year>\d\d\d\d))\s+(?P<name>\S+\.root)')

        for line in p.stdout :
            match=lineRegex.match(line)
            if match:
                name=match.group('name')
                filename=localDataPath+name
                f=ROOT.TFile(filename)
                info=HistogramTools.getInfo(rootFile=f,name='Info')
                
                info=re.sub(r'NLO part.*','',info)
                if info not in partsdict:
                    partsdict[info]=dict()
                if part not in partsdict[info]:
                    partsdict[info][part]=list()
                partsdict[info][part].append(name)
                                    
    return partsdict

BIRV=['B001','I001','R001','V001']
BFIRV=['B001','I001','R001','V001','V002']
BIRVWp4j=['B001','I001','R001','R002','R003','R004','R005','V001']
BIRVZ4j=['B001','I001','I002','I003','R001','R002','R003','R004','R005','R006','V001','V002','V003','V004','V005','V006']
BIRV_YY=['B001','I001','R001','V001','V002','V003','V004']
filesToWrite={}

filesToWrite['8TeV']={
'Wp_8TeV.wiki':{
    'Wp1j':BIRV,
    'Wp2j':BIRV,
    'Wp3j':BFIRV
    },

'Wm_8TeV.wiki':{
    'Wm1j':BIRV,
    'Wm2j':BIRV,
    'Wm3j':BFIRV
    },

'Zee_8TeV.wiki':{
    'Zee1j':BIRV,
    'Zee2j':BIRV,
    'Zee3j':BFIRV
    },

'jets_8TeV.wiki':{
    '2j':BIRV,
    '3j':BIRV,
    '4j':BIRV
    }

}

filesToWrite['7TeV']={
'Wp_7TeV.wiki':{
    'Wp1j':BIRV,
    'Wp2j':BIRV,
    'Wp3j':BFIRV,
    'Wp4j':BIRVWp4j,
    },

'Wm_7TeV.wiki':{
    'Wm1j':BIRV,
    'Wm2j':BIRV,
    'Wm3j':BFIRV,
    'Wm4j':BIRV,
    },

'Zee_7TeV.wiki':{
    'Zee1j':BIRV,
    'Zee2j':BIRV,
    'Zee3j':BFIRV,
    'Zee4j':BIRVZ4j,
    },

'jets_7TeV.wiki':{
    '2j':BIRV,
    '3j':BIRV,
    '4j':BIRV
    }

}


filesToWrite={}
filesToWrite['8TeV']={
'Wp_8TeV.wiki':{
    'Wp1j':BIRV,
    'Wp2j':BIRV,
    'Wp3j':BFIRV
    }
}
filesToWrite['8TeV']={
'YY2j8TeV.wiki':{
    'YY2j':BIRV
    }
}


for energy in filesToWrite.keys():
    for f in filesToWrite[energy].keys():
        out=open(f,'w')
        for process in sorted(filesToWrite[energy][f].keys()):
            print 'Treating process %s and writing to %s'  % (process,f)
            out.write('\n== %s == \n\n' % process)
            parts=filesToWrite[energy][f]
            pp=checkInfo(process,energy,parts[process])
        #print pp

            for info in pp.keys():
                out.write(info)
                out.write( '|| part || # of files || # event/file || total events || size of a file || disk/Mevent|| total disk usage||\n')
                for part in pp[info].keys():
                    IFW.printInfo(process,part,'HOFFMAN2_NTUPLES',energy=energy,out=out,dropAnomalous=False)



