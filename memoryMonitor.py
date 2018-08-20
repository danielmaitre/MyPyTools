import time
import os
import errno


_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(PID,VmKey):
    _proc_status = '/proc/%d/status' % PID
    '''Private.
    '''

    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(PID,since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB(PID,'VmSize:') - since


def resident(PID,since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB(PID,'VmRSS:') - since


def stacksize(PID,since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB(PID,'VmStk:') - since



def is_running(pid):        
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
    return True

import string
def filtered_string(s):
    return filter(lambda x: x in string.printable, s)



def get_process(cmd):
    pids = []
    processes = []
    for i in os.listdir('/proc'):
        if i.isdigit():
            pids.append(i)

    for pid in pids:
        proc = open(os.path.join('/proc', pid, 'cmdline'), 'r').readline()
        if proc:
            cmd0=filtered_string(proc.split('\x00')[0])
            if cmd0 == cmd:
                processes.append(int(pid))
#            else:
#                print "%s: '%s'!='%s'" % (pid, repr(cmd0),repr(cmd))
            
    return processes          

def is_running(pid):
    return os.path.exists("/proc/%s" % str(pid))

sizes=[(1024**3,'GB'),(1024**2,'MB'),(1024,'KB')]

def    prettyPrint(m):
    for s,n in sizes:
        if m > s:
            return "%.2f %s" % (m/s,n)
    return "%s" % s


if __name__=="__main__":

    import sys
    if len(sys.argv)!=3:
        print "usage: memoryMonitor PROGRAM SECONDSTOWAIT"
        sys.exit(1)
    prog=sys.argv[1]
    time.sleep(int(sys.argv[2]))

    pids=get_process(prog)

    running=pids

    max=dict([(ppiidd,0) for ppiidd in pids ])

    while running:
        for PID in pids:
            mem=memory(PID)
            if mem>max[PID]:
                max[PID]=mem
                print "%s [%s]: %s" % (prog,PID,prettyPrint(mem))
        time.sleep(int(sys.argv[2]))
        running=[p for p in running if is_running(p)]
    
    
