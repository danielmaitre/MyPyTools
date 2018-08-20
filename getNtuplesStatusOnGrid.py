import sys
import re
import os

def runBash(cmd):
    import subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out


def humanReadable(size):
    if size >= 1024**4:
        return '%.2fT' % (int(size)/float(1000000000000))
    if size >= 1024**3:
        return '%.2fG' % (int(size)/float(1000000000))
    if size >= 1024**2:
        return '%.2fM' % (int(size)/float(1000000))
    if size >= 1024:
        return '%.2fk' % (int(size)/float(1000))
    else:
        return '%.2f' % float(size)


directories=runBash("lfc-ls /grid/pheno/BHSNtuples").split()
for pro in directories:
    energies=runBash("lfc-ls /grid/pheno/BHSNtuples/%(pro)s" % locals()).split()
    print "===== %s ===== " % (pro)
    for e in energies:
        parts=runBash("lfc-ls /grid/pheno/BHSNtuples/%(pro)s/%(e)s" % locals()).split()
        print ":::::: %s :::::: " % (e)
        totalSize=0
        for p in parts:
            files=runBash("lfc-ls -l /grid/pheno/BHSNtuples/%(pro)s/%(e)s/%(p)s" % locals()).split('\n')
            lines=[ line.split() for line in files]
            #print lines[0]
            sizes=[int(l[4]) for l in lines ]
            tot=sum(sizes)
            totalSize+=tot
            print "    %s: %s " % (p,humanReadable(tot))
        print "total size: %s" % humanReadable(totalSize)
