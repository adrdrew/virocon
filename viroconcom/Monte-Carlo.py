import csv

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import scipy.stats as sts
import matplotlib.patches as mpatches
import xarray as xr
from viroconcom.contours import IFormContour
from viroconcom.fitting import Fit


def get_data_coast():
    significant_wave_height = xr.open_dataset('cD-2_WAM-North_Sea_hs_1965.nc')
    wave_period = xr.open_dataset('cD-2_WAM-North_Sea_tm2_1965.nc')
    print(significant_wave_height)
    print(wave_period)

    #daily_data_swh = significant_wave_height.groupby('time.hour').mean('time')
    #daily_data_wp = wave_period.groupby('time.hour').mean('time')

    swh = significant_wave_height.sel(lon=14, lat=40, method='nearest')
    wp = wave_period.sel(lon=21, lat=12, method='nearest')
    s = swh.to_dataframe()
    w = wp.to_dataframe()
    print(w)


    #plt.plot(swh['hs'].data, wp['tm2'].data, 'k.')
    #plt.show()
    #swh['hs'].plot.line('o-', color='blue', figsize=(15,10))
    #plt.ylim((-0.5, 10))
    #plt.show()

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
    print(coast)
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


#data0, data1 = get_data_ndbc()
#show_data(data0, data1)
#my_fit, sea_state_sample = fit(data0, data1)
#show_contour(my_fit, sea_state_sample)

get_data_coast()