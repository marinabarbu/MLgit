import numpy as np
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
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11',
         '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
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
            element.append(h)
            element.append(nr_masuratori)
            element.append(medie)
            PM10.append(element)
            l.clear()
        except:
            pass

X, y = [], []

for i in range(len(PM10)):
    X.append(i)
    y.append(PM10[i][3])

y_data = y
y = [ '%.2f' % elem for elem in y_data ]

X = np.array([X]).T
y = np.array(y).ravel()
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

y_test = [float(e) for e in y_test]
svr_rbf = SVR(kernel= 'rbf', C= 1e2, gamma= 0.1).fit(X_train, y_train)
y_pred = svr_rbf.predict(X_test)

y_pred = [ '%.2f' % elem for elem in y_pred]
y_pred = [float(e) for e in y_pred]

for i in range(len(y_test)):
    print(y_test[i], y_pred[i])
print()

corr_coef = np.corrcoef(y_test, y_pred)[0,1]
print("accuracy: ",corr_coef)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:",mse)

rmse = math.sqrt(mse)
print("Root Mean Squared Error:", rmse)

svr_for_graph = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1).fit(X, y)
y_pred_for_graph = svr_for_graph.predict(X)

plt.show()
y = [float(i) for i in y]
plt.scatter(X,y, color='black', label='real data')
plt.plot(X, y_pred_for_graph, color='red', lw=3, label="RBF model")
plt.ylim(bottom=0)
plt.ylim(top=150)
plt.xlabel('data')
plt.ylabel('grad de poluare PM10')
plt.legend()
plt.show()