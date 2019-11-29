
# data: WSPD APD
#       xyz  xyz
#       ...  ...
# WSPD: WindSpeed
# WVHT: significantWaveHight
# APD: wavePeriode
#
# Hier erstmal nach dem Paper von elsevier Ocean Engineering
#
# Variablen:
# Tz = wavePeriod
# Hs = significantWaveHeight


#
# Daten aufbereiten.
#

import csv
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


def _plot_data():
    data_list = []
    with open('SampleDataBuoy44009Year2000', 'r') as data:
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            data_list.append(row)
    data_list.pop(0)
    for i in data_list:
        i.pop(1)
    data_list.pop(0)
    array = []
    array1 = []
    array2 = []
    for i in data_list:
        array1.append(i[0])
        array2.append(i[1])
    array.append(array1)
    array.append(array2)

    # print(array1)
    for i in data_list:
        i[0] = float(i[0])
        i[1] = float(i[1])
    print(data_list)

    # Array1 sortieren
    array1 = sorted(array1)

    # Durchschnitt
    a = 0.0
    for i in array1:
        a = a+float(i)
    mean = a/len(array1)
    print(mean)

    # Varianz
    b = 0.0
    for i in array1:
        b = b + ((float(i)-mean)*(float(i)-mean))
    var = b/(len(array1)-1)
    print(var)

    # Standartabweichung
    s = math.sqrt(var)
    print(s)

    # PlotData
    df = pd.DataFrame(data_list, columns=["x", "y"])
    sns.jointplot(x='x', y='y', data=df)
    plt.show()



# omega = scale
# mu = location
def _normal_density_function(x, omega, mu):
    return (1 / math.sqrt(2 * math.pi * omega ** 2)) * math.exp((-(x - mu) ** 2) / (2 * omega ** 2))

# math.exp(mu) = scale
# omega = shape
def _lognormal_density_function(x, omega, mu):
    return (1 / (x * omega * math.sqrt(2 * math.pi))) * math.exp((-(math.log10(x) - mu) ** 2) / (2 * omega ** 2))

# a = scale
# b = shape
# c = location
def _weibull_density_function(a, b, c):
    x = 1
    list = []
    list1 = []
    list2 = []
    if x >= c:
        while x <= 10:

            list1.append(x)
            list2.append((b / a) * (((x - c) / a) ** (b - 1)) * math.exp(-((x - c) / a) ** b))

            x = x+0.001

        list.append(list1)
        list.append(list2)
        return list
    else:
        raise Exception('x must be greater or equal to c')


print(_normal_density_function(1, 1.25, 2))
print(_lognormal_density_function(1, 1.25, 2))
print(_weibull_density_function(1.25, 2, 0.125))

plt.plot(_weibull_density_function(2.776, 1.471, 0.8888), 'ro')
plt.show()