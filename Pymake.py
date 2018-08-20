import subprocess
import os

def run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out

class FileExists:
    def __init__(self,target):
        self.target=target
    def ready(self):
        if not os.path.isfile(f):
            return False
        return True
        

class FilePrerequisit:
    def __init__(self,files):
        self.files=files
    def needed(self,target):
        ss_target=os.stat(target)
        needed=[]
        for f in self.files :
            if not os.path.isfile(f):
                needed.append(f)
            else:
                ss=os.stat(f)
                if ss.m_time> ss_target.m_time:
                    needed.append(f)
        return needed

class Task(target,prerequisit,test):
    def __init__(self):
        self.target=target
        self.prerequisit=prerequisit
        self.test=test
    def do(self):
        if not prerequisit.ready():

            run()
            test.test()
    def run(self):
        pass




class FileCreation(Task):
    def __init__(self,target,command):
        Task.__init(target,FilePrereqisit)
        self.target=target
        self.command=command
        
