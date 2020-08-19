import pandas as pd


dataset = pd.read_excel("Prelucrari date V6 27.04.2020.xlsx", sheet_name='SCP3 PM10')
db = []

for i in range(0, 180):
    for j in range(3, 27):
        print(j-3, dataset.iloc[i,j])
        db.append([j-3, dataset.iloc[i,j]])

print(db)




