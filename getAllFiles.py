import sys
import castorTools as CT
import time

def getAllFiles(PROCESS,PART,allFiles):
	#print 'Process %s part: %s files: %s' % (PROCESS, PART, FILES)
	FILES = list(allFiles)

	copiedFiles=[]
	
	maxround = 24
	
	for round in range(1,maxround+1) :
	    if not FILES and len(sys.argv)!=3:
	        #no files to process
	        print 'All files successfully copied!'
	        return 0
	    print 'Round %s' % round
	    res=CT.GetAllFiles(PROCESS, PART, FILES,'COPY',dest='.')
	    for f in res.get('copied',[]):
	        FILES.remove(f)
	        copiedFiles.append(f)
	
	    if len(res['stagein'])>0:
	        print '%d file still stageing in...' % len(res['stagein'])
	        print 'Waiting 5 minutes'
	        time.sleep(5*60)
	
	
	if len(copiedFiles ) == len(allFiles):
	    return 0
	else:
	    return 1
	
	

if __name__ == "__main__":
	if len(sys.argv)<3:
	    print 'Usage: GetAllFiles PROCESS PART FILES'
	    sys.exit(1)
	    
	PROCESS = sys.argv[1]
	PART = sys.argv[2]
	allFiles = list(sys.argv[3:])
	
	sys.exit(getAllFiles(PROCESS,PART,allFiles))
	
	