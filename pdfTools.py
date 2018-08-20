import numpy as np

nMembers = {
    'CT10': 52,
    'CT14': 56,
    'MSTW': 40,
    'MMHT': 50,
    'NNPDF': 100,
    'NNPDF3': 100,
    'NNPDF31': 100,
    'ABM': 28,
}

factor={
    'CT10': 1/1.645,   # this is what one gets for  scipy.special.erfinv(0.9)/scipy.special.erfinv(0.6826)
    'MSTW': 1,
    'NNPDF': 1,
    'CT14': 1/1.645,   # this is what one gets for  scipy.special.erfinv(0.9)/scipy.special.erfinv(0.6826)
    'MMHT': 1,
    'NNPDF3': 1,
    'NNPDF31': 1,
    'ABM':1,
}

lhapdfSuffix=''

pdfErrorFiles={
    "CT10":"CT10nlo"+lhapdfSuffix,
    "CT14":"CT14nlo"+lhapdfSuffix,
    "NNPDF":"NNPDF23_nlo_as_0118"+lhapdfSuffix,
    "NNPDF3":"NNPDF30_nlo_as_0118"+lhapdfSuffix,
    "NNPDF31":"NNPDF31_nlo_as_0118"+lhapdfSuffix,
    "MSTW":"MSTW2008nlo68cl"+lhapdfSuffix,
    "MMHT":"MMHT2014nlo68cl"+lhapdfSuffix,
    "ABM":"abm11_5n_nlo"+lhapdfSuffix
}

errorType = {
    'CT10': 'hessian',
    'MSTW' : 'hessian',
    'NNPDF' : 'mc',
    'CT14' : 'hessian',
    'MMHT' : 'hessian',
    'NNPDF3' : 'mc',
    'NNPDF31' : 'mc',
    'ABM': 'hessianSym'
}


def hessian(central,members,factor):
    n=len(central)
    cov=np.zeros((n,n))
    nMembers=len(members)
    for i in range(0,nMembers/2):
        down=np.array(members[2*i])
        up=np.array(members[2*i+1])
        diff=np.array([up-down])
        diff=diff*factor
        C=np.dot(diff.transpose(),diff) 
        cov=cov+C
    cov=cov/4.0
    return cov

def hessianSym(central,members,factor):
    n=len(central)
    cov=np.zeros((n,n))
    nMembers=len(members)
    for i in range(0,nMembers):
        mem=np.array(members[i])
        diff=np.array([central-mem])
        diff=diff*factor
        C=np.dot(diff.transpose(),diff) 
        cov=cov+C
    return cov


def MCerror(central,members,factor):
    n=len(central)
    cov=np.zeros((n,n))
    for m in members:
        diff=np.array(m)-central
        diff=np.array([diff*factor])
        C=np.dot(diff.transpose(),diff) 
        cov+=C

    cov=cov/(len(members)-1)
    print len(members)
    return cov



