import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, maskoceans, interp, shapefile
from matplotlib.colors import from_levels_and_colors ;
import matplotlib.colors as mcolors
import netCDF4
import time
from datetime import datetime

#EDIT date and time for mapping product at desired date and time
#****************************************************************
date_check=datetime(2011,1,1,13,00)

ncfile=netCDF4.Dataset('G002_1d_20110101_20110105_gridT.nc','r')

#Reading the variables from data
#****************************************************
lat=ncfile.variables['nav_lat']
lon=ncfile.variables['nav_lon']
ssh=ncfile.variables['sossheig']
time = ncfile.variables['time_centered']


#Creating the date object from the start date of the Dataset
##################################################################


dates = netCDF4.num2date(time[:], time.units, time.calendar)
#dates

#Finding the data corresponding to date_check
#*****************************************************

count=0
try:
#  count = np.where(dates[:] == date_check)[0]
  lev = np.where(dates[:] == date_check)[0]
    count=lev.min()
except:
  print('error')
  exit()
#for i, date in enumerate(dates[:]):
#for i in range(0,5):
#    print (i)
#    if (date_check == dates[i]) :
#       count = i
#       print (count)
#       break
#    else :
#       print("The dates are not matcing")

#Mapping
##################

lt = np.amax(lat,axis=1)
#lats=lt.reshape(432,1)
ln = np.amax(lon,axis=0)
#lons=ln.reshape(780,1)
lt.shape
ln.shape
m=Basemap(projection='mill',llcrnrlat=lt.min(),urcrnrlat=lt.max(),llcrnrlon=ln.min(),urcrnrlon=ln.max(),resolution='f')
lon1, lat1 = np.meshgrid(ln, lt)
xi, yi = m(lon1, lat1)

nice_cmap=plt.get_cmap('RdYlGn')
clevs=np.arange(-.5,.5,.02)
cs = (m.contourf(xi,yi,ssh[count,:,:],clevs,cmap=nice_cmap,extended='both'))
m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(20.,31.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(47.,70.,5.), labels=[0,0,0,1])
m.fillcontinents(color='w',lake_color='aqua')               #Land Mask 'w' white
#m.fillcontinents(lake_color='aqua')               #Land Mask default Gray color
cbar = m.colorbar(cs, location='bottom', pad="10%")
plt.title('Model Output SSH Timestep-'+ str(date_check),fontsize=12,color='k');
cbar.set_label('meter');
plt.savefig('ssh.png', dpi=100);
plt.show()
