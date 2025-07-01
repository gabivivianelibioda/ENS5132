# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 14:07:49 2025

@author: gabri

https://disc.gsfc.nasa.gov/

https://ads.atmosphere.copernicus.eu/#!/home

Neste trabalho vocês precisarão demontrar que:

1 - Sabem abrir e explorar um cube data

2 - Sabem recortar o cube data para uma região de interesse

3 - Sabem extrair dados e analisar dados no tempo e no espaço

OU usando um netCDF conhecido.

Seguir o tutorial para analisar dados no espaço e agrupá-los : https://martinfleischmann.net/sds/clustering/quiz.html

https://geographicdata.science/book/notebooks/06_spatial_autocorrelation.html

OU criando seu netCDF.

Transformando um arquivo de geometria em uma grade regular com variabilidade no tempo. Ou seja, transformar um shapefile/geodataframe em um netCDF e avalia-lo. 
"""

#Data Cube
import xarray as xr
import rioxarray as rio
from shapely.geometry import mapping
import numpy as np
import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
from mpl_toolkits.basemap import Basemap
import regionmask
from statsmodels.tsa.seasonal import seasonal_decompose
import pymannkendall as mk


project = 'C:/ENS5132/ENS5132/Projeto03/'
path = 'C:/ENS5132/ENS5132/Projeto03/Input3/'
pathnetCDF = 'C:/ENS5132/ENS5132/Projeto03/Input3/GLDAS/'
listanetCDF = os.listdir(pathnetCDF)
df = pd.DataFrame(listanetCDF)

#Ponto na região Sul:
#Leitura dos Dados nc4:
AllData = []
TranspCanopyall = []
meses = []
anos =  []
files = []
for arq in listanetCDF:
    caminhoitem = pathnetCDF + arq
    Mes = arq[-10:]
    Mes = Mes[0:2]
    Ano = arq[-14:]
    Ano = Ano[0:4]
    read = xr.open_dataset(caminhoitem)
    read.rio.set_spatial_dims(x_dim = 'lon', y_dim = 'lat', inplace=True)
    read.dims
    read.data_vars
    read.lat
    read.lon
    TranspCanopy = read.variables['TVeg_tavg'][:]
    lon = read.variables['lon'][:]
    lat = read.variables['lat'][:]
    longitude = -50.5
    latitude = -25.5
    lat_ind = (np.abs(lat-latitude)).argmin()
    lon_ind = (np.abs(lon-longitude)).argmin()
    data = pd.DataFrame(TranspCanopy[:,lat_ind,lon_ind])
    files.append(read)
    meses.append(Mes)
    anos.append(Ano)
    AllData.append(data[0])
    TranspCanopyall.append(TranspCanopy)
    
anos = pd.DataFrame(anos)
meses = pd.DataFrame(meses)
allData = pd.DataFrame(AllData)
allData.rename(columns = {0:'Value'}, inplace=True)

indexes = enumerate(allData)
allData = allData.reset_index()
allData.rename(columns = {'index':'Zeros'}, inplace=True)
allData = pd.DataFrame(allData['Value'])
allData.set_index(indexes)

df.rename(columns={0:'File'}, inplace=True)
df['Mes'] = meses
df['Ano'] = anos
df['Data'] = (df['Mes'] + '/' + df['Ano'])
df['Dados'] = allData
df.to_excel(project + 'Output3/DadosSul2.xlsx', sheet_name='Dados nc', index=False)
df = df.set_index('Data')
df.plot(title='Série Temporal Irradiação \n (Região Sul)', ylabel = 'Irradiação (W/m.m)',xlabel = 'Data')


col = pd.DataFrame ( ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept'] ).transpose()
testmk = mk.original_test(df['Dados'], alpha =  0.05)
testmkdf = pd.DataFrame(testmk)
testmkt = testmkdf.transpose()
Test_Result = pd.concat([col,testmkt])
Test_Result.to_excel(project + 'Output3/MKT3Sul2.xlsx', sheet_name='Resultados', index=False)
print(Test_Result)

#1 -50.5 e -25.5 sul
#2: -42.5 e -20.5 sudeste
#3: -53.5 e -20.5 centro-oeste
#4: -62.5 e -3.5 norte
#5: -38.5 e  -6.5 nordeste

    
#leitura unica para entender os arquivos:
read = xr.open_dataset(pathnetCDF + 'GLDAS_CLSM10_M.A200002.021.nc4')
print(read.variables.keys())
dataset = read.to_dataframe()
dados = read.rio.set_spatial_dims(x_dim = 'lon', y_dim = 'lat', inplace=True)
read.dims
read.data_vars
read.lat
read.lon

#Variáveis de Interesse:

lon = read.variables['lon'][:]
lat = read.variables['lat'][:]
times = read.variables['time_bnds'][:]
TranspCanopy = read.variables['TVeg_tavg'][:]


#`Ponto de Interesse
longitude = -50.5
latitude = -25.5


#Índices mais próximos das coordenadas escolhidas
lat_ind = (np.abs(lat-latitude)).argmin()
lon_ind = (np.abs(lon-longitude)).argmin()
data = pd.DataFrame(TranspCanopy[:,lat_ind,lon_ind])

df2 = pd.DataFrame({TranspCanopy:data}, index=df['Data'])
read.close()


print('Primeiras Linhas:')
print(df2.head())

endfile = df2.to_excel(project + 'Output3/AmostrasPontuais.xlsx', sheet_name='Dados nc', index=False)

#Plotar a série temporal completa:
df2.plot(title = 'Série Temporal - Irradiação (W/m.m) \nPonto: ({latitude}, {longitude})', ylabel = 'Irradiação', xlabel = 'Data')




