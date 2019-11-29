import csv
import random
import matplotlib.pyplot as plt

import numpy as np
import numpy.ma as ma
import scipy.stats as sts
import netCDF4
import xarray as xr
from viroconcom.contours import IFormContour
from viroconcom.fitting import Fit


def get_data_coast():
    significant_wave_height = netCDF4.Dataset('cD-2_WAM-North_Sea_hs_1966.nc', 'r')
    wave_period = netCDF4.Dataset('cD-2_WAM-North_Sea_tm2_1966.nc', 'r')
    #print(significant_wave_height.variables)
    #print(significant_wave_height.variables['lon'][:])

    lats = significant_wave_height.variables['lat'][:]
    lons = significant_wave_height.variables['lon'][:]
    lat_idx = np.abs(lats - 53).argmin()
    lon_idx = np.abs(lons - 14).argmin()
    wh = significant_wave_height.variables['hs'][:]
    wp = wave_period.variables['tm2'][:]

    print(wh)

def get_data_ndbc():
    datalist = []
    with open('SampleDataBuoy44009Year2000', 'r') as data:
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            datalist.append(row)

    datalist.pop(0)
    array1 = []
    array2 = []
    array0 = []
    for i in datalist:
        array0.append(float(i[0]))
        array1.append(float(i[1]))
        array2.append(float(i[2]))
    return array1, array2


def show_data(coast, coast2):

    fig1 = plt.figure()
    plt.plot(coast, coast2, '.k')
    plt.show()


# The dependency for the parameters must be given in the order shape, location, scale.
def fit(array1, array2):
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

    fig2 = plt.figure()
    plt.hist(array1, density=1)
    shape = my_fit.mul_var_dist.distributions[0].shape(0)
    loc = my_fit.mul_var_dist.distributions[0].loc(0)
    scale = my_fit.mul_var_dist.distributions[0].scale(0)
    x = np.linspace(0, 20, 100)
    f = sts.weibull_min.pdf(x, c=shape, loc=loc, scale=scale)
    plt.plot(x, f)
    plt.show()
    return my_fit, sea_state_sample


def show_contour(my_fit, sea_state_sample):
    c = IFormContour(my_fit.mul_var_dist, 50, 1, 50)
    fig3 = plt.figure()
    plt.plot(c.coordinates[0][0], c.coordinates[0][1])
    plt.plot(sea_state_sample[0], sea_state_sample[1], '.k')
    plt.show()


def random_numbers():
    list = []
    i = 0
    while i <= 1000:
        list.append(random.randint(0, 99))
        i= i+1
    print(list)
#random_numbers()
data0, data1 = get_data_coast()
#show_data(data0, data1)
#my_fit, sea_state_sample = fit(data0, data1)
#show_contour(my_fit, sea_state_sample)

