import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, addcyclic
import netCDF4
from netCDF4 import Dataset
import matplotlib.colors as mcolors
import sys
import time
from sys import argv
from datetime import datetime

#---------------------------------------------------------------------------------------------------------------------
## This code selects the NEMO forecast outputs and generates the maps of temperature,salinity, sealevel or current

# Python command line to run this programme withi input arguments is given below

##python python.py netcdf.nc yyyy mm dd hh ss depth variable

#example:-
#python plot_temp_salinity_Arg_file.py G002_1d_20110101_20110105_gridT.nc 2011 1 2 12 0 3.7658734 temperature
#python plot_temp_salinity_Arg_file.py G002_1d_20110101_20110105_gridT.nc 2011 1 2 12 0 3.7658734 salinity

#ncfile=Dataset('G002_1d_20110101_20110105_gridT.nc','r')
#ufile=Dataset('G002_1d_20110101_20110105_gridU.nc','r')
#vfile=Dataset('G002_1d_20110101_20110105_gridV.nc','r')
#---------------------------------------------------------------------------------------------------------------------

file=sys.argv[1]   # input file name

file=file[:-8]   #select common part of the file name for all the files generated uv an T

#Select and load all the crresponding data files
ncfile=Dataset(file+'gridT.nc')
ufile=Dataset(file+'gridU.nc')
vfile=Dataset(file+'gridV.nc')

# The input arguments from 4th to 6th are year, month, day, hour and seconds (the date to be plotted

date_check=datetime(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
depthlev=float(sys.argv[7])     #depth at which the temp sal or current is plotted - input as 7th argument
#var='temperature'
var=sys.argv[8]  # variable to be plotted temperature,salinity, sealevel or current- input as 8th Argument
print(var)


#read the variables from files and set the colorbar levels and unit of the variable for the plots
if (var=='temperature'): 
   ss='votemper'
   unit=' Deg.C'
   clevs=np.arange(20,32,1)
   plotvar=ncfile.variables[ss]
elif (var=='salinity'):
     ss='vosaline'
     unit=' PSU'
     clevs=np.arange(34,44,1)
     plotvar=ncfile.variables[ss]
elif (var=='sealevel'):   
     ss='sossheig'
     unit=' meter'
     clevs=np.arange(-.5,.5,.02)
     ssh=ncfile.variables['sossheig']
elif (var=='current'):
     unit=' m/sec'
     u=ufile.variables['vozocrtx']
     v=vfile.variables['vomecrty']
#UV to cntre
     uc=0.5*(u[:,:,:-1,:-1]+u[:,:,:-1,1:])
     vc=0.5*(v[:,:,:-1,:-1]+v[:,:,1:,:-1])
     
   

lat=ncfile.variables['nav_lat']
lon=ncfile.variables['nav_lon']
lt=np.amax(lat,axis=1)
ln=np.amax(lon,axis=0)
depth=ufile.variables['depthu']
#plotvar=ncfile.variables[ss]
#temperature=ncfile.variables['votemper']
#salinity=ncfile.variables['vosaline']

time = ncfile.variables['time_centered']

#Creating the date object from the start date of the Dataset
##################################################################


dates = netCDF4.num2date(time[:], time.units, time.calendar)


try:
#  count = np.where(dates[:] == date_check)[0]
  days = np.where(dates[:] == date_check)[0]
  day=days[0]
except:
  print('error -Time Mismatch')
  exit()

#depthlev- Select the depth level to be plotted (temp., sal. and currents)
depth[0]
try:
#  deep = np.where(depth[:] == depthlev)[0]
  deep = np.where(np.around(depth[:]) == round(depthlev))[0]
  lev=deep[0]
except:
  print('No Data available at specified depth')
  exit()


#lt_uc =lt[0:ny]
lt_uc =lt[:-1]
#ln_uc =ln[0:nx]
ln_uc =ln[:-1]

m=Basemap(projection='cyl',llcrnrlat=lt_uc.min(),urcrnrlat=lt_uc.max(),llcrnrlon=ln_uc.min(),urcrnrlon=ln_uc.max(),resolution='h')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='w',lake_color='aqua')               #Land Mask 'w' white
m.drawparallels(np.arange(20.,31.,5.), labels=[1,0,0,0],linewidth=0.0)
m.drawmeridians(np.arange(47.,70.,5.), labels=[0,0,0,1],linewidth=0.0)

lons,lats=np.meshgrid(ln_uc,lt_uc)
X4,Y4=m(lons,lats)

nice_cmap=plt.get_cmap('RdYlGn')
#nice_cmap=plt.get_cmap('gist_rainbow')
#clevs=np.arange(-.5,.5,.02)

if (var=='sealevel'):
#   cs = (m.contourf(X4,Y4,ssh[day,:-1,:-1],clevs,cmap=nice_cmap,extend='both'))
   cs = (m.contourf(X4,Y4,ssh[day,:-1,:-1],clevs,cmap=nice_cmap,extend='both'))
elif (var=='temperature' or var=='salinity'):
   cs = (m.contourf(X4,Y4,plotvar[day,lev,:-1,:-1],clevs,cmap=nice_cmap,extend='both'))
elif (var=='current'):
     x=X4[::10,::10]    #skip xlength=10
     y=Y4[::10,::10]    #yskip=10
     varU=uc[day,lev,::10,::10]
     varV=vc[day,lev,::10,::10]
     speed=np.sqrt(varV*varV + varU*varU)
     vmax=speed.max()
     yy=np.arange(0,len(lt_uc),10)
     xx=np.arange(0,len(ln_uc),10)
     points=np.meshgrid(yy,xx)
     skiplen=x[0,1]-x[0,0]
     cs = m.quiver(x,y,varU,varV,speed,width=0.003,scale_units = 'x',scale =(.2/skiplen)*vmax,headlength=7)
     qk = plt.quiverkey(cs, 0.8, 0.8, .4, '0.4 m/s', labelpos='E')
   

cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(str(var)+'-'+ str(unit),fontsize=12,fontweight='bold',color='k');
plt.title('Date: '+ str(date_check),fontsize=12,color='k',fontweight='bold');
#cbar.set_label(str(var)+'(Deg.C)',fontsize=12,color='k');

plt.show()
