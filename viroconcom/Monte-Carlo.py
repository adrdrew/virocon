
import csv
import matplotlib.pyplot as plt
from viroconcom.fitting import Fit
from viroconcom.contours import IFormContour
import  scipy.stats as sts
import numpy as np


dataList = []

with open('SampleDataBuoy44009Year2000', 'r') as data:
    reader = csv.reader(data, delimiter=',')
    for row in reader:
        dataList.append(row)

dataList.pop(0)
array1 = []
array2 = []
array0 = []
for i in dataList:
    array0.append(float(i[0]))
    array1.append(float(i[1]))
    array2.append(float(i[2]))

print(array0)
fig1 = plt.figure()
plt.plot(array1, array2, '.k')
plt.show()

# The dependency for
# the parameters must be given in the order shape, location, scale.
dist_description_1 = {'name': 'Weibull_3p',
                      'dependency': (None, None, None),
                      'width_of_intervals': 1}
dist_description_2 = {'name': 'Lognormal',
                      'dependency': (0, None, 0),
                      'functions': ('exp3', None, 'power3')}
dist_structure = (dist_description_1, dist_description_2)

sea_state_sample = (array1, array2)

my_fit = Fit(sea_state_sample, dist_structure)
print(my_fit.mul_var_dist.distributions[0].name)
print('Shape: ' + str(my_fit.mul_var_dist.distributions[0].shape))
print('Location: ' + str(my_fit.mul_var_dist.distributions[0].loc))
print('Scale: ' + str(my_fit.mul_var_dist.distributions[0].scale))
print(my_fit.mul_var_dist.distributions[1])
print(my_fit.mul_var_dist.latex_repr(['Hs', 'T']))

fig2=plt.figure()
plt.hist(array1, density=1)
shape = my_fit.mul_var_dist.distributions[0].shape(0)
loc = my_fit.mul_var_dist.distributions[0].loc(0)
scale = my_fit.mul_var_dist.distributions[0].scale(0)
x = np.linspace(0, 20, 100)
f = sts.weibull_min.pdf(x, c=shape, loc=loc, scale=scale)
plt.plot(x, f)
plt.show()

c = IFormContour(my_fit.mul_var_dist, 50, 1, 50)
fig3 = plt.figure()
plt.plot(c.coordinates[0][0], c.coordinates[0][1])
plt.plot(sea_state_sample[0], sea_state_sample[1], '.k')
plt.show()
