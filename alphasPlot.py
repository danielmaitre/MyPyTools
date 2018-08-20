import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#scale factor


path='/home/daniel/workspace/LHAPDF/install_dir/'
import sys
sys.path.append('%s/python2.6/site-packages/' % path)
sys.path.append('%s/lib/' % path)

import lhapdf
lhapdf.initPDFSetByName("cteq6mE.LHgrid")
lhapdf.initPDF(0)
print "alpha_s(Mz) = ", lhapdf.alphasPDF(91.2) 


sf=1/lhapdf.alphasPDF(90.1)

x=range(100,1500)
y=[sf*lhapdf.alphasPDF(xx) for xx in x ]
y2=[yy*yy for yy in y]
y3=[yy*yy*yy for yy in y]
y4=[yy*yy*yy*yy for yy in y]
y5=[yy*yy*yy*yy*yy for yy in y]


from matplotlib import rc

import matplotlib as mpl

rc('text',usetex=True)
mpl.rcParams['font.size']=20.0

rc('axes',edgecolor='y')
rc('text',color='y')
rc('xtick',color='y')
rc('ytick',color='y')
rc('axes',labelcolor='y')

fig = plt.figure(figsize=(8,5))
ax  = fig.add_subplot(111)

#box = ax.get_position()
#ax.set_position([0.3, 0.4, box.width*0.3, box.height])
# you can set the position manually, with setting left,buttom, witdh, hight of the axis
# object
ax.set_position([0.1,0.1,0.6,0.8])
#ax.plot(x, y)

plt.title('Renormalisation scale dependence')
plt.xlabel(r'$\mu$')

ax.plot(x,y,label=r'$\alpha_S(\mu)/\alpha_S(M_Z)$',linewidth = 5)
ax.plot(x,y2,label=r'$\alpha_S^2(\mu)/\alpha_S^2(M_Z)$',linewidth = 5)
ax.plot(x,y3,label=r'$\alpha_S^3(\mu)/\alpha_S^3(M_Z)$',linewidth = 5)
ax.plot(x,y4,label=r'$\alpha_S^4(\mu)/\alpha_S^4(M_Z)$',linewidth = 5)
ax.plot(x,y5,label=r'$\alpha_S^5(\mu)/\alpha_S^5(M_Z)$',linewidth = 5)
leg=ax.legend(bbox_to_anchor=(0.7, 1), loc=2, borderaxespad=0.)
#leg.get_frame().set_alpha(0.5)




#for t in leg.get_texts():
#    t.set_color('y')

plt.savefig('alphasPlot.png',transparent=True)
plt.show()


