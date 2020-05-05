import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math

dates, values = [], []

time_list = [line.rstrip('\n') for line in open('time_file.txt')] #extract date/time data
data_list = [line.rstrip('\n') for line in open('data_file.txt')] #extract values data
type_list = [line.rstrip('\n') for line in open('type_file.txt')] #extract type data

PM10_time, PM10_data = [], []

for i in range(len(type_list)):
    if type_list[i] == "PM10":
        PM10_time.append(time_list[i])
        PM10_data.append(data_list[i])

l = []
i = 0
PM10 = []

while i < len(PM10_time):
    #print(HUM_time[i][9:14])  #selecting the hour
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
         12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    for h in hours:
        try:
            while PM10_time[i][9:11] == h:
                # print(type(HUM_data[i]))
                l.append(float(PM10_data[i]))
                i += 1
            medie = np.mean(l)
            nr_masuratori = len(l)
            element = []
            element.append(PM10_time[i][:9])
            # print(h)
            element.append(h)
            element.append(nr_masuratori)
            element.append(medie)
            PM10.append(element)
            l.clear()
        except:
            pass

X, y = [], []

for i in range(1, len(PM10)):
    X.append([PM10[i-1][1], PM10[i-1][3], PM10[i][1]])
    y.append(PM10[i][3])

# print(X)
# print(y)

print("X length: ", len(X))
print("y length: ", len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0)

print("x train length: ", len(X_train))
print("y train length: ", len(y_train))

print("x test length: ", len(X_test))
print("y test length: ", len(y_test))

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X_train, y_train)

# print(clf.predict([[2., 2.], [-1., -2.]]))