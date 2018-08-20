import datetime
import os
import re
import stat
import shlex, subprocess
import sys
import time
import itertools
import operator
genInfoRegex = re.compile(r'--process=(?P<process>.*?)\s+--analysis=(?P<analysis>.*?)\s+')
genInfoFile = open('gen_analysis.log')
match= genInfoRegex.search(genInfoFile.read())

if match:
    PROCESS=match.group('process')
    ANALYSIS_NAME=match.group('analysis')
else:
    print 'Could not find process and analysis info.'
    sys.exit(1)


ANALYSIS_DIR='/afs/cern.ch/user/d/dmaitre/NtuplesAnalysis/analysis_%s_%s' % (PROCESS,ANALYSIS_NAME)
ANALYSIS_DIR='/u/home/bern/maitreda/Analysis/analysis_%s_%s' % (PROCESS,ANALYSIS_NAME)
SCRIPT = '%s/analysisJobPart.sh' % ANALYSIS_DIR

doSubmit = False
ignoreRunning = False


def prettyPrint(l):
    s=[ (e.split('_')[1].split('.')[0] ,e.split('_')[-1]) for e in l]
    dd={}
    for suffix,index in s:
        if not dd.get(suffix,None):
            dd[suffix]=[]
        dd[suffix].append(int(index))
    txt=[]
    for suffix in dd.keys():
        indices=[]
        idata=[int(ind) for ind in dd[suffix]]
        if len(idata)==1:
            for ind in dd[suffix]:
                txt.append('%s_%s' % (suffix,ind) )
        else:
            ranges=[]
            for k, g in itertools.groupby(enumerate(idata), lambda (i,x):i-x):
                ranges.append(map(operator.itemgetter(1), g))
            for r in ranges:
                first,last=r[0],r[-1]
                if first==last:
                    indices.append('%s' % (first) )
                else:
                    indices.append('%s-%s' % (first,last) )
            txt.append('%s_{%s}' % (suffix,','.join(indices)) )
    return txt



def submitLFS(part,npart,queue='1nw'):
    ARGS="%s_%s NOT_USED %s NOT_USED_EITHER %s %s  %s " % (PROCESS,part,ANALYSIS_NAME,npart,ANALYSIS_DIR,part)
    cmd='bsub -R "pool>30000" -q %s -J %s_%s_%s_%s %s %s' %(queue,PROCESS,ANALYSIS_NAME,part,npart,SCRIPT,ARGS)
#    print cmd
    args = shlex.split(cmd)
#    print args
    p = subprocess.Popen(args)
    return p.wait()

walltimes={'qmedium':"-l h_data=4096M,h_rt=24:00:00",
           'qbatch':"1:59:59",
           'qlong':"240:00:00"
}


def submitQsub(part,npart,queue='qmedium'):
    #print 'arguments for submit %s:' % str( (part,npart,queue) )
    CMD="--local \
--analysis-file=%(ANALYSIS_DIR)s/analysis_%(part)s_split.dat \
--file-list=%(ANALYSIS_DIR)s/%(part)s_parts/split_%(part)s_%(npart)s \
--npart=%(npart)s --part=%(part)s \
--dataRoot=/u/home/bern/maitreda/NtuplesData/ \
--process=%(PROCESS)s \
--analysis-dir=%(ANALYSIS_DIR)s " % { 'ANALYSIS_DIR':ANALYSIS_DIR,'PROCESS': PROCESS,'part':part,'npart':npart}

    #print CMD
    
    jobName="%s_%s_%s_%s" % (PROCESS,ANALYSIS_NAME,part,npart)
    script=open('script_%s.sh' % jobName ,'w')

    script.write("#PBS -N %s \n" % jobName)
    script.write("#PBS -q %s\n"  % queue)
    script.write("python %s/analysisJobPart.py %s " % (ANALYSIS_DIR,CMD) )

    script.close()

    cmd='qsub %s script_%s.sh' % (walltimes.get(queue,''),jobName)
    #print cmd
    args = shlex.split(cmd)
    #print args
    p = subprocess.Popen(args)
    return p.wait()


import random
import string

uuid=''.join(random.choice(string.ascii_uppercase) for x in range(15))
delegateProxyDone=False

def submitGrid(part,npart,removeOld):
    global delegateProxyDone
    if not delegateProxyDone:  
        cmd='glite-wms-job-delegate-proxy -d %s' % uuid 
        p = subprocess.Popen(cmd,shell=True)
        p.wait()
        delegateProxyDone=True

    jdlName="analysis_%s_%s.jdl" % (part,npart)
    jidName="analysis_%s_%s.jid" % (part,npart)

    if removeOld:
        cmd='lcg-del -a lfn:/grid/pheno/daniel/BHS_ntuples/%s_%s/%s/histograms_%s.root_%s' % (PROCESS,part,ANALYSIS_NAME,part,npart) 
        print 'removing old histogram file...'
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)

    cmd='glite-wms-job-submit  -d %s -o %s %s' % (uuid,jidName,jdlName)
    print cmd
    p = subprocess.Popen(cmd,shell=True,cwd='./%s_parts'%part)
    return p.wait()

def submit(part,npart,removeOld=False):
    submitGrid(part,npart,removeOld)


def getRunStatusGrid(part,npart):
    jidName="analysis_%s_%s.jid" % (part,npart)
    if not os.path.isfile('%s_parts/%s' % (part,jidName)):
        #print 'file: %s ' % ('%s_parts/%s' % (part,jidName))
        return 'NeverSubmitted'
    cmd='glite-wms-job-status `tail -n1 %s_parts/%s`' % (part,jidName)
    #print cmd
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    runningRegex=re.compile(r'.*Running.*')
    waitingRegex=re.compile(r'.*Waiting.*')
    waitingRegex=re.compile(r'.*Ready.*')
    waitingRegex=re.compile(r'.*Submitted.*')
    Regex=re.compile(r'.*Scheduled.*')
    states=['Submitted','Waiting','Ready','Scheduled','Running','Done','Cleared']
    regexes=[(s,re.compile(r'.*%s.*'% s)) for s in states]
    for line in p.stdout:
        for s,r in regexes:
            if r.match(line):
                return s
    return 'Other'




def getRunStatusLFS():
    jobRegex=re.compile(r'Job <(?P<JobID>\d+)>,\s+Job Name <(?P<name>\w+)>')
    cmd='bjobs -l ' 
#    print cmd
    args = shlex.split(cmd)
    #print args
    jobIDs={}
    p = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in p.stdout:
        match= jobRegex.match(line)
        if match:
            jobIDs[match.group('name')]=match.group('JobID')
    return jobIDs        

def getRunStatus():
    
    jobRegex2=re.compile(r'job_name:\s+script_(?P<name>.*).sh')
    cmd="qstat -u maitreda | grep maitreda | cut -d ' ' -f1" 
    #print cmd
    args = shlex.split(cmd)
    #print args
    jobIDs={}
    jobids=[]
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    for line in p.stdout:
        jobID=int(line)
        jobids.append(str(jobID))

    for j in jobids:
        cmd='qstat -j %s -f | grep job_name' %j 
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        for line in p.stdout:
            match=jobRegex2.match(line)
            if match:
                jobIDs[match.group('name')]=j
    #print jobIDs
    return jobIDs        


def getRunStatusKelvin():
    jobRegex1=re.compile(r'Job Id: (?P<JobID>\d+)\.master0.alineos.net')
    jobRegex2=re.compile(r'\s+Job_Name = (?P<name>.*)')
    cmd='qstat -f' 
#    print cmd
    args = shlex.split(cmd)
    #print args
    jobIDs={}
    p = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in p.stdout:
        match= jobRegex1.match(line)
        if match:
            #print line
            line2=p.stdout.next()
            #print line2
            match2= jobRegex2.match(line2)
            if match2:
                #print 'match'
                jobIDs[match2.group('name')]=match.group('JobID')
    #print jobIDs
    return jobIDs        


