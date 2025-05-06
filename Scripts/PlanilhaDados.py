# -*- coding: utf-8 -*-
"""
Created on Mon May  5 22:10:48 2025

@author: gabri
"""
#mesma tabela, mas com os shapes menores e mais focado no tipo de material que evapotranspira na lagoa
def planilhasevapo (Classes, alldataread):
    import numpy as np
    import pandas as pd
    import os
    
    pathmain = "C:/ENS5132/ENS5132/Projeto01/"
    pathexcel = "C:/ENS5132/ENS5132/Projeto01/Inputs/" #Estatisticas
    pathout = "C:/ENS5132/ENS5132/Projeto01/Outputs/"
    Lista = os.listdir(pathexcel)
    for file in Lista:
        reading = pd.read_excel(pathexcel + file)
    Classes = reading['nm_class_2']
    allfiles=[]
    for file in Lista:
        arqread = pd.read_excel(pathexcel+file)
        arqreaddf = pd.DataFrame(arqread)
        dataarq = file[0:8]
        datas = []
        landsats = []
        for classe in Classes:
            dataarqcopy = np.copy(dataarq)
            datas.append(dataarqcopy)
        datasdf = pd.DataFrame(datas)
        datasdfrenamed = datasdf.rename(columns = {0:'Data'})
        datasconcat = pd.concat([arqreaddf,datasdfrenamed], axis=1)
        Landsat = file[9:11]
        landsats = []
        for classe in Classes:
            Landarqcopy = np.copy(Landsat)
            landsats.append(Landarqcopy)
        landsatdf = pd.DataFrame(landsats)
        Landdfrenamed = landsatdf.rename(columns = {0:'Landsat'})
        Landconcat = pd.concat([datasconcat,Landdfrenamed], axis=1)
        allfiles.append(Landconcat)
        allfilesconcat = pd.concat(allfiles)
        allfilesconcatdf = pd.DataFrame(allfilesconcat)
        Landconcat.to_csv(pathout + file[0:11] +'_data.csv')
    allfilesconcat.to_csv(pathout + 'alldata.csv')
    ListaOut = os.listdir(pathout)
    
    alldataread = pd.read_csv(pathout + 'alldata.csv', sep=',', encoding='latin-1')
    datatimedef =  pd.to_datetime(alldataread['Data'], format = '%Y%m%d')
    datatimedefdf = pd.DataFrame(datatimedef)
    datatimedefdf = datatimedefdf.rename(columns = {'Data':'Datetime'})
    alldataread = pd.concat([alldataread, datatimedefdf], axis = 1)
    alldataread['Mes'] = alldataread['Datetime'].dt.month
    alldataread['Ano'] = alldataread['Datetime'].dt.year
    alldataread ["Season"] = np.nan
    # Verão
    alldataread["Season"][(alldataread.Mes==1) | (alldataread.Mes==12) | 
                      (alldataread.Mes==2) ] = 'Verão'
    # Outono
    alldataread["Season"][(alldataread.Mes==3) | (alldataread.Mes==5) | 
                      (alldataread.Mes==4) ] = 'Outono'
    # Inverno
    alldataread["Season"][(alldataread.Mes==6) | (alldataread.Mes==7) | 
                      (alldataread.Mes==8) ] = 'Inverno'
    # Primavera
    alldataread["Season"][(alldataread.Mes==9) | (alldataread.Mes==10) | 
                      (alldataread.Mes==11) ] = 'Primavera'
    alldataread.to_csv(pathout + 'alldata2.csv')
    return (Classes, alldataread)

    