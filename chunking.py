import pandas as pd
import numpy as np
import csv
import os

#in_file_384 = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV\MIDI-Unprocessed_01_R1_2006_01-09_ORIG_MID--AUDIO_01_R1_2006_01_Track01_wav.csv'
#out_file_384 = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\Chunks\MIDI-Unprocessed_01_R1_2006_01-09_ORIG_MID--AUDIO_01_R1_2006_01_Track01_wav_chunkedwithcontrolc.csv'
#in_file_480 = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV\MIDI-Unprocessed_041_PIANO041_MID--AUDIO-split_07-06-17_Piano-e_1-01_wav--1.csv'
#out_file_480 = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\Chunks\MIDI-Unprocessed_041_PIANO041_MID--AUDIO-split_07-06-17_Piano-e_1-01_wav--1_chunkedwithcontrolc.csv'
test_file_size_as_input = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV\MIDI-Unprocessed_03_R2_2011_MID--AUDIO_R2-D1_07_Track07_wav.csv'
output = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\Chunks\MIDI-Unprocessed_03_R2_2011_MID--AUDIO_R2-D1_07_Track07_wavchunksizeasinput.csv'

def chunk(input_file, output_file, size):
    song = pd.read_csv(input_file, names = ["Track", "Tick", "Call", "Channel", "Note", "Velocity", "0"])
    chunk = [0.000]*132
    chunk[0] = "Time"
    chunk[129] = "64 Control_c"
    chunk[130] = "67 Control_c"
    chunk[131] = "66 Control_c"
    for i in range(0,128):
        chunk[i+1] = str(i)+" Note_on_c"
    with open(output_file, 'a', newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(chunk)
    chunk = [0.000]*132
    num_rows = len(song.axes[0])-1
    row = 0
    ppq = song.loc[row, "Velocity"]
    step = (ppq*size)/8000
    for i in np.arange (0, song.loc[num_rows-1, "Tick"], step):
        nexti = i+step
        cur_tick = song.loc[row, "Tick"]
        while i <= cur_tick and cur_tick <= nexti:
            chunk[0] = i/(2*ppq)
            cur_call = song.loc[row, "Call"]
            if(cur_call == " Note_on_c"):
                cur_note = song.loc[row, "Note"]
                cur_vel = song.loc[row, "Velocity"]
                chunk[int(cur_note)+1]=cur_vel/127
            if(cur_call == " Control_c"):
                cur_note = song.loc[row, "Note"]
                cur_vel = song.loc[row, "Velocity"]
                place = 0
                if(cur_note == 64):
                    place = 129
                elif(cur_note == 67):
                    place = 130
                elif(cur_note == 66):
                    place = 131
                chunk[place]=cur_vel/127
            row+=1
            cur_tick = song.loc[row, "Tick"]
        with open(output_file, 'a', newline='') as result_file:
            wr = csv.writer(result_file, dialect='excel')
            wr.writerow(chunk)
pass

def batchchunkall(directory, size):
    count = 0
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".csv"):
                count+=1
                newfile = filepath.replace("\CSV","\Chunks" )
                newfile = newfile.replace(".csv", "1024chunk.csv")
                chunk(filepath, newfile, size)
                print(count)
pass

batchchunkall(r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV', 1024)