def getHistogramFilesGrid(suffix):
    gridHistogramFiles={}
    cmd='lfc-ls -l /grid/pheno/daniel/BHS_ntuples/%s_%s/%s/' % (PROCESS,suffix,ANALYSIS_NAME) 
    #print cmd
    args = shlex.split(cmd)

    p = subprocess.Popen(args,stdout=subprocess.PIPE)
    patt=re.compile('[rw-]+\s+\d\s+\d+\s+\d+\s+(?P<size>\d+)\s+(?P<date>\w+\s+\d+\s+\d+:\d\d)\s+(?P<filename>[\w-]+.root_\d+)')
    for line in p.stdout:
        #print line
        match=patt.match(line)
        if match:
            #print 'match!'
            date_string=match.group('date')+ ' 2013'
            dt=datetime.datetime(*(time.strptime(date_string,'%b %d %H:%M %Y')[0:6]))
            gridHistogramFiles[match.group('filename')]=dt
    return gridHistogramFiles

def getHistogramFilesLocal(suffix):
    HistogramFiles={}
    cmd='ls -l histograms_%s.root_* 2> /dev/null ' % suffix 
    #print cmd
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    patt=re.compile('[rw-]+\s+\d\s+(?P<user>\w+)\s+(?P<group>\w+)\s+(?P<size>\d+)\s+(?P<date>\w+\s+\d+\s+\d+:\d\d)\s+(?P<filename>[\w-]+.root_\d+)')
    for line in p.stdout:
        #print line
        match=patt.match(line)
        if match:
            #print 'match!'
            date_string=match.group('date')+ ' 2013'
            dt=datetime.datetime(*(time.strptime(date_string,'%b %d %H:%M %Y')[0:6]))
            HistogramFiles[match.group('filename')]=dt
        else:
            #print 'no match for %s' % line
            pass

    return HistogramFiles




