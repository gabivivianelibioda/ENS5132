# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 20:32:57 2025

@author: gabri
"""

import xarray as xr
import rioxarray as rio
import rasterio
from shapely.geometry import mapping
import numpy as np
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from mpl_toolkits.basemap import Basemap
import regionmask

project = 'C:/ENS5132/ENS5132/Projeto03/'
path = 'C:/ENS5132/ENS5132/Projeto03/Input3/'
pathnetCDF = 'C:/ENS5132/ENS5132/Projeto03/Input3/GLDAS/'
pathout = 'C:/ENS5132/ENS5132/Projeto03/Output3/'
lista = os.listdir(path)
listanetCDF = os.listdir(pathnetCDF)

read = xr.open_dataset(pathnetCDF + 'GLDAS_CLSM10_M.A202502.021.nc4')
print(read.variables.keys())
dataset = read.to_dataframe()
dados = read.rio.set_spatial_dims(x_dim = 'lon', y_dim = 'lat', inplace=True)
read.dims
read.data_vars
read.lat
read.lon

lon = read.variables['lon'][:]
lat = read.variables['lat'][:]
times = read.variables['time_bnds'][:] 

irr =  read.variables['TVeg_tavg'][:]
data_variable = read['TVeg_tavg']
unitp = data_variable.units

irr

x = read.variables['TVeg_tavg'][0,0,:]
x
y = read.variables['TVeg_tavg'][0,:,0]
y

data_variable.plot()
plt.title('Irradiação - Fev/2025')
plt.show()


#world
fig = plt.figure(figsize=(15,5))
mapa = Basemap(projection ='mill', llcrnrlat = -50,
               urcrnrlat = 50, llcrnrlon = -180,
               urcrnrlon = 180)
mapa.drawcoastlines()
mapa.drawstates()
mapa.drawcountries()
mapa.drawlsmask(land_color='moccasin',ocean_color='blue')
mapa.drawcounties()
lons,lats = np.meshgrid(lon,lat)
x,y = mapa(lons,lats)
parallels = np.arange(-90,90,20.)
mapa.drawparallels(parallels,labels = [1,0,0,0], fontsize = 10)
meridians = np.arange(-180.,180.,40.)
mapa.drawmeridians(meridians, labels=[0,0,0,1], fontsize = 10)
var  = mapa.contourf(x,y,irr[0,:,:])
cb = mapa.colorbar(var, 'bottom', size = '8%', pad = '10%')
plt.title('Irradiação - Fev/2025', fontsize=12)
cb.set_label('Irradiação({})'.format(unitp))
plt.show()



#Zoom no país:
fig = plt.figure(figsize=(5,10))
mapa = Basemap(projection ='mill', llcrnrlat = -40,
               urcrnrlat = 10, llcrnrlon = -80,
               urcrnrlon = -30)
mapa.drawcoastlines()
mapa.drawstates()
mapa.drawcountries()
mapa.drawlsmask(land_color='moccasin',ocean_color='blue')
mapa.drawcounties()
lons,lats = np.meshgrid(lon,lat)
x,y = mapa(lons,lats)
parallels = np.arange(-90,90,10.)
mapa.drawparallels(parallels,labels = [1,0,0,0], fontsize = 10)
meridians = np.arange(180.,360.,10.)
mapa.drawmeridians(meridians, labels=[0,0,0,1], fontsize = 10)
var  = mapa.contourf(x,y,irr[0,:,:])
cb = mapa.colorbar(var, 'bottom', size = '5%', pad = '10%')
plt.title('Irradiação - Fev/2025')
cb.set_label('Irradiação({})'.format(unitp))
plt.show()


#corte (clip) with a shapefile

#plot do shape
Brasil = gpd.read_file(path + 'shapes/BR_Regioes_2024/BR_Regioes_2024.shp')
print(Brasil.crs)
Brasil



my_list = list(Brasil['NM_REGIA'])
indexes = [my_list.index(x) for x in my_list]

#mask
Brasil_mask_poly = regionmask.Regions(name='NM_REGIA', numbers = indexes, 
                                      names = Brasil.NM_REGIA[indexes], abbrevs= Brasil.NM_REGIA[indexes], 
                                      outlines = list(Brasil.geometry.values[i] for i in range(0,Brasil.shape[0])))

Brasil_mask_poly
#mask = regionmask.defined_regions.srex.mask_3D(lons,lats)


#teste
print('{}'.format(Brasil_mask_poly.names[0]))
mask = Brasil_mask_poly.mask(read.isel(time=0))
mask
mask.to_netcdf(pathout + 'mask_by_Brasil3.nc')
readmask = xr.open_dataset(pathout + 'mask_by_Brasil3.nc')
dataframe = readmask.to_dataframe()
masked_shape = read.where(mask!='nan')
masked_shape

#Extractin data series with Brasil map
read = xr.open_dataset('C:/ENS5132/ENS5132/Projeto03/Input3/GLDAS/GLDAS_CLSM10_M.A202502.021.nc4')
read.rio.write_crs('epsg:4674', inplace = True)
read['TVeg_tavg'].rio.to_raster('C:/ENS5132/ENS5132/Projeto03/Output3/test32025.tif')
Brasil = gpd.read_file(path + 'shapes/BR_Regioes_2024/BR_Regioes_2024.shp')
with rasterio.open('C:/ENS5132/ENS5132/Projeto03/Output3/test32025.tif') as src:
    Brasil=Brasil.to_crs(src.crs)
    out_image, out_transform = rasterio.mask.mask(src, Brasil.geometry, crop = True)
    out_meta = src.meta.copy()
out_meta.update({'driver':'Gtiff',
                 'height':out_image.shape[1], 'width':out_image.shape[2], 'transform': out_transform})
with rasterio.open('C:/ENS5132/ENS5132/Projeto03/Output3/clipped32025.tif', 'w', **out_meta) as dst:
    dst.write(out_image)


#Apenas um test para ver o raster:
regioes = gpd.read_file(path + 'shapes/BR_Regioes_2024/BR_Regioes_2024.shp', masked=True).squeeze()
clipped = rio.open_rasterio(pathout + 'clipped32025.tif', masked=True).squeeze()
f,ax=plt.subplots()
clipped.plot(ax=ax, cbar_kwargs = {'orientation':'vertical', 'shrink': 0.8, 'label':'Irradiância (W/m2)'})
ax.set_title('Irradiância - Fev/2025')
ax.set_xlabel('Longitude', fontsize = 10)
ax.set_ylabel('Latitude', fontsize = 10)
clipped.plot.imshow(Brasil)


#Mapa
f,ax=plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
clipped = rio.open_rasterio(pathout + 'clipped32025.tif', masked=True).squeeze()
regioes = gpd.read_file(path + 'shapes/BR_Regioes_2024/BR_Regioes_2024.shp', masked=True).squeeze()
plt.grid(True, color = 'gray', linestyle = '--', linewidth=0.6)
clipped.plot(ax=ax, cbar_kwargs = {'orientation':'vertical', 'shrink': 0.8, 'label':'Irradiância (W/m.m)'})
regioes.plot(ax=ax, facecolor='none', edgecolor='black')
plt.grid(True, color = 'gray', linestyle = '--', linewidth=0.6)
ax.set_title('Irradiância - Fev/2025')
ax.set_xlabel('Longitude', fontsize = 10)
ax.set_ylabel('Latitude', fontsize = 10)





Arrunando os grides para graus

clipped = rio.open_rasterio(pathout + 'clipped.tif', masked=True).squeeze()
regioes = gpd.read_file(path + 'shapes/BR_Regioes_2024/BR_Regioes_2024.shp', masked=True).squeeze()
f,ax=plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
clipped.plot(ax=ax, cbar_kwargs = {'orientation':'vertical', 'shrink': 0.8, 'label':'Irradiância (W/m.m)'})
regioes.plot(ax=ax, facecolor='none', edgecolor='black')
ax.set_title('Irradiância - Fev/2000')
ax.set_xlabel('Longitude', fontsize = 10)
ax.set_ylabel('Latitude', fontsize = 10)
grid.ylabels_right = False
grid.xlabels_top = False
grid.yformatter = LATITUDE_FORMATTER
grid.xformatter = LONGITUDE_FORMATTER








