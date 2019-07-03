import numpy as  np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

time_list = [line.rstrip('\n') for line in open('time_file.txt')] #extract date/time data
data_list = [line.rstrip('\n') for line in open('data_file.txt')] #extract values data
type_list = [line.rstrip('\n') for line in open('type_file.txt')] #extract type data

#creating 2 lists for each parameter with time and data/values
PM10_time = []
PM10_data = []

#sorting the data and put every date in the specific list
for i in range(len(type_list)):
    if type_list[i] == "PM10":
        PM10_time.append(time_list[i])
        PM10_data.append(data_list[i])

for i in range(len(PM10_time)):
    print(PM10_time[i])


start = 0
stop = 0
#print(len(PM10))
PM10 = []
'''
for i in range(1, len(PM10_time)):
    #print(PM10[i])
    if PM10_time[i] == PM10_time[i-1] and PM10_time[i-1][9:11] is '23':
        PM10.insert(i+23, PM10[i-1])
        PM10.remove(PM10[i-1])
print(len(PM10))
'''
for i in range(len(PM10_time)):
    #print(PM10[i])
    if PM10_time[i] == '28-10-18 ':
        start = i
    elif PM10_time[i] == "02-11-18 ":
        stop = i

x_data, y_data, x_data_days_hours = [],[],[]



for i in range(start+1, start+25):
    #print(PM10[i])
    x_data.append(i)
    y_data.append(PM10_data[i])
    x_data_days_hours.append(PM10_time[i] + " " + PM10_time[i])

print(x_data)
print(y_data)
