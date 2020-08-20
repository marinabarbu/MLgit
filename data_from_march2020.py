import pandas as pd
import pickle


dataset = pd.read_excel("Prelucrari date V6 27.04.2020.xlsx", sheet_name='SCP3 PM10')
db = []

for i in range(0, 180):
    for j in range(3, 27):
        # print(j-3, dataset.iloc[i,j])
        db.append([float(j-3), float(round(dataset.iloc[i,j]))])

print(db)

X, y = [], []
for i in range(1, len(db)):
    X.append([db[i-1][0], db[i-1][1], db[i][0]])
    y.append(db[i][1])

print(X)
print(y)

with open('X_1y', 'wb') as f:
    pickle.dump(X, f)

with open('y_1y', 'wb') as f:
    pickle.dump(y, f)

with open("X_values_serie_mare", 'rb') as f:
    X = pickle.load(f)

with open("y_values_serie_mare", 'rb') as f:
    y = pickle.load(f)

print(X)
print(y)



