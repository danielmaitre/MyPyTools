import os
import subprocess
import shlex
import re
import time
import sys

validResponseRegex = re.compile(r'(?:Received 1 responses\n)?/castor/.*?\s.*?\s(?P<state>\w*)')

def isLXPLUS():
    import socket
    hostname=socket.gethostname()
    lxplus=re.compile(r'lxplus(\d+).cern.ch')
    if lxplus.match(hostname):
        return True
    else:
        return False
def forceLXPLUS():
    if not isLXPLUS():        
        print 'You are not on lxplus! '
        sys.exit(1)

def getStagerStatus(file):
    cmd='stager_qry -M %s' % file
    args=shlex.split(cmd)
    p=subprocess.Popen(args,stdout=subprocess.PIPE)
    answer =  p.stdout.read()
    match = validResponseRegex.match(answer)
    if match:
        return match.group('state')
    else :
        print 'Invalid answer: "%s"' % answer
        return None

def stagerGetFile(file):
    cmd='stager_get -M %s' % file
    args=shlex.split(cmd)
    p=subprocess.Popen(args,stdout=subprocess.PIPE)
    answer =  p.stdout.read()
    return answer

goodCopyAnswer=re.compile(r'(?P<in>\d+) bytes in \d+ seconds .*?(?P<out>\d+) bytes in remote file',re.DOTALL)

def getCastorFile(filename,dest='.'):
    cmd='rfcp %s %s' % (filename, dest)
    #print cmd
    args=shlex.split(cmd)
    p=subprocess.Popen(args,stdout=subprocess.PIPE)
    answer =  p.stdout.read()
    match = goodCopyAnswer.match(answer)
    if match:
        return match.group('in') == match.group('out') 
    else:
        print answer
        return False

def IsStaged(file):
    if getStagerStatus(file)=='STAGED':
        return True
    else :
        return False

file = '/castor/cern.ch/user/d/dmaitre/Wp1j7TeV/loop/output_3364_23193.root'

rfdirOutputLineRegex = re.compile(r'[-rw]+\s+\d+\s+(?P<user>\w+)\s+(?P<group>\w+)\s+(?P<size>\d+)\s+(?P<month>\w+)\s+(?P<day>\d+)\s+((?P<hour>\d\d:\d\d)|(?P<year>\d\d\d\d))\s+(?P<name>[\w\.-]+)')

def getFileList(path,info=['name']):
    cmd='rfdir %s' % path
    args=shlex.split(cmd)
    p=subprocess.Popen(args,stdout=subprocess.PIPE)
    answer =  p.stdout.read()
    allFiles=[]
    for line in answer.splitlines():
        match = rfdirOutputLineRegex.match(line)
        if match:
            if len(info)==1:
                allFiles.append( match.group(info[0]))
            else:
                allFiles.append( [match.group(i) for i in info ] )
        else :
            print 'Invalid line in rfdir output: %s' % line
    return allFiles



def allFilesStaged(process,part,fileList=[]):
    dir='/castor/cern.ch/user/d/dmaitre/%s/%s/' % ( process, part)
    if not fileList:
        #print dir
        fs=getFileList(dir)
    else:
        fs=fileList
    status = [ getStagerStatus(dir+'/'+f) for f in fs ]
    if set(status)==set(['STAGED']):
        return True,[]
    else :
        failed = [ z for z in zip(fs,status) if not z[1]=='STAGED' ]
        return False,failed
    
def getNpoints(filename):
    fname='castor:/castor/cern.ch/user/d/dmaitre/%s' % filename
    import ROOT
    cf=ROOT.TCastorFile(fname)
    t=cf.Get("t3")
    return t.GetEntries() 

def getCastrorFileInfo(filename):
    if filename[0]=='/':
        fname='castor:%s' % filename
    else:
        fname='castor:/castor/cern.ch/user/d/dmaitre/%s' % filename
    import ROOT
    cf=ROOT.TCastorFile(fname)
    infos=list()
    n=0
    l=cf.GetListOfKeys()
    for k in l:
        if k.GetClassName() == 'InfoFile':
            infos.append(k.GetName())       
        if k.GetName() == 't3':
            t=cf.Get("t3")
            n=t.GetEntries()

    return n,infos        

def testDirectory(directory):
    if directory[0] != '/':
        dirname='/castor/cern.ch/user/d/dmaitre/%s' % directory
    else:
        dirname=directory
        

    fs=getFileList(dirname)
    infos=list()
    empty=list()
    noInfo=list()
    for f in fs:
        info=getCastrorFileInfo('%s/%s' % (dirname,f))
        if info[0] == 0:
            empty.append(f)
        if not info[1]:
            noInfo.append(f)
        infos.append(info)    

    if empty:
        print 'empty files: %s' % empty
    if noInfo:
        print 'files without info: %s' % noInfo
    s=sum([ x[0] for x in infos]  )
    print 'Total number of PS points: %s' % s









def GetAllFiles(PROCESS, PART, FILELIST=[],action='STAGE',dest='/tmp/dmaitre/'):
    """
    With action='STAGE' requests all FILES to be staged. If no FILES are given,
    all files will be staged.
    With action='COPY' all FILES will be copied. FILES not present will be
    requested, but not copied. Check the size of res['notThere'] or
    res['copied'] to make sure all files have been copied. 
    """
    dir='/castor/cern.ch/user/d/dmaitre/%s/%s/' % ( PROCESS, PART)
    if not FILELIST:
        #print dir
        FILES=getFileList(dir)
    else:
        FILES=FILELIST
    success,failed = allFilesStaged(PROCESS, PART, FILES)
    failedFiles=[f[0] for f in failed]
    successFiles=[f for f in FILES if f not in failedFiles ]
    stageinFiles=[f for f,status in failed if status=='STAGEIN']
    notThere=[ f for f in failedFiles if f not in stageinFiles ]


    #first request the missing files to be staged:

    res={}
    res['notThere']=notThere
    res['stagein']=stageinFiles
    res['staged']=successFiles
    for f in notThere:
        print 'Requesting: %s' % f
        filename='/castor/cern.ch/user/d/dmaitre/%s/%s/%s' % ( PROCESS, PART, f)
        stagerGetFile(filename)
        

    #get the files that are staged:

    if action=='COPY':
        copiedFiles=[]
        for f in successFiles:
            print 'getting file %s' % f 
            filename='/castor/cern.ch/user/d/dmaitre/%s/%s/%s' % ( PROCESS, PART, f)
            copySuccessful=getCastorFile(filename,dest)
            if copySuccessful:
                copiedFiles.append(f)
                print 'Sucessful copy of %s' % f
        res['copied']=copiedFiles

    return res

def stageAll(PROCESS, PART):
    forceLXPLUS()
    for i in range(1,36):
        res=GetAllFiles(PROCESS, PART, FILELIST=[],action='STAGE')

        if len(res['stagein']) > 0 or len(res['notThere']) > 0:
            print 'Files to be staged: %i   stagein: %i' % (len(res['notThere']),len(res['stagein']))
            print 'Waiting 5 minutes for stager...'
            sys.stdout.flush()
            time.sleep(5*60)
            continue
        else:
            print 'All files staged!'
            return True

    return False
