import shelve
import array
import sys
import numpy
import os


#
# this is working but the method with writing everything to the file system and
# comparing with meld is much more effective
#
def compareDicts(d1,d2):
    k1,k2=d1.keys(),d2.keys()
    if k1!=k2:
        print "Keys are not the same!"
    else :
        print "Keys are the same!"
        print "{}".format(k1)
    for k in k1:
        print k
        if hasattr(d1[k],'keys'):
            print " comparing key {0}...".format(k)
            if not compareDicts(d1[k],d2[k]):
                print "key: {0}".format(k)
                return False
        else:
            areEqual=False
            if isinstance(d1[k],array.array) or isinstance(d1[k],numpy.ndarray):
                areEqual=(d1[k]==d2[k]).all()
            else :
                areEqual= (d1[k]==d2[k])
            if areEqual:    
                print "object {0} are equal.".format(k)
                continue
            else:
                print "object {0} are NOT equal! {1} != {2} ".format(k,d1[k],d2[k])
                return False
    return True



def dumpDict(d):
    ''' dumps the content of the dictionary in the current directory
'''

    cwd=os.path.realpath(os.path.curdir)
    for k in d.keys():
        if hasattr(d[k],'keys'):
            os.mkdir(str(k))
            os.chdir(str(k))
            dumpDict(d[k])
        else:
            with open(str(k),'w') as f:
                if hasattr(d[k],"__iter__"):
                    for i in iter(d[k]):
                        f.write("{0}\n".format(i))
                else :
                    f.write(str(d[k]))
        os.chdir(cwd)

     

def dumpShelve(s,path=None):
    cwd=os.path.realpath(os.path.curdir)
    sh=shelve.open(s,'r')
    if not path:
        import tempfile
        path=tempfile.mkdtemp()
    else:
        os.mkdir(path)

    os.chdir(path)
 
    #print sh.keys()
    dumpDict(sh)

    os.chdir(cwd)
    return path

                
if __name__=="__main__" :
    s1Name=sys.argv[1]
    s2Name=sys.argv[2]

    path1=dumpShelve(s1Name)
    path2=dumpShelve(s2Name)

    
    os.system("meld -L {s1Name} {path1} -L {s2Name} {path2} 2>/dev/null".format(**locals()))
    for path in path1,path2:
        os.system("rm -r {0}".format(path))
    
    

