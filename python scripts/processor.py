import subprocess
import os
import csv
import sys
import re
import numpy
sums=0.0
def preprocess(sums,input_file,output_file1,output_file2):
	packets=[]
	std=[]
	subcarriers=[]
	for x in range(12,42):
		sub1 = []
		avg=[]
		file = open(input_file)
		reader = csv.reader(file)
 		next(reader)
		for row in reader:
			sub1.append(row[x])
		window = 300  #according to the data nearest value to 0.3s window is 300ms. hence setting window size to index of 311ms
		sub1_sums = 0.0
		sums=0.0
		for var in range(1, len(sub1)):
			sub1_sums = sub1_sums + float(sub1[var])
		data_avg = sub1_sums/(len(sub1)-1) #average of entire data
		for var in range(1, window):
			sums= sums + float(sub1[var])
		avg.append(sums/window)
		for var in range (window+1, len(sub1)):
			sums = sums - float(sub1[var-(window+1)])
			sums = sums + float(sub1[var])
			avg.append(sums/window)
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
	return std

def fftCalculate(output_file1):
	listr=[]
	for i in range(1,30):
		sub=[]
		file = open(output_file1)
		reader = csv.reader(file)
		next(reader)
		for row in reader:
		    sub.append(row[i])
		result=numpy.fft.fft(sub)
		exp=abs(result**2)
		fftsum=sum(exp)
		listr.append(fftsum)
		file.close()
	return listr


mainfile = open('final_file.txt','w')
mainfile.write("@RELATION CROWD_COUNTING\n\n")
mainfile.write("")
for r in range(1,30):
	mainfile.write("@ATTRIBUTE Subcarrier"+str(r)+"STD NUMERIC\n")
for r in range(1,30):
	mainfile.write("@ATTRIBUTE Subcarrier"+str(r)+"ME NUMERIC\n")
mainfile.write("\n@DATA\n")

subprocess.call(["gcc","my_read_bfee.c","-lm"])
for filename in os.listdir("/home/shreyans/Desktop/readings"):
	if filename.endswith(".dat"):
		tempstring=re.findall(r'\d+',filename)
		numofpeople = tempstring[0]
		input_file=os.path.splitext(filename)[0]+'.csv'
		result=subprocess.call(["./a.out",filename,input_file])
		output_file1=os.path.splitext(filename)[0]+'_smooth.csv'
		output_file2=os.path.splitext(filename)[0]+'_std.csv'
		res1= preprocess(sums,input_file,output_file1,output_file2)
		res2= fftCalculate(output_file1)
		mainfile.write(str(res1).replace("[","").replace("]","")+",")
		mainfile.write(str(res2).replace("[","").replace("]","")+",")
		mainfile.write(numofpeople+"\n")
		print result
