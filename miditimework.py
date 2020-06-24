from mido import MidiFile, second2tick
import os
import sox
import shutil
from sox import file_info
import math
import csv

temp = ["Audio Path", "Midi Path", "CSV Path", "Length in Seconds", "Length in Ticks", "Number of Samples", "Ticks per Second", "Samples per Second", "Samples per Tick"]


#include in sheet:
#audio file name ***********[0] (r'filename')
#midi file name ************[1] (r'filename')
#csv file name *************[2] (r'filename')
#length of audio in sec ****[3] (mid.length)
#length of midi in ticks ***[4] (math.ceil(second2tick(mid.length, mid.ticks_per_beat, 500000)))
#number of samples *********[5] (file_info.num_samples(file))
#ticks per sec *************[6] (ticks/sec)
#samples per sec ***********[7] (samples/sec)
#samples per tick **********[8] (samples/ticks)

audioloc = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\AudioOnly'
midiloc = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\MidiOnly'
csvloc = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV'

def allinfo(directory, temp):
    n = 0
    with open(r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\masterInfo.csv', 'w+', newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(temp)
    
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith("_cutandresample.wav"):
                audiopath = subdir + os.sep + filename
                audioname = filename
                temp[0] = audioname
                
                midipath = audiopath
                midipath = midipath.replace("AudioOnly", "MidiOnly")
                midipath = midipath.replace("_cutandresample.wav", ".midi")
                midiname = filename
                midiname = midiname.replace("_cutandresample.wav", ".midi")
                temp[1] = midiname
                
                csvpath = audiopath
                csvpath = csvpath.replace("AudioOnly", "CSV")
                csvpath = csvpath.replace("_cutandresample.wav", ".csv")
                csvname = filename
                csvname = csvname.replace("_cutandresample.wav", ".csv")
                temp[2] = csvname

                mid = MidiFile(midipath)
                leng = mid.length
                temp[3] = leng

                tic = math.ceil(second2tick(mid.length, mid.ticks_per_beat, 500000))
                temp[4] = tic

                samp = file_info.num_samples(audiopath)
                temp[5] = samp

                temp[6] = tic/leng

                temp[7] = samp/leng

                temp[8] = samp/tic

                with open(r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\masterInfo.csv', 'a', newline='') as result_file:
                    wr = csv.writer(result_file, dialect='excel')
                    wr.writerow(temp)
                n+=1
                print("Created line", n)

pass

def writeinfotocsv(directory):
    f = open(r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\timemath.csv', 'w')
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".midi"):
                mid = MidiFile(filepath)
                temp[0] = str(filepath)
                temp[1] = " Length: "+str(mid.length)
                for i in range(len(temp)):
                    f.write(temp[i])
                f.write("\n")
pass

def copyaudiotonewfolder(directory, destination):
    n = 0
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".wav"):
                shutil.copy(filepath, destination)
                n+=1
                print("Audio", n)
pass

def copymiditonewfolder(directory, destination):
    n = 0
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".midi"):
                shutil.copy(filepath, destination)
                n+=1
                print("Midi",n)
pass

def cutaudio(audio_path):
    n = 0
    for subdir, dirs, files in os.walk(audio_path):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".wav"):
                midiversion = filepath
                midiversion = midiversion.replace('.wav', '.midi')
                midiversion = midiversion.replace('AudioOnly', 'MidiOnly')
                mid = MidiFile(midiversion)
                newfile = filepath
                newfile = newfile.replace('.wav', '_cut.wav')
                tfm = sox.Transformer()
                tfm.trim(0,mid.length)
                tfm.build(filepath, newfile) 
                n+=1
                print("Cut", n)                        
pass

def resampleaudio(audio_path):
    n = 0
    for subdir, dirs, files in os.walk(audio_path):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith("_cut.wav"):
                tfn = sox.Transformer()
                tfn.rate(16000)
                remix_dictionary = {1:[1,2]}
                tfn.remix(remix_dictionary)
                tfn.build(filepath, filepath.replace('cut.wav', 'cutandresample.wav'))
                print("Resample ", n)

                             
                
pass



#writeinfotocsv(direc)
#copyaudiotonewfolder(direc, dest)
#copymiditonewfolder(direc, mididest)
#cutaudio(dest)
#resampleaudio(dest)
allinfo(audioloc, temp)





