#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert mp3s to 8-bit 32kHz mono wav files
"""

import os
import subprocess
import argparse


def make_wavs(filelist, outdir):
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    i = 0
    
    with open(filelist) as fileobj:
        line = ' '
        
        while True:
            
            line = fileobj.readline()
            line = line.strip()
            
            if not line:
                break
            
            track = line
            
            track = track.replace(' ', '\ ')
            track = track.replace('(', '\(')
            track = track.replace(')', ')')
            
            outfile = "{}.wav".format(i)
            out = os.path.join(outdir, outfile)
            
            subprocess.run(["sox", track, "-b", "8", "-r", "32000", "-c", "1", 
                            out])
            
            i += 1
    
    
def make_ino_file(inofile, wavdir):
    
    out = 'void makeFileArray() {\n'
    
    ls = os.listdir(wavdir)
    ls.sort(key=lambda s:float(s.split('.')[0]))
    
    for i, file in enumerate(ls):
        out += '    fileArray[{}] = "{}";\n'.format(i, file)
        
    out += '}\n'
        
    with open(inofile, 'w') as fileobj:
        fileobj.write(out)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('mp3FileList', help='file listing mp3 files to be '
                        'converted')
    parser.add_argument('wavDir', help='Path to write wavs to')
    parser.add_argument('inoFile', help='Filename to write ino file to')

    args = parser.parse_args()
        
    print('Converting to wav...', end='')
    make_wavs(args.mp3FileList, args.wavDir)
    print('Done!')
    
    print('Writing .ino file...', end='')
    make_ino_file(args.inoFile, args.wavDir)
    print('Done!')
    