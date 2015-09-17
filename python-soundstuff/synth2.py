#infinite replays.
#option to restart rather than automatic
#make loudness between 1 and 10
#accept notes+volumes as tuples
#GUI?
#uppercase/lowercase notes
#figure out screenshotted error

import math
import wave
import struct
from pygame import mixer

# Code from Nemeth at http://stackoverflow.com/a/5174008
# Also, rework this to accept ([freq], [coef]) tuple instead.
def synthComplex(freq=[440], coef=[1], datasize=10000, fname="test.wav"):
    frate = 44100.00
    amp = 8000.0
    sine_list = []
    for x in range(datasize):
        samp = 0
        for k in range(len(freq)):
            samp = samp + coef[k] * math.sin(2*math.pi*freq[k]*(x/frate))
        sine_list.append(samp)
    wav_file = wave.open(fname, "w")
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = datasize
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    for s in sine_list:
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    wav_file.close()

#def get_list(prompt='Enter a list. '):
#    while (True):
#        mylist = raw_input(prompt).strip()
#        if not mylist.startswith('[') or not mylist.endswith(']'):
#            continue # Make user input proper list or force quit. Hah.
#        else: return eval(mylist)

# Generate tone id for storage. Very particular, would like to generalize. (Can pass strings and lists, will cram it all together?)
def tone_id(notes, coef, length):
    id_list = [str(x) for x in notes + coef]
    id_list.append(str(length))
    tone_id = ''.join(id_list)
    return tone_id
	

FREQS = {'A1':55.000, 'A2':110.000, 'A3':220.000, 'A4':440.000, 'A5':880.000,
        'A6':1760.000, 'A#1':58.270, 'A#2':116.541, 'A#3':233.082, 'A#4':466.164,
        'A#5':932.328, 'A#6':1864.655, 'B1':61.735, 'B2':123.471, 'B3':246.942,
        'B4':493.883, 'B5':987.767, 'B6':1975.533, 'C1':65.406, 'C2':130.813,
        'C3':261.626, 'C4':523.251, 'C5':1046.502, 'C6':2093.005, 'C#1':69.296,
        'C#2':138.591, 'C#3':277.183, 'C#4':554.365, 'C#5':1108.731, 'C#6':2217.461,
        'D1':73.416, 'D2':146.832, 'D3':293.665, 'D4':587.330, 'D5':1174.659,
        'D6':2349.318, 'D#1':77.782, 'D#2':155.563, 'D#3':311.127, 'D#4':622.254,
        'D#5':1244.508, 'D#6':2489.016, 'E1':82.407, 'E2':164.814, 'E3':329.628,
        'E4':659.255, 'E5':1318.510, 'E6':2637.020, 'F1':87.307, 'F2':174.614,
        'F3':349.228, 'F4':698.456, 'F5':1396.913, 'F6':2793.826, 'F#1':92.499,
        'F#2':184.997, 'F#3':369.994, 'F#4':739.989, 'F#5':1479.978, 'F#6':2959.955,
        'G1':97.999, 'G2':195.998, 'G3':391.995, 'G4':783.991, 'G5':1567.982,
        'G6':3135.963, 'G#1':103.826, 'G#2':207.652, 'G#3':415.305, 'G#4':830.609,
        'G#5':1661.219, 'G#6':3322.438, 'A':220.000,'A#':233.082, 'B':246.942,
        'C':261.626, 'C#':277.183, 'D':293.655, 'D#':311.127, 'E':329.628,
        'F':349.228, 'F#':369.994, 'G':391.995, 'G#':415.305}

mixer.init()

# Synthesize and play tones to user specifications. Store tones for playback later.
tone_dict = {}
go = True
while (go):

    print ''
    while (True):

        notes = raw_input('List of notes? ').replace(' ','').split(',')
        invalid_note = False
        for note in notes:
            if note not in FREQS.keys():
                print note + ' is not an accepted note.'
                invalid_note = True
                break
        if invalid_note: continue
        freq = [FREQS[note] for note in notes if note in FREQS.keys()]

# Idiot-proof this.
        coef = raw_input('Relative volume of notes? (0.0-1.0) ').replace(' ','').split(',')
        coef = [float(x) for x in coef]

        if len(notes) != len(coef): 
            print 'Please input the same number of values for notes and volumes.'
            continue
        else: break

    length = float(raw_input('Length of tone in seconds? '))
    datasize = int(44100.00*length) # Assuming fixed frate as in complexSynth method above.    
    tone_id = tone_id(notes, coef, length)

    print ''
    
    if tone_id not in tone_dict:
        fname = tone_id + '.wav'
        synthComplex(freq, coef, datasize, fname)
        tone_dict[tone_id] = mixer.Sound(fname)
        print 'Tone synthesized and stored.'

    print 'Playing tone.'
    tone = tone_dict[tone_id]
    tone.play()

    # Need replay/new tone/quit menu.
    print ''
    print '(r)eplay, (n)ew tone, or (q)uit? '
    choice = raw_input()
    if 'r' in choice or 'R' in choice: tone.play()
    elif 'q' in choice or 'Q' in choice: go = False
    
