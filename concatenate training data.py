directory = "D:/Documents/Computer Science/Year 3/Final Project/MIDI files/small td/"
noOfFiles = 70
filenames = []
for files in range(noOfFiles):
    filename = directory + str(files) + ".txt"
    filenames.append(filename)
number = 0
with open("D:/Documents/Computer Science/Year 3/Final Project/MIDI files/concatenated/half.txt", "w", encoding ="utf-8") as outfile:
    for fname in filenames:
        with open(fname, encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)
        print("Added file number " + str(number))
        number += 1
                
