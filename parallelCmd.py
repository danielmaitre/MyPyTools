#!/usr/bin/python

import Queue
import threading
import time
import subprocess



def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out  #This is the stdout from the shell command


class myThread (threading.Thread):
    def __init__(self, q, ql):
        threading.Thread.__init__(self)
        self.q = q
        self.ql = ql
    def run(self):
        process_data(self.q,self.ql)


def process_data(q,queueLock):
    while True:
        queueLock.acquire()
        if not q.empty():
            cmd = q.get()
            queueLock.release()
            runBash(cmd)
            time.sleep(1)
            q.task_done()
            print "%s done!" % cmd 
        else:
            queueLock.release()
            return


def parallelCmd(cmdList,nThreads):
    queueLock = threading.Lock()
    workQueue = Queue.Queue(len(cmdList))
    threads = []

    # Fill the queue
    queueLock.acquire()
    for cmd in cmdList:
        workQueue.put(cmd)
    queueLock.release()

    # Create new threads
    for t in range(nThreads):
        thread = myThread(workQueue,queueLock)
        thread.start()

    # Wait for queue to empty
    workQueue.join()
    print "All done!"

if __name__=="__main__":
    nThreads=2
    cmdList = ["touch One", "touch Two", "touch Three", "touch Four", "touch Five"]

    parallelCmd(cmdList,nThreads)
