import csv
import sys
import numpy
std=[]
packets = []
subcarriers = []
sum=0.0

def preprocess(sum,input_file,output_file1,output_file2):
    for x in range(12,42):
        sub1 = []
        avg=[]
        
        file = open(input_file)
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            sub1.append(row[x])
        window = 300  #according to the data nearest value to 0.3s window is 300ms. hence setting window size to index of 311ms
        sub1_sum = 0.0
        sum=0.0
        for var in range(1, len(sub1)):
            sub1_sum = sub1_sum + float(sub1[var])
        data_avg = sub1_sum/(len(sub1)-1) #average of entire data
        for var in range(1, window):
            sum= sum + float(sub1[var])
        avg.append(sum/window)
        for var in range (window+1, len(sub1)):
            sum = sum - float(sub1[var-(window+1)])
            sum = sum + float(sub1[var])
            avg.append(sum/window)
        std.append(numpy.std(avg))
        subcarriers.append(avg)
        file.close()
    file = open(input_file)
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        packets.append(row[1])
    file.close()
    example=csv.writer(open(output_file1, 'wb'), delimiter=',')
    example.writerow(["packet#" , "subcarrier1", "subcarrier2", "subcarrier3", "subcarrier4", "subcarrier5", "subcarrier6", "subcarrier7", "subcarrier8", "subcarrier9", "subcarrier10", "subcarrier11", "subcarrier12", "subcarrier13", "subcarrier14", "subcarrier15", "subcarrier16", "subcarrier17", "subcarrier18", "subcarrier19", "subcarrier20", "subcarrier21", "subcarrier22", "subcarrier23", "subcarrier24", "subcarrier25", "subcarrier26", "subcarrier27", "subcarrier28", "subcarrier29", "subcarrier30"])
    for  i in range(len(subcarriers[0])):
        example.writerow([packets[i],subcarriers[0][i],subcarriers[1][i],subcarriers[2][i],subcarriers[3][i],subcarriers[4][i],subcarriers[5][i],subcarriers[6][i],subcarriers[7][i],subcarriers[8][i],subcarriers[9][i],subcarriers[10][i],subcarriers[11][i],subcarriers[12][i],subcarriers[13][i],subcarriers[14][i],subcarriers[15][i],subcarriers[16][i],subcarriers[17][i],subcarriers[18][i],subcarriers[19][i],subcarriers[20][i],subcarriers[21][i],subcarriers[22][i],subcarriers[23][i],subcarriers[24][i],subcarriers[25][i],subcarriers[26][i],subcarriers[27][i],subcarriers[28][i],subcarriers[29][i]])
    example=csv.writer(open(output_file2, 'wb'), delimiter=',')
    for r in range(len(std)):
        example.writerow([r+1,std[r]])
preprocess(sum,"csi_Empty.csv","csi_Empty_SOMMMMMMTH.csv","csi+STDSTD.csv")