import csv
import sys
import numpy

sub=[]
file = open('csi_Empty_smooth.csv')
reader = csv.reader(file)
next(reader)
for row in reader:
    sub.append(row[1])
result=numpy.fft.fft(sub)
exp=abs(result**2)
fftsum=sum(exp)
print fftsum
file.close()