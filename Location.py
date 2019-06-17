import socket
import re

cernHost=re.compile(r'.*cern\.ch.*')
kelvinHost=re.compile(r'(?:.*alineos.*)|(?:.*cea\.fr)')
hoffman2Host=re.compile(r'login.*')
durhamHost=re.compile(r'.*\.ac\.uk')
ithakaHost=re.compile(r'm076\..*|ithaka')

def whereAmI():
    hostname=socket.gethostname()
    if cernHost.match(hostname):
        return 'CERN'
    if kelvinHost.match(hostname):  
	return 'KELVIN'
    if hostname == 'spartacus':
        return 'SPARTACUS'
    if hoffman2Host.match(hostname):
        return 'HOFFMAN2'
    if durhamHost.match(hostname):
        return 'IPPP'
    if ithakaHost.match(hostname):
        return 'ITHAKA'
    if re.match('scummy',hostname):
        return 'SCUMMY'
    if re.match('xps',hostname):
        return 'XPS'

    

HOME={
    'HOFFMAN2':'/u/home/bern/maitreda',
    'HOFFMAN2_NTUPLES':'/u/home/bern/maitreda',
    'KELVIN':'/home/dmaitre',
    'CERN':'/afs/cern.ch/user/d/dmaitre',
    'IPPP':'/home/daniel',
    'ITHAKA':'/home/daniel',
    'SCUMMY':'/home/daniel'
}

def home():
    return HOME.get(whereAmI(),'unknown')