def main(part=None):
    allFiles=os.listdir('.')

    histogramRegex = re.compile('histograms_(?P<part>.*)\.root_(?P<npart>\d+)')

    histFiles = filter(lambda x: histogramRegex.match(x),allFiles)

    partDirRegex = re.compile('(?P<part>.*?)_parts')
    partDirs = filter(lambda x: partDirRegex.match(x),allFiles)

    if part:
        print 'Only one part: %s' %part
        suffixes = [ part ]
    else:
        suffixes = [ partDirRegex.match(part).group('part') for part in partDirs ]

    print 'Suffixes: '+' '.join(suffixes)

    notThere=[]
    olderFiles=[]
    olderFilesOnGrid=[]
    newerFilesOnGrid=[]
    zeroSize=[]
    running=[]
    jobs=getRunStatus()
    runningPrecise={}
    for suffix in suffixes:
        try:
            mode_ref_suffix=os.stat('LFS_Start_'+suffix)
            ref_dt=datetime.datetime.fromtimestamp(os.path.getmtime('LFS_Start_'+suffix))
        except:
            print 'No stat info for %s' % suffix
            continue
        jdlRegex = re.compile('analysis_'+suffix+'_(?P<npart>.*)\.jdl')
        jdlFiles=os.listdir(suffix+'_parts')
        #print "jdlFiles",jdlFiles
        jf = filter(lambda x: jdlRegex.match(x),jdlFiles)

        #print "jf",jf
        gridHistogramFiles=getHistogramFilesGrid(suffix)
        #print gridHistogramFiles
        localHistogramFiles=getHistogramFilesLocal(suffix)
        #print localHistogramFiles

        #sys.exit(1)

        for f in jf:
            npart = jdlRegex.match(f).group('npart')
            #print ' - - - - %s' % npart
            histFile='histograms_%s.root_%s' % (suffix,npart)
            jobName='%s_%s_%s_%s' % (PROCESS,ANALYSIS_NAME,suffix,npart)
            state='undecided'
            submitThis=False
            isRunning=False    
            if histFile in localHistogramFiles:
                if localHistogramFiles[histFile] > ref_dt :
                    #print 'ref: %s, onGrid: %s' % (ref_dt,localHistogramFiles[histFile])
                    pass
                    #print f,' newer'
                else :
                    #print f,' older'
                    #print 'ref: %s, onGrid: %s' % (ref_dt,gridHistogramFiles[histFile]) 
                    olderFiles.append(histFile)
                    submitThis=True
                #print mode[stat.ST_SIZE]        
                mode=os.stat(histFile)
                if mode[stat.ST_SIZE] == 0 :
                    #print f,' zero size'
                    zeroSize.append(histFile)
                    submitThis=True
            # no point looking on the grid if a local file is already here           
            else : # that means no histogram files in the directory 
                submitThis=True
                # unless it is on the gid, which we check now...
                
            if submitThis and histFile in gridHistogramFiles:
                if gridHistogramFiles[histFile] > ref_dt :
                    #print f,' newer on grid'
                    #print 'ref: %s, onGrid: %s' % (ref_dt,gridHistogramFiles[histFile]) 
                    newerFilesOnGrid.append(histFile)
                    if histFile in olderFiles:
                        olderFiles.remove(histFile)
                    if histFile in notThere:
                        notThere.remove(histFile)
                    submitThis=False
                    pass
                else :
                    #print f,' older'
                    olderFilesOnGrid.append(histFile)
                    submitThis=True
            if histFile not in gridHistogramFiles and histFile not in localHistogramFiles and histFile not in newerFilesOnGrid :
                #print f,' not there'
                notThere.append(histFile)
                submitThis=True

            if submitThis: # something is not right, so want to see if job is running
                state=getRunStatusGrid(suffix,npart)
                #print 'state for %s : %s' % (histFile,state)
                if state in ['Running','Submitted','Ready','Waiting','Scheduled']:
                    thelist=runningPrecise.get(state,None)
                    if not thelist:
                        runningPrecise[state]=[]
                        thelist=runningPrecise.get(state)
                    thelist.append('%s_%s' % (suffix,npart))
                    running.append(histFile)
                    isRunning=True
                
            if submitThis and doSubmit and ( ignoreRunning or not isRunning  ):
                if not ignoreRunning: # no point checking status if it is ignored
                    state=getRunStatusGrid(part,npart)
                    if state in ['Running','Submitted','Ready','Waiting','Scheduled']:
                        isRunning=True
                    else:
                        isRunning=False
                if ignoreRunning or not isRunning:
                    if histFile in olderFilesOnGrid:
                        submit(suffix,npart,removeOld=True)
                    else:
                        submit(suffix,npart,removeOld=False)


    if not doSubmit:
        if notThere or olderFiles or zeroSize or running or olderFilesOnGrid :
            if not ignoreRunning:
                print 'older files: ',prettyPrint([f for f in olderFiles if not f in running ])
                print 'missing files: ', prettyPrint([ f for f in notThere if not f in running])
                print 'zero size: ',prettyPrint([ f for f in zeroSize if not f in running] )
                print 'old on grid: ',prettyPrint([ f for f in olderFilesOnGrid if not f in running] )
                print 'still running: ',prettyPrint([ f.split('_')[1].split('.')[0] + '_'+ f.split('_')[-1] for f in running ])
                for st in runningPrecise.keys():
                    print 'still running (%s): %s' % (st,prettyPrint(runningPrecise[st]))
                print '\nNot all files are finished/done. Run with --submit to submit the missing/failed files.'
            else:
                print 'older files: ',prettyPrint([f for f in olderFiles  ])
                print 'missing files: ', prettyPrint([ f for f in notThere ])
                print 'zero size: ',prettyPrint([ f for f in zeroSize ] )
                print 'still running (allegedly): ',prettyPrint([ f.split('_')[1].split('.')[0] + '_'+ f.split('_')[-1] for f in running ])
                print '\nNot all files are finished/done. Run with --submit to submit the missing/failed files.'

        elif newerFilesOnGrid :
            print 'Newer files on the grid, collect them.'
            print newerFilesOnGrid
        else :
            print 'All files OK'



if __name__ == '__main__':
    import getopt
    opts, extraparams = getopt.getopt(sys.argv[1:],'sp:i',['submit','part=','ignore-running']) 
    #print opts
    part=None
    for o,a in opts:
        if o in ('-s','--submit'):
            doSubmit = True
        if o in ('-p','--part'):
            part=a
        if o in ('-i','--ignore-running'):
            ignoreRunning=True
    main(part)
        

