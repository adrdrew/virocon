import csv

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import scipy.stats as sts
from mpl_toolkits.basemap import Basemap
from viroconcom.contours import IFormContour
from viroconcom.fitting import Fit


def get_data_coast():
    significant_wave_height = netCDF4.Dataset('cD-2_WAM-North_Sea_hs_1965.nc', 'r')
    wave_period = netCDF4.Dataset('cD-2_WAM-North_Sea_tm2_1965.nc', 'r')
    significant_wave_height_lons = significant_wave_height.variables['lon'][:]
    significant_wave_height_lats = significant_wave_height.variables['lat'][:]
    significant_wave_height_hs = significant_wave_height.variables['hs'][:]
    wave_period_lons = wave_period.variables['lon'][:]
    wave_period_lats = wave_period.variables['lat'][:]
    wave_period_tm2 = wave_period.variables['tm2'][:]
    hs_units = significant_wave_height.variables['hs'].units
    tm2_units = wave_period.variables['tms'].units
    significant_wave_height.close()
    wave_period.close()

    #significant wave height
    lon_0 = significant_wave_height_lons.mean()
    lat_0 = significant_wave_height_lats.mean()
    m_0 = Basemap(width=5000000, height=3500000, resolution='l', projection='stere', lat_ts=40, lat_0=lat_0, lon_0=lon_0)
    lon0, lat0 = np.meshgrid(significant_wave_height_lons, significant_wave_height_lats)
    xi, yi = m_0(lon0, lat0)
    cs = m_0.pcolor(xi, yi, np.squeeze(significant_wave_height_hs))
    # Add Grid Lines
    m_0.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
    m_0.drawmeridians(np.arange(-180., 181., 10.), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m_0.drawcoastlines()
    m_0.drawstates()
    m_0.drawcountries()

    # Add Colorbar
    cbar = m_0.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label(hs_units)

    plt.show()

    #wave period
    lon_1 = wave_period_lons.mean()
    lat_1 = wave_period_lats.mean()
    m_1 = Basemap(width=5000000, height=3500000, resolution='l', projection='stere', lat_ts=40, lat_0=lat_1, lon_0=lon_1)
    lon1, lat1 = np.meshgrid(wave_period_lons, wave_period_lats)
    xa, ya = m_1(lon1, lat1)


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