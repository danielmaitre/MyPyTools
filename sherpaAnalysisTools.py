def readSherpaScale(filename,part):
    f=open(filename)
    lines=f.readlines()
    index=lines[1].split().index(part)-1
    numlines=[l.split() for l in lines[2:]]
    xs=[float(l[0]) for l in numlines]
    values=[ float(l[index]) for l in numlines ]
    errors=[ float(l[index+1]) for l in numlines ]

    return xs,values,errors
