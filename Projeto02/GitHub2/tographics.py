# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:30:29 2025

@author: GABI
"""
import os
import pandas as pd
import numpy as np

path = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/'
lista = os.listdir(path)
listaarq = []
for arquive in lista:
    if arquive.endswith('Ano.csv'):
        listaarq.append(arquive)

anos = np.array(range(1985,2025))
anosdataframe = (pd.DataFrame(anos)).transpose()

for arq in listaarq:
    patharq = path + arq
    listarqread = pd.read_csv(patharq)
    classe = pd.unique(listarqread ['Classe'])
    anounique = pd.unique(listarqread['Ano']).tolist()
    anounique.sort()
    anounique = np.array(anounique)
    Planilha = []
    Planilha.append(pd.DataFrame(anosdataframe))
    Anos = []
    for year in anounique:
        filtro = listarqread[listarqread ['Ano'] == year]
        filtro = filtro['Value']
        filtro = filtro.reset_index()
        filtro = np.array(filtro)
        filtro_t = np.transpose(filtro)
        filtro_t = filtro_t[1]/1000
        filtrodf = (pd.DataFrame(filtro_t).rename(columns={0:year})).transpose()
        Anos.append(filtrodf)
    AnosConcat = pd.concat(Anos).transpose()
    AnosConcat.to_excel(path + arq[4:-8] + '_ano.xlsx', index=False)

listaarq = []
for arquive in lista:
    if arquive.endswith('_Mes.csv'):
        listaarq.append(arquive)
        
meses = np.array(range(1,13))

for csv in listaarq:
    pathcsv = path + csv
    leitura_arq = pd.read_csv(pathcsv)
    planilha = []
    for i in meses:
        Mes = leitura_arq[leitura_arq['Mes']==i]
        Mes = Mes['Value']/1000
        Mes = pd.DataFrame(Mes).reset_index()
        Mes = Mes.iloc[:,1]
        Mes = pd.DataFrame(Mes)
        if i == 1: name = 'Jan'
        if i == 2: name = 'Fev'
        if i == 3: name = 'Mar'
        if i == 4: name = 'Abr'
        if i == 5: name = 'Mai'
        if i == 6: name = 'Jun'
        if i == 7: name = 'Jul'
        if i == 8: name = 'Ago'
        if i == 9: name = 'Set'
        if i == 10: name = 'Out'
        if i == 11: name = 'Nov'
        if i == 12: name = 'Dez'
        Mes = Mes.rename(columns={'Value':name}).transpose()
        planilha.append(Mes)
    planilhafinal = (pd.concat(planilha)).transpose()
    planilhafinal.to_excel(path + csv[4:-8] + '_mes.xlsx', index=False)


listaarq = []
for arquive in lista:
    if arquive.endswith('_Season.csv'):
        listaarq.append(arquive)

Seasons = ['Outono', 'Inverno', 'Primavera', 'Verão']

for csv in listaarq:
    pathcsv = path + csv
    leitura_arq = pd.read_csv(pathcsv)
    planilha = []
    for i in Seasons:
        Season = leitura_arq[leitura_arq['Season']==i]
        Season = Season['Value']/1000
        Season = pd.DataFrame(Season).reset_index()
        Season = Season.iloc[:,1]
        Season = pd.DataFrame(Season)
        Season = Season.rename(columns={'Value':i}).transpose()
        planilha.append(Season)
    planilhafinal = (pd.concat(planilha)).transpose()
    planilhafinal.to_excel(path + csv[4:-11] + '_Season.xlsx', index=False)
