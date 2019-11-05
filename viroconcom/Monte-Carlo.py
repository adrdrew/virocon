
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
print(array)


#
#
#
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt
#xmin, xmax, ymin, ymax = 0, 20, 0, 20
#plt.axis([xmin, xmax, ymin, ymax])
plt.plot(array1, array2, ',')
plt.xticks(np.arange(0, 100, 10))
plt.yticks(np.arange(0, 100, 10))
plt.show()