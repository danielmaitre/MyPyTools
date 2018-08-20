import urllib2
import re
import ROOT
from array import array
import math

lineregex=re.compile(r'\t*(?P<x>[\d\.]+(?:E[+-]\d+)?)\t(?P<xlow>[\d\.]+(?:E[+-]\d+)?)\t(?P<xhigh>[\d\.]+(?:E[+-]\d+)?)\t(?P<y>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp2>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym2>[\d\.]+(?:E[+-]\d+)?).*\n')


line2regex=re.compile(r'\t*(?P<x>[\d\.]+(?:E[+-]\d+)?)\t(?P<xlow>[\d\.]+(?:E[+-]\d+)?)\t(?P<xhigh>[\d\.]+(?:E[+-]\d+)?)\t(?P<y>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp2>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym2>[\d\.]+(?:E[+-]\d+)?)\t(?P<y2>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dy2p>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dy2m>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dy2p2>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dy2m2>[\d\.]+(?:E[+-]\d+)?).*\n')


line3regex=re.compile(r'\t*(?P<x>[\d\.]+(?:E[+-]\d+)?)\t(?P<xlow>[\d\.]+(?:E[+-]\d+)?)\t(?P<xhigh>[\d\.]+(?:E[+-]\d+)?)\t(?P<y>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp2>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym2>[\d\.]+(?:E[+-]\d+)?)\t\+(?P<dyp3>[\d\.]+(?:E[+-]\d+)?)\t\-(?P<dym3>[\d\.]+(?:E[+-]\d+)?).*\n')

def dpatt(name):
    return "(?P<%s>[\d\.]+(?:E[+-]\d+)?)" % name

line4txt=r'\t*'+dpatt('x')+'\t'+dpatt('xlow')+'\t'+dpatt('xhigh')+'\t'
line4txt=line4txt+dpatt('y')+'\t'+'+'+dpatt('dyp')+'\t\-'+dpatt('dym')
line4txt=line4txt+'\t+'+dpatt('dyp2')+'\t\-'+dpatt('dym2')
line4txt=line4txt+'\t+'+dpatt('dyp3')+'\t\-'+dpatt('dym3')
line4txt=line4txt+dpatt('y2')+'\t'+'+'+dpatt('dy2p')+'\t\-'+dpatt('dy2m')
line4txt=line4txt+'\t+'+dpatt('dy2p2')+'\t\-'+dpatt('dy2m2')
line4txt=line4txt+'\t+'+dpatt('dy2p3')+'\t\-'+dpatt('dy2m3')
line4txt=line4txt+'\t+'+dpatt('dy2p4')+'\t\-'+dpatt('dy2m4')
line4txt=line4txt+dpatt('y3')+'\t'+'+'+dpatt('dy3p')+'\t\-'+dpatt('dy3m')
line4txt=line4txt+'\t+'+dpatt('dy3p2')+'\t\-'+dpatt('dy3m2')
line4txt=line4txt+'\t+'+dpatt('dy3p3')+'\t\-'+dpatt('dy3m3')
line4txt=line4txt+'\t+'+dpatt('dy3p4')+'\t\-'+dpatt('dy3m4')
line4txt+='\n'

line4regex=re.compile(line4txt)


def extractHistogram(url,name,name2=None,nErrors=2):
    xs=[]
    xus=[]
    xds=[]
    ys=[]
    yus=[]
    yds=[]
    yu1s=[]
    yd1s=[]
    yu2s=[]
    yd2s=[]
    yu3s=[]
    yd3s=[]

    y2s=[]
    y2us=[]
    y2ds=[]
    website = urllib2.urlopen(url)
    ls=website.readlines()

    nEntries=0
    for l in ls:
        if nErrors==3:
            match=line3regex.match(l)
        elif name2:
            match=line2regex.match(l)
        else:
            match=lineregex.match(l)
            

        if match :
            nEntries+=1
            print match.group('x'),match.group('y')
            xs.append(float(match.group('x')))
            dyu1=float(match.group('dyp'))
            dyu2=float(match.group('dyp2'))
            dyd1=float(match.group('dym'))
            dyd2=float(match.group('dym2'))
            if nErrors==3:
                dyu3=float(match.group('dyp3'))
                dyd3=float(match.group('dym3'))
                du=math.sqrt(dyu1*dyu1+dyu2*dyu2+dyu3*dyu3)
                dd=math.sqrt(dyd1*dyd1+dyd2*dyd2+dyd3*dyd3)
            else:
                du=math.sqrt(dyu1*dyu1+dyu2*dyu2)
                dd=math.sqrt(dyd1*dyd1+dyd2*dyd2)

            xus.append(float(match.group('x'))-float(match.group('xlow')))
            xds.append(float(match.group('xhigh'))-float(match.group('x')))
            ys.append(float(match.group('y')))
            yus.append(du)
            yds.append(dd)
            yu1s.append(dyu1)
            yd1s.append(dyd1)
            yu2s.append(dyu2)
            yd2s.append(dyd2)
            if nErrors==3:
                yu3s.append(dyu3)
                yd3s.append(dyd3)

            if name2:
                dy2u1=float(match.group('dy2p'))
                dy2u2=float(match.group('dy2p2'))
                dy2d1=float(match.group('dy2m'))
                dy2d2=float(match.group('dy2m2'))
                d2u=math.sqrt(dy2u1*dy2u1+dy2u2*dy2u2)
                d2d=math.sqrt(dy2d1*dy2d1+dy2d2*dy2d2)
                y2s.append(float(match.group('y2')))
                y2us.append(d2u)
                y2ds.append(d2d)




            

    g=ROOT.TGraphAsymmErrors(nEntries,
                             array('d',xs),
                             array('d',ys),
                             array('d',xds),
                             array('d',xus),
                             array('d',yds),
                             array('d',yus)
                             )

    g.SetName(name)
    g.Write()
    errorgs=[('1',yu1s,yd1s),('2',yu2s,yd2s)]
    if nErrors==3:
        errorgs.append(('3',yu3s,yd3s))
    for ename,eu,ed in errorgs:
        ge=ROOT.TGraphAsymmErrors(nEntries,
                             array('d',xs),
                             array('d',ys),
                             array('d',xds),
                             array('d',xus),
                             array('d',ed),
                             array('d',eu)
                             )

        ge.SetName(name+'_e'+ename)
        ge.Write()
    
    if name2:
        g2=ROOT.TGraphAsymmErrors(nEntries,
                             array('d',xs),
                             array('d',y2s),
                             array('d',xds),
                             array('d',xus),
                             array('d',y2ds),
                             array('d',y2us)
                             )

        g2.SetName(name2)
        g2.Write()


if __name__=='__main__':
    f=ROOT.TFile('hepdata.root','recreate')

    figureMap={

    '1':'g_4a_DY_1_2' ,
    '2':'g_4a_DY_2_3' ,
    '3':'g_4a_DY_3_4' ,
    '4':'g_4a_DY_4_5' ,
    '5':'g_4a_DY_5_6' ,


    '13':'g_5a_avpt_70_90_DY_2_3' ,
    '14':'g_5a_avpt_70_90_DY_4_5' ,
    '15':'g_5a_avpt_120_150_DY_2_3' ,
    '16':'g_5a_avpt_120_150_DY_4_5' ,
    '17':'g_5a_avpt_210_240_DY_2_3' ,
    '18':'g_5a_avpt_210_240_DY_4_5' ,

    '19':'g_8a_avpt_70_90' ,
    '20':'g_8a_avpt_90_120' ,
    '21':'g_8a_avpt_120_150' ,
    '22':'g_8a_avpt_150_180' ,
    '23':'g_8a_avpt_180_210' ,
    '24':'g_8a_avpt_210_240' ,
    '25':'g_8a_avpt_240_270' ,


    '26':'g_6a_avpt_DY_1_2' ,
    '27':'g_6a_avpt_DY_2_3' ,
    '28':'g_6a_avpt_DY_3_4' ,
    '29':'g_6a_avpt_DY_4_5' 





        }

    for index in figureMap.keys():
        extractHistogram('http://hepdata.cedar.ac.uk/view/irn9126244/d%s/plain.txt' % index,figureMap[index])


    figure2Map={



    '6':('g_3a_avpt_70_90','g_7a_avpt_70_90') ,
    '7':('g_3a_avpt_90_120','g_7a_avpt_90_120') ,
    '8':('g_3a_avpt_120_150','g_7a_avpt_120_150') ,
    '9':('g_3a_avpt_150_180','g_7a_avpt_150_180') ,
    '10':('g_3a_avpt_180_210','g_7a_avpt_180_210') ,
    '11':('g_3a_avpt_210_240','g_7a_avpt_210_240') ,
    '12':('g_3a_avpt_240_270','g_7a_avpt_240_270') ,

    }



    for index in figure2Map.keys():
        extractHistogram('http://hepdata.cedar.ac.uk/view/irn9126244/d%s/plain.txt' % index,figure2Map[index][0],figure2Map[index][1])
