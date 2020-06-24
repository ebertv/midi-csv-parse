import os
import py_midicsv
import shutil

direc = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0'
copyto = r'C:\Users\victo\Documents\Research\Datasets\maestro-v2.0.0\CSV'

def miditocsvconvert(directory):
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename 
            if filepath.endswith(".midi"):
                csv_string = py_midicsv.midi_to_csv(filepath)
                newfile = filepath.replace('.midi', '.csv')
                path = directory
                f = open(os.path.join(path, newfile), 'w+')
                for i in range(len(csv_string)):
                    f.write(csv_string[i])
pass

def copytonewdirectory(source, destination):
    for subdir, dirs, files in os.walk(source):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".csv"):
                shutil.copy(filepath, destination)


pass

#miditocsvconvert(direc)
#copytonewdirectory(direc, copyto)

