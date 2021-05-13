import csv
#import operator
import os
from collections import defaultdict
import glob

file_in = glob.glob("D:/Documents/Computer Science/Year 3/Final Project/data/**/*.csv", recursive=True)
#file_in = glob.glob("D:/Documents/Computer Science/Year 3/Final Project/data/test_output6_multi.csv", recursive=True)

num_of = 0
for files in file_in:
    f = open(files)
    csv_f = csv.reader(f)
    
    channelCount = max(csv_f, key=lambda row: row[0])[0]

    for row in csv_f:
        print(row)
    

    #sort = sorted(csv_f,key=lambda x: int(x[1]))

    for channel in range(int(channelCount)):
        print(channel+1)
        newDir = files[:-4] + str(channel) + ".csv"
    
        
        with open(newDir, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(['0', ' 0', ' Header', ' 1', ' 1', ' 480'])
            wr.writerow(['0', ' 0', ' Start_track'])
            wr.writerow(['0', ' 0', ' Program_c'])
            
            
            if (row[0] == str((channel+1))) and (row[0] == '1'):
                wr.writerow(row)
            elif (row[0] == str((channel+1))) and (row[0] != '1'):
                  row[0] = '1'
                  wr.writerow(row)

            wr.writerow(['0', ' 0', ' End_of_file'])
        num_of += 1
