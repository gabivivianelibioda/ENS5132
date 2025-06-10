# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 11:38:53 2025

@author: PC

"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#%%Floresta Ano
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/FOD_ano.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (20,5))
ax = sns.boxplot(read, orient='v', color = 'lightgreen')
sns.set_style("whitegrid")
plt.title('Gráfico Boxplot - Média Diária da Evapotranspiração ao Ano da Floresta Ombrófila Densa', fontsize = 16)
plt.ylim(0,6)
plt.xlabel ('Ano', fontsize = 14)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 14)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/FOD_year_color2_graphic.png')
#%%Floresta Mês
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/FOD_mes.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (6,5))
ax = sns.boxplot(read, orient='v', color = 'lightgreen',  width = 0.7)
sns.set_style("whitegrid")
plt.title('Gráfico Boxplot\nMédia Diária da Evapotranspiração por Mês\nFloresta Ombrófila Densa', fontsize = 12)
plt.ylim(-0.3,6)
plt.xlabel ('Mês', fontsize = 10)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 10)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/FOD_mes_color2_graphic.png')
#%%Floresta Estação do Ano
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/FOD_Season.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (6,5))
ax = sns.boxplot(read, orient='v', color = 'lightgreen',  width = 0.7)
sns.set_style("whitegrid")
plt.title('Gráfico Boxplot\nMédia Diária da Evapotranspiração por Estações do Ano\nFloresta Ombrófila Densa', fontsize = 12)
plt.ylim(-0.3,6)
plt.xlabel ('Estações do Ano', fontsize = 10)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 10)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/FOD_Season_color2_graphic.png')
#%%Área Urbana Ano
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/AURB_ano.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (20,5))
sns.set_style("whitegrid")
ax = sns.boxplot(read, orient='v', color = 'gray')
plt.title('Gráfico Boxplot - Média Diária da Evapotranspiração ao Ano da Área Urbana', fontsize = 16)
plt.ylim(0,6)
plt.xlabel ('Ano', fontsize = 14)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 14)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/AURB_year_color2_graphic.png')
#%%Área Urbana Mês
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/AURB_mes.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (6,5))
sns.set_style("whitegrid")
ax = sns.boxplot(read, orient='v', color = 'gray',  width = 0.7)
plt.title('Gráfico Boxplot\nMédia Diária da Evapotranspiração por Mês\nÁrea Urbana', fontsize = 12)
plt.ylim(-0.3,6)
plt.xlabel ('Mês', fontsize = 10)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 10)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/AURB_mes_color_graphic.png')
#%%Área Urbana Estação do Ano
PATH = 'C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/New folder/AURB_Season.xlsx'
read= pd.read_excel(PATH)
fig, ax = plt.subplots(figsize = (6,5))
sns.set_style("whitegrid")
ax = sns.boxplot(read, orient='v', color = 'gray',  width = 0.7)
plt.title('Gráfico Boxplot\nMédia Diária da Evapotranspiração por Estações do Ano\nÁrea Urbana', fontsize = 12)
plt.ylim(-0.3,6)
plt.xlabel ('Estações do Ano', fontsize = 10)
plt.ylabel('Evapotranspiração (mm/d)', fontsize = 10)
plt.savefig('C:/ENS5132/ENS5132/Projeto02/Output2/Read_1985_2024/Grap/AURB_Season_color2_graphic.png')