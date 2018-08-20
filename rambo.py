import random
import math
from numpy import array
random.seed(1234)

def doublePi():
    return math.pi

math.get_pi=doublePi

def dot(a,b):
    return sum([a[i]*b[i] for i in range(len(a))],type(a[0])(0) )

def norm2(p):
    return p[0]*p[0]-dot(p[1:],p[1:])

def getRandomQ(RandomGenerator=random.random,Type=float,mathLib=math):
    c=Type(2)*RandomGenerator()-Type(1)
    phi=Type(2)*mathLib.get_pi()*RandomGenerator()
    q0=-mathLib.log(RandomGenerator()*RandomGenerator())
    qx=q0*mathLib.sqrt(Type(1)-c*c)*mathLib.cos(phi)
    qy=q0*mathLib.sqrt(Type(1)-c*c)*mathLib.sin(phi)
    qz=q0*c
    return (q0,qx,qy,qz)

def boost(q,x,gamma,b):
    Type=type(x)
    p0=x*(gamma*q[0]+dot(b,q[1:]))
    p= array(q[1:])
    p+= b*q[0]
    f=Type(1)/(Type(1)+gamma)
    f*=dot(b,q[1:])
    p+=b*f
    p*=x
    return (p0,)+tuple(p)

def finalStatePS(w,n,Type=float,mathLib=math,**kargs):
    qs = [ getRandomQ(Type=Type,mathLib=mathLib,**kargs) for i in range(n)]
    Q = array([ sum([q[j] for q in qs ],Type(0)) for j in range(4)])
    M = mathLib.sqrt(Q[0]*Q[0]-dot(Q[1:],Q[1:]))
    b = array( [-q/M for q in Q[1:] ]) 
    x = Type(w)/M 
    gamma = Q[0]/M 
    ps=[ boost(q,x,gamma,b) for q in qs ]
    return ps

def PS(n,Type=float,mathLib=math,RandomGenerator=random.random,**kargs):
    ctheta=Type(2)*RandomGenerator()-Type(1)
    stheta=mathLib.sqrt(Type(1)-ctheta*ctheta)
    phi=Type(2)*RandomGenerator()*mathLib.get_pi()    
    sphi=mathLib.sin(phi)
    cphi=mathLib.cos(phi)
    w=Type(n)
    E=w/Type(2)
    c=mathLib
    p1=(-E,
        -E*stheta*sphi,
        -E*stheta*cphi,
        -E*ctheta
    )
    p2 = ( -E , -p1[1], -p1[2], -p1[3])
    ps=finalStatePS(n,n-2,RandomGenerator=RandomGenerator,Type=Type,mathLib=mathLib,**kargs)
    return [ p1,p2] + ps 

