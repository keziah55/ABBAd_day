#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert mp3s to 8-bit 32kHz mono wav files and write ABBAd_day/fileArray.ino
file.
"""

import re
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
            track = track.replace(')', '\)')
            
            # wav file to write
            outfile = "{}.wav".format(i)
            out = os.path.join(outdir, outfile)
            
            # run sox
            subprocess.run(["sox", track, "-b", "8", "-r", "32000", "-c", "1", 
                            out])
    
            # increment wav number
            i += 1
    
    
def make_ino_file(path, wavdir):
    """ Make .ino file containing a function to populate an array of file names
    
        Paramters
        ---------
        path : str
            Path to .ino file directory
        wavdir : str
            Directory where the wavs are
    """
    
    inofile = os.path.join(path, 'fileArray.ino')
    
    # beginning of file
    out = '//////////////////////////////////////////////\n'
    out += '// This file is automatically generated by  //\n'
    out += '// convert_wav_arduino.py                   //\n'
    out += '//////////////////////////////////////////////\n\n'
    out += 'void makeFileArray() {\n'
    
    # get list of wavs and sort by number
    ls = os.listdir(wavdir)
    ls.sort(key=lambda s:float(s.split('.')[0]))
    
    # add lines to file
    for i, file in enumerate(ls):
        out += '    fileArray[{}] = "{}";\n'.format(i, file)
        
    out += '}\n'
        
    update_main_ino(path, len(ls))
        
    # write .ino file
    with open(inofile, 'w') as fileobj:
        fileobj.write(out)
        
        
def update_main_ino(path, size):
    """ Automatically change the array size in ABBAd_day.ino """
    
    inoFile = os.path.join(path, 'ABBAd_day.ino')
    
    # read file
    with open(inoFile) as fileobj:
        text = fileobj.read()
        
    # regexes of the two lines that need to be updated
    lines = [r'char \*fileArray\[(\d+)\];', r'int arrSize = (\d+);']
    
    for line in lines:
        # find line in text
        srch = re.search(line, text)
        # store original line
        full_line = srch.group(0)
        # get current array size from the line
        current_size = srch.group(1)
        # make new line by substituting the new size for the old size
        new_line = re.sub(current_size, str(size), full_line)
        # replace the line in the text
        text = re.sub(re.escape(full_line), new_line, text)
        
    # write updated file
    with open(inoFile, 'w') as fileobj:
        fileobj.write(text)
    

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('mp3FileList', help='File listing mp3 files to be '
                        'converted. Please provide full path to each.')
    parser.add_argument('wavDir', help='Path to write wavs to.')

    args = parser.parse_args()
        
    print('Converting to wav...', end='')
    make_wavs(args.mp3FileList, args.wavDir)
    print('Done!')
    
    print('Writing .ino file...', end='')
    inoDir = 'ABBAd_day'
    make_ino_file(inoDir, args.wavDir)
    print('Done!')
    
