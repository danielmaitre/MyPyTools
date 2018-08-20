import sys
sys.path.append('/home/daniel/workspace/BHlib/build/lib/')
sys.path.append('/home/daniel/workspace/BHlib/my_programs')
import BH


p = BH.cvar.p
m = BH.cvar.m
PRO = BH.process(p,m,p,m,p,m)
A=BH.TreeHelAmpl(PRO)
ind = BH.vectori([1,2,3,4,5,6])

RG=BH.GMP_random()
RGr = RG.random
RG.seed(123456)
BH.RGMP_set_precision(1024)

import rambo 


ps =rambo.PS(6,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
cms = [ BH.Cmomgmp(*p) for p in ps ]
mc = BH.mcgmp(*cms)
r1 = A.eval(mc,ind)


RG.seed(123456)
BH.RGMP_set_precision(2048)

ps =rambo.PS(6,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
cms = [ BH.Cmomgmp(*p) for p in ps ]
mc = BH.mcgmp(*cms)
r2 = A.eval(mc,ind)

ps =rambo.PS(4,RandomGenerator=RGr,Type=BH.RGMP,mathLib=BH)
cms = [ BH.Cmomgmp(*p) for p in ps ]
mc = BH.mcgmp(*cms)
