# ABBAd_day

A very stupid project for anyone who has ever wanted 
to make their flatmate's kitchen cupboard play ABBA 
songs whenever they open the door (or any songs really.)

I built (and tested) this project with an Arduino Uno. 
For some reason, I couldn't get a Nano to read an SD card.
I'll upload a circuit diagram eventually.

## Hardware
* Arduino Uno
* 9V battery and battery clip
* LDR
* 200kOhm resistor
* SD card and SD card reader
* 0.2W speaker

## Software
`convert_wav_arduino.py` is a Python script which provides 
two functions. 

The first takes a file which lists a bunch of mp3s 
and converts them to wav files (8-bit, 32kHz, mono wavs, so that
the Arduino can play them).

The second makes another .ino file which contains an array of 
the wav file names.

You can run `convert_wav_arduino.py` from the command line to
execute both of these functions. Use `--help` to get the command
line args.

Note that you'll have to change the array size in `ABBAd_day.ino`
manually until I get round to doing it properly.


## Requirements
* sox
* TMRpcm (https://github.com/TMRh20/TMRpcm)
