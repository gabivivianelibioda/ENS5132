# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:36:00 2025

@author: PC
"""# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:38:45 2025

@author: GABI
"""

import rasterio as rio
from rasterio.plot import show
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from datetime import datetime
 



pathshp = "C:/ENS5132/ENS5132/Projeto02/Input2/"
path = "C:/ENS5132/ENS5132/Projeto02/Input2/"
pathtif = "C:/ENS5132/ENS5132/Projeto02/Input2/Tif/"
listpath = os.listdir(pathtif)
pathouta = "C:/ENS5132/ENS5132/Projeto02/Output2/"
os.makedirs(pathouta + 'Read_1985_2024/', exist_ok = True)
lista_read = os.listdir(pathouta + 'Read_1985_2024/')
folder = pathouta + 'Read_1985_2024/'
os.makedirs(pathouta + 'MK_1985_2024/', exist_ok = True)
listmk = os.listdir(pathouta + 'MK_1985_2024/')
os.makedirs(folder + 'New folder/', exist_ok = True)


classes = ['FOD', 'AURB']
        

listtifs = []
for file in listpath:
    if file.endswith('.tif'):
        list_tifs = file
        listtifs.append(list_tifs) 

listpathstifs = []
for item in listtifs:
    if item.endswith('.tif'):
        path_tifs = os.path.join(pathtif + item)
        listpathstifs.append(path_tifs)



Adata = []
AL = []
for name in classes:    
    alldataframes = []
    allamostra = []
    for caminho in listpathstifs:
        raster = rio.open(caminho)
        raster_values = raster.read(1)
        data = caminho[57:65]
        Adata.append(data)
        data.split('/')
        datasarq = data.split('/')[0][0:4] + '/' + data.split('/')[0][4:6] + '/' + data.split('/')[0][6:9]
        datafilename = data.split('_')[0][0:4] + '_' + data.split('_')[0][4:6] + '_' + data.split('_')[0][6:9]
        landsat = caminho[40:44]
        AL.append(landsat)
        amostra = gpd.read_file(pathshp + 'Am.shp')
        amostra ['Value'] = 0
        amostra ['Data'] = 0
        amostra ['Landsat'] = 0
        amostra ['Classe'] = 0
        for index, row in amostra.iterrows():
            p = row['id']
            long = row['geometry'].x
            lat = row['geometry'].y
            rowIndex, colIndex = raster.index(long, lat)
            amostra ['Value'].loc[index] = raster_values[rowIndex, colIndex]
            amostra ['Data'] = datasarq
            amostra ['Landsat'] = landsat
            amostra ['Classe'] = name
        allamostra.append(amostra)
        #alldataframes.append(amostra)
    alldataframesdf = pd.concat(allamostra)
    alldataframesdf.to_csv(pathouta + 'All_' + name + '_1985_2024.csv')
    
    
for name in classes:   
    alldataread = pd.read_csv(pathouta + 'All_' + name + '_1985_2024.csv', sep=',', encoding='latin-1')
    datatimedef =  pd.to_datetime(alldataread['Data'])
    datatimedefdf = pd.DataFrame(datatimedef)
    datatimedefdf = datatimedefdf.rename(columns = {'Data':'Datetime'})
    alldataread = pd.concat([alldataread, datatimedefdf], axis = 1)
    alldataread['Ano'] = alldataread['Datetime'].dt.year
    alldataread['Mes'] = alldataread['Datetime'].dt.month
    alldataread['Dia'] = alldataread['Datetime'].dt.day
    alldataread ['Season'] = np.nan
    alldataread['Season'][(alldataread['Datetime'].dt.month == 12) & (alldataread['Datetime'].dt.day >= 21) | 
                      (alldataread['Datetime'].dt.month == 1) | (alldataread['Datetime'].dt.month == 2) | 
                      (alldataread['Datetime'].dt.month == 3) & (alldataread['Datetime'].dt.day <= 20)] = 'Verão'
    # Outono
    alldataread['Season'][(alldataread['Datetime'].dt.month == 3) & (alldataread['Datetime'].dt.day > 20) | 
                      (alldataread['Datetime'].dt.month == 4) | (alldataread['Datetime'].dt.month == 5) |
                      (alldataread['Datetime'].dt.month == 6) & (alldataread['Datetime'].dt.day <= 20)] = 'Outono'
    # Inverno
    alldataread['Season'][(alldataread['Datetime'].dt.month == 6) & (alldataread['Datetime'].dt.day >20) | 
                      (alldataread['Datetime'].dt.month == 7) | (alldataread['Datetime'].dt.month == 8) | 
                      (alldataread['Datetime'].dt.month == 9)  & (alldataread['Datetime'].dt.day <= 22)]  = 'Inverno'
    # Primavera
    alldataread['Season'][(alldataread['Datetime'].dt.month == 9) & (alldataread['Datetime'].dt.day > 22)  | 
                      (alldataread['Datetime'].dt.month ==10) | (alldataread['Datetime'].dt.month ==11) | 
                      (alldataread['Datetime'].dt.month == 12) & (alldataread['Datetime'].dt.day <= 20)] = 'Primavera'
    alldataread.to_csv(pathouta +'All_' + name + '_1985_2024.csv')
    alldatareadmes = pd.concat([alldataread['Classe'], alldataread['Value'], alldataread['Mes']], axis = 1) 
    alldatareadano = pd.concat([alldataread['Classe'], alldataread['Value'], alldataread['Ano']], axis = 1)
    alldatareadseason = pd.concat([alldataread['Classe'], alldataread['Value'], alldataread['Season']], axis = 1) 
    alldatareadmes.to_csv(folder + 'New folder/' + 'All_' + name + '_Mes.csv')
    alldatareadano.to_csv(folder + 'New folder/' + 'All_' + name + '_Ano.csv')
    alldatareadseason.to_csv(folder + 'New folder/' + 'All_' + name + '_Season.csv')


