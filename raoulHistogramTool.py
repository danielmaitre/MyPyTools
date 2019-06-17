import sys
import re

def getHist(filename, obs):
    f=open(filename,'r')
    lines=f.readlines()
    #print lines
    regex = 'Obs={}'.format(obs)

    beginIndex = [ ind for ind,l in enumerate(lines) if regex in l]
    
    #print beginIndex
    bi = beginIndex[0]
    endIndex = [ ind for ind,l in enumerate(lines[bi+1:]) if '-----' in l]
    #print endIndex
    ei = bi+endIndex[0]
    hlines = lines[bi+3:ei+1]
    #print ''.join(hlines)


    bb = [ float(l.split()[2]) for l in hlines ]
    val = [ float(l.split()[3]) for l in hlines ]
    err = [ float(l.split()[4]) for l in hlines ]
    #print bb, val, err

    return bb, val, err



if __name__ == '__main__':
    filename = sys.argv[1]
    obs = sys.argv[2]
    getHist(filename, obs)
