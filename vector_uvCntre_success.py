import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, addcyclic
from netCDF4 import Dataset
import matplotlib.colors as mcolors

ncfile=Dataset('G002_1d_20110101_20110105_gridT.nc','r')
ufile=Dataset('G002_1d_20110101_20110105_gridU.nc','r')
vfile=Dataset('G002_1d_20110101_20110105_gridV.nc','r')



lat=ncfile.variables['nav_lat']
lon=ncfile.variables['nav_lon']

lt=np.amax(lat,axis=1)
ln=np.amax(lon,axis=0)

u=ufile.variables['vozocrtx']
v=vfile.variables['vomecrty']

t,d,nyy,nxx=u.shape
nx=nxx-1
ny=nyy-1
print(nx,ny)

#UV to centre
uc=0.5*(u[:,:,0:ny,0:nx]+u[:,:,0:ny,1:nx+1])
vc=0.5*(v[:,:,0:ny,0:nx]+v[:,:,1:ny+1,0:nx])

lt_uc =lt[0:ny]
ln_uc =ln[0:nx]

#m=Basemap(projection='cyl',llcrnrlat=lt.min(),urcrnrlat=lt.max(),llcrnrlon=ln.min(),urcrnrlon=ln.max(),resolution='h')
m=Basemap(projection='cyl',llcrnrlat=lt_uc.min(),urcrnrlat=lt_uc.max(),llcrnrlon=ln_uc.min(),urcrnrlon=ln_uc.max(),resolution='h')

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='w',lake_color='aqua')               #Land Mask 'w' white
m.drawparallels(np.arange(20.,31.,5.), labels=[1,0,0,0],linewidth=0.0)
m.drawmeridians(np.arange(47.,70.,5.), labels=[0,0,0,1],linewidth=0.0)

#lons,lats=np.meshgrid(ln,lt)
lons,lats=np.meshgrid(ln_uc,lt_uc)

X4,Y4=m(lons,lats)
#varU=u[0,0,:,:]
#varV=v[0,0,:,:]
varU=uc[0,0,:,:]
varV=vc[0,0,:,:]
speed=np.sqrt(varU*varU+varV*varV)

#yy=np.arange(0,len(lt),12)
#xx=np.arange(0,len(ln),14)
yy=np.arange(0,len(lt_uc),10)  #skip 10 lines in y
xx=np.arange(0,len(ln_uc),10)  #skip 10 lines in y
#print(yy,xx)
points=np.meshgrid(yy,xx)

cmap=plt.get_cmap('RdYlGn')

#cs = m.quiver(X4[points],Y4[points],varU[points],varV[points],speed[points],cmap=cmap,latlon=True)
#cs = m.quiver(X4[points],Y4[points],varU[points],varV[points],speed[points],latlon=True,color='g')
##cs = m.quiver(X4[points],Y4[points],varU[points],varV[points])
cs = m.quiver(X4[points],Y4[points],varU[points],varV[points],headlength=6)
#cs = m.quiver(X4,Y4,varU,varV)
#qk = plt.quiverkey(cs, 0.2, -0.2, .4, '0.4 m/s', labelpos='W')
qk = plt.quiverkey(cs, 0.8, 0.8, .4, '0.4 m/s', labelpos='E')
#cbar = m.colorbar(cs, location='bottom', pad="10%")
#plt.title('Timestep-'+ str(date_check),fontsize=12,color='k');
#cbar.set_label('Ocean Currents (meter/sec)');
plt.show()
