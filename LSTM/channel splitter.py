import csv

#Creates empty set - this will be used to store the values that have already been used
for i in range(40):
    filelist = set()

    directory = 'C:/Users/willb/Documents/Computer Science/Year3/Final Project/polyphonictomono/data/test_output' + str(i) + '_multi' 

    #Opens the large csv file in "read" mode
    with open(directory + '.csv', 'r') as csvfile:

        #Read the first row of the large file and store the whole row as a string (headerstring)
        read_rows = csv.reader(csvfile)
        headerrow = next(read_rows)
        headerstring=','.join(headerrow)
        

        for row in read_rows:

            
            #Store the whole row as a string (rowstring)
            rowstring=','.join(row)

            #Defines filename as the first entry in the row - This could be made dynamic so that the user inputs a column name to use
            filename = (row[0])

            #This basically makes sure it is not looking at the header row.
            if filename != "0":

                #If the filename is not in the filelist set, add it to the list and create new csv file with header row.
                if filename not in filelist:    
                    filelist.add(filename)
                    with open(directory +str(filename)+'.csv','a') as f:
                        strrow1 = ['0',' 0',' Header',' 1',' 1',' 1024']
                        str1 = ','.join(strrow1)
                        strrow2 = [filename,' 0',' Start_track']
                        str2 = ','.join(strrow2)
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")
                        #f.write([filename,' 0',' Start_track'])
                        f.close()   
                #If the filename is in the filelist set, append the current row to the existing csv file.     
                else:
                    with open(directory +str(filename)+'.csv','a') as f:
                        f.write(rowstring)
                        f.write("\n")
                        f.close()

    with open(directory + '1.csv','a') as g:
        strrowi = ['0',' 0',' End_of_file']
        stri = ','.join(strrowi)
        g.write(stri)
        g.close()

    with open(directory + '2.csv','a') as h:
        strrowo = ['0',' 0',' End_of_file']
        stro = ','.join(strrowo)
        h.write(stro)
        h.close()

    '''import csv

    with open('D:/Documents/Computer Science/Year 3/Final Project/data/test_output6_multi.csv') as fin:    
        csvin = csv.DictReader(fin)
        
        # Category -> open file lookup
        outputs = {}
        for row in csvin:
            
            cat = row['0']
            # Open a new file and write the header
            if cat not in outputs:
                fout = open('{}.csv'.format(cat), 'w', newline="")
                dw = csv.DictWriter(fout, fieldnames=csvin.fieldnames)
                dw.writeheader()
                outputs[cat] = fout, dw
            # Always write the row
            outputs[cat][1].writerow(row)
        # Close all the files
        for fout, _ in outputs.values():
            fout.close()'''
