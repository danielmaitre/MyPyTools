import matplotlib as mpl

mpl.use('Agg')

import histPlotTools as hpt
import sys


import argparse

parser = argparse.ArgumentParser(description='Creates an histogram from a root file.')
parser.add_argument('rootfile',  type=str, 
                    help='the root file where the histogram is')
parser.add_argument('histogramName',  type=str, 
                    help='the name of the histogram')
parser.add_argument('--logx', dest='logx', action='store_const',
                    const=True, default=False,
                    help='whether to use a logarithmic x scale')
parser.add_argument('--logy', dest='logy', action='store_const',
                    const=True, default=False,
                    help='whether to use a logarithmic y scale')

parser.add_argument('-o', dest='output', type=str,
                    help='where to save the file')

args = parser.parse_args()



p=hpt.Plot()
p.title=args.histogramName
p.addLineFromRoot(args.rootfile,args.histogramName)


p.makePlot()

if args.logx:
    hpt.pylab.xscale('log')
if args.logy:
    hpt.pylab.yscale('log')


if args.output:
    p.fig.savefig(args.output)
else:
    p.show()
