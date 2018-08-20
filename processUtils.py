Wm1j_Info={
    'njets':1 ,
    'nparticles':4,
    'particles':['electron','neutrino'],
    'particlesPDGcodes':[11,-12],
    'nonpartons' : [0,1],
    'alphaPower':1
}
Wm4j_Info={
    'njets':4 ,
    'nparticles':7,
    'particles':['electron','neutrino'],
    'particlesPDGcodes':[11,-12],
    'nonpartons' : [0,1],
    'alphaPower':4
}
Z0j_Info={
    'njets':0 ,
    'nparticles':3,
    'particles':['electron','positron'],
    'particlesPDGcodes':[11,-11],
    'nonpartons' : [0,1],
    'alphaPower':0
}
Z1j_Info={
    'njets':1 ,
    'nparticles':4,
    'particles':['electron','positron'],
    'particlesPDGcodes':[11,-11],
    'nonpartons' : [0,1],
    'alphaPower':1
}
Z2j_Info={
    'njets':2 ,
    'nparticles':5,
    'particles':['electron','positron'],
    'particlesPDGcodes':[11,-11],
    'nonpartons' : [0,1],
    'alphaPower':2
}
Z3j_Info={
    'njets':3 ,
    'nparticles':6,
    'particles':['electron','positron'],
    'particlesPDGcodes':[11,-11],
    'nonpartons' : [0,1],
    'alphaPower':3
}
Z4j_Info={
    'njets':4 ,
    'nparticles':7,
    'particles':['electron','positron'],
    'particlesPDGcodes':[11,-11],
    'nonpartons' : [0,1],
    'alphaPower':4
}

def getInfo(process):
    return {
        'Wm1j': Wm1j_Info,
        'Wm4j': Wm4j_Info,
        'Z0j': Z0j_Info,
        'Z1j': Z1j_Info,
        'Z2j': Z2j_Info,
        'Z3j': Z3j_Info,
        'Z4j': Z4j_Info
    }[process]

processBlockTemplate = """
<Process>

NbrParticles {nparticles}
ParticlesNames {{ {particlesList} }}
ParticlesPDGCodes {{ {pdgcodesList} }}
NonPartons {{ {nonpartonsList}  }}
AlphasPower {alphaPower}

</Process>
"""

def getProcessBlock(process):
    info = getInfo(process)
    info['particlesList'] = ' , '.join(info['particles'])
    info['pdgcodesList'] = ' , '.join(map(str,info['particlesPDGcodes']))
    info['nonpartonsList'] = ' , '.join(map(str,info['nonpartons']))
    return processBlockTemplate.format(**info)
