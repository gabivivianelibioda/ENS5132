# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:37:58 2025

@author: PC
"""

"""
Created on Sun May 25 06:47:11 2025

@author: gabri
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt #gráficos
from statsmodels.tsa.seasonal import seasonal_decompose
import pymannkendall as mk



diretorio = 'C:/ENS5132/ENS5132/Projeto02/Output2/'
lista = os.listdir(diretorio)

caminho2 = diretorio + 'Read_1985_2024/'
mkpath2 = diretorio + 'MK_1985_2024/'
lista2 = os.listdir(caminho2)


col = pd.DataFrame ( ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope', 'intercept', 'classe'] )

#%% 1985 - 2024:

for arq in lista:
    if arq.endswith('_1985_2024.csv'):
        pathfile = diretorio + arq
        classe = arq[:-14]
        classe = classe[4:]
        read = pd.read_csv(pathfile)
        read['Image'] = read['Data'] + '_' + read['Landsat']
        read.to_csv(caminho2 + classe + '.csv')
        
pathfile = caminho2 + 'FOD' + '.csv'
readfile = pd.read_csv(pathfile)
image = pd.unique(readfile['Image'])
image = pd.DataFrame(image).rename(columns = {0: 'Image'})
image.to_csv(mkpath2 + 'ImagesUnique1985-2024.csv')

Teste_Result = []
for file in lista2:
    if file.endswith('.csv'):
        pathway = caminho2 + file
        classe  = file[:-4]
        fileread = pd.read_csv(pathway)
        fileread['Value'] = fileread['Value'] /1000
        filereaddt = pd.to_datetime(fileread['Data'])
        fileread = fileread.rename(columns={'Data': 'data1'})
        filereadconcat = pd.concat([fileread, filereaddt], axis =1)
        filereadconcatfinal = filereadconcat.groupby(['Data', 'Landsat'], as_index=False)['Value'].mean()
        testmkarquivo = mk.original_test(filereadconcatfinal['Value'], alpha =  0.05)
        testmkarquivodf = pd.DataFrame(testmkarquivo)
        testmkarquivot = testmkarquivodf.transpose()
        testmkarquivot ['9'] = classe
        Teste_Result.append(testmkarquivot)
Test_Resultdf = pd.concat(Teste_Result)
Test_Resultdf = (pd.DataFrame(Test_Resultdf)).rename(columns={0:'trend', 1: 'h', 2: 'p', 3: 'z', 4: 'Tau', 
                                                              5: 's', 6: 'var_s', 7: 'slope', 8: 'intercept', 
                                                              9: 'classe'})
Test_Resultdf.to_csv(mkpath2 + 'Test_mk_0.05_1985-2024.csv')
print(Test_Resultdf)

