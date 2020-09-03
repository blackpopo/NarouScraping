import sys
import os
import getopt

processed = False
dir = ''
file = ''

if __name__=='__main__':
    base_dir = '/home/maya/PycharmProjects/NarouScraping/SS_v11'
    ops, args = getopt.getopt(sys.argv[1:], 'pd:f:', ['processed', 'directory=', 'file='])
    for o, a in ops:
        if o in ('-p', '--processed'):
            processed = True
        elif o in ('-d', '--directory'):
            dir = a
        elif o in ('-f', '--file'):
            file = a
        else:
            assert False, 'Unhandled Option!'

    if processed:
        dir = dir + '_processed'
        file = file + '_processed.txt'

    with open(os.path.join(base_dir, dir, file)) as f:
        lines = f.readlines()

    for line in lines:
        print(line.rstrip('\n'))
