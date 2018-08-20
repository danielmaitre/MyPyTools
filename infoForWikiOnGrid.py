import Location

import sys
# this needs to be mounted with 
#         sshfs daniel@login.phyip3.dur.ac.uk:/mt/home $HOME/ippp_home/

sys.path.append('/mt/home/daniel/ippp_home/daniel/workspace/NtuplesAnalysis/scripts/')
import getNtupleInfo as gni

import subprocess
def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out  #This is the stdout from the shell command


def printInfo(process,part,location,energy):
    res=gni.getInfo(process,part,location,energy=energy)
    res['part']=part
    eventsPerFile=0  #gni.getEventNumber(process,part,location)
    if eventsPerFile !=0 :
        res['eventsPerFile']=gni.humanReadable(eventsPerFile)
        res['totalEvents']=gni.humanReadable(eventsPerFile*res['nbrFiles'])
        res['diskPerMevent']=gni.humanReadable(int(1000000*res['averageSize']/eventsPerFile))
    else:
        res['eventsPerFile']='?'
        res['totalEvents']='?'
        res['diskPerMevent']='?'        
    print "|| %(part)s || %(nbrFiles)s || %(eventsPerFile)s || %(totalEvents)s || %(eventsPerFile)s || %(diskPerMevent)s || %(totalSize)s ||" % res




location=Location.whereAmI()
print '= Files on %s =' % location

processesTxt=runBash('lfc-ls /grid/pheno/BHSNtuples')
processes=processesTxt.split()
print processes



for process in processes:
    print '\n== %s == \n\n' % process
    energiesTxt=runBash('lfc-ls /grid/pheno/BHSNtuples/%(process)s' % locals())
    energies=energiesTxt.split()
    for energy in energies:
        print energy

sys.exit(0)



for process in processes:
    print '\n== %s == \n\n' % process
    energiesTxt=runBash('lfc-ls /grid/pheno/BHSNtuples/%(process)s' % locals())
    energies=energiesTxt.split()
    for energy in energies:
        print energy
        partsTxt=runBash('lfc-ls /grid/pheno/BHSNtuples/%(process)s/%(energy)s' % locals())
        parts=partsTxt.split()
        print '|| part || # of files || # event/file || total events || size of a file || disk/Mevent|| total disk usage||'
        for part in parts:
            print part
            printInfo(process,part,location,energy)




sys.exit()

for process in sorted(parts.keys()):
    print '\n== %s == \n\n' % process
    
    info=open('%s.info' % process)
    ls= info.readlines() 
    for l in ls:
        print '* %s' % l ,
    print '|| part || # of files || # event/file || total events || size of a file || disk/Mevent|| total disk usage||'
    for part in parts[process]:
        printInfo(process,part,location,energy)
