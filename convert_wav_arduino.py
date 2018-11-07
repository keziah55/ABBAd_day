#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert mp3s to 8-bit 32kHz mono wav files
"""

import os
import subprocess
import argparse


def make_wavs(filelist, outdir):
    """ Convert files to wavs that an Arduino can play
    
        Paramters
        ---------
        filelist : str
            Path to a file containing the file names to be converted
        outdir : str
            Path to directory where wavs should be saved
    """
    
    # if wav dir does not exist, make it
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    # wav number (for file name)
    i = 0
    
    with open(filelist) as fileobj:
        
        line = ' ' # non-empty string so it can be used as 'while' condition
        
        while line:
            
            # get next track name
            line = fileobj.readline()
            # remove newline character from end
            line = line.strip() 
            
            # make 'track' variable and escape special characters
            track = line
            track = track.replace(' ', '\ ')
            track = track.replace('(', '\(')
            track = track.replace(')', ')')
            
            # wav file to write
            outfile = "{}.wav".format(i)
            out = os.path.join(outdir, outfile)
            
            # run sox
            subprocess.run(["sox", track, "-b", "8", "-r", "32000", "-c", "1", 
                            out])
    
            # increment wav number
            i += 1
    
    
def make_ino_file(inofile, wavdir):
    """ Make .ino file containing a function to populate an array of file names
    
        Paramters
        ---------
        inofile : str
            Path to file to
        wavdir : str
            Directory where the wavs are
    """
    
    # beginning of file
    out = 'void makeFileArray() {\n'
    
    # get list of wavs and sort by number
    ls = os.listdir(wavdir)
    ls.sort(key=lambda s:float(s.split('.')[0]))
    
    # add lines to file
    for i, file in enumerate(ls):
        out += '    fileArray[{}] = "{}";\n'.format(i, file)
        
    out += '}\n'
        
    # write .ino file
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
    