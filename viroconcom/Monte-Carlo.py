
#data: WSPD APD
#      xyz  xyz
#      ...  ...
#WSPD: WindSpeed
#WVHT: significantWaveHight
#APD: wavePeriode
#
# Hier erstmal nach dem Paper von elsevier Ocean Engineering
#
#Variablen:
#Tz = wavePeriod
#Hs = significantWaveHeight


#
#Daten aufbereiten.
#

import csv
dataList = []

with open('SampleDataBuoy44009Year2000', 'r') as data:
    reader = csv.reader(data, delimiter=',')
    for row in reader:
        dataList.append(row)
dataList.pop(0)
for i in dataList:
    i.pop(1)
dataList.pop(0)
array = []
array1 = []
array2 = []
for i in dataList:
    array1.append(i[0])
    array2.append(i[1])
array.append(array1)
array.append(array2)
#print(array1)
for i in dataList:
    i[0] = float(i[0])
    i[1] = float(i[1])
print(dataList)
#Array1 sortieren
array1 = sorted(array1)
#print(array1)
#
#Durchschnitt

a = 0.0
for i in array1:
    a = a+float(i)
mean = a/len(array1)
print(mean)

#Varianz
b = 0.0
for i in array1:
    b = b + ((float(i)-mean)*(float(i)-mean))
var = b/(len(array1)-1)
print(var)

#Standartabweichung
import math
s = math.sqrt(var)
print(s)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


df = pd.DataFrame(dataList, columns=["x", "y"])
sns.jointplot(x='x', y='y', data=df)
plt.show()