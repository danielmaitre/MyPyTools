import sys
import shlex
import subprocess
import tempfile

if len(sys.argv)!= 2 :
    print 'usage: M4kePlots inputFile'
    sys.exit(1)
fileName=sys.argv[1]

Cmd='m4 '+fileName
args=shlex.split(Cmd)


p=subprocess.Popen(args, stdout=subprocess.PIPE)

text= p.stdout.read()
tmpName='_tmp_m4kePlots.dat'
tmpfile = open(tmpName,'w')

tmpfile.write(text)


makePlotCmd='makePlot  %s ' % tmpName

args=shlex.split(makePlotCmd)

p=subprocess.Popen(args, stdout=subprocess.PIPE)


print 'Plots created.'
sys.exit(0)

