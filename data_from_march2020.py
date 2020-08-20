import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import torch
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPClassifier

# dataset = pd.read_excel("Prelucrari date V6 27.04.2020.xlsx", sheet_name='SCP3 PM10')
# db = []
#
# for i in range(0, 180):
#     for j in range(3, 27):
#         # print(j-3, dataset.iloc[i,j])
#         db.append([float(j-3), float(round(dataset.iloc[i,j]))])

# print(db)

# X, y = [], []
# for i in range(1, len(db)):
#     X.append([db[i-1][0], db[i-1][1], db[i][0]])
#     y.append(db[i][1])

# print(X)
# print(y)

# with open('X_1y', 'wb') as f:
#     pickle.dump(X, f)
#
# with open('y_1y', 'wb') as f:
#     pickle.dump(y, f)

with open("large_X", 'rb') as f:
    X = pickle.load(f)

with open("large_y", 'rb') as f:
    y = pickle.load(f)

clf = MLPClassifier()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

print(X_train)
print(X_test)
print(y_test)
print(y_train)
# print(y)
clf.fit(X_train, y_train)

y_pred = []

for i in range(len(X_test)):
    pred = clf.predict([X_test[i]])
    # print(pred[0], y_test[i])
    y_pred.append(pred[0])

print()

corr_coef = np.corrcoef(y_test, y_pred)[0,1]
print("corelatia : ",corr_coef)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)



