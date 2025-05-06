# -*- coding: utf-8 -*-
"""
Created on Mon May  5 21:14:48 2025

@author: gabri
"""

def gerandoplots ():
    import matplotlib.pyplot as plt #gráficos
    import openpyxl as opx 
    import seaborn as sns #estatística
    import plotly.express as px #bloxplot
    from scipy import stats
    from scipy.stats import lognorm
    from scipy.stats import kstest
    import statsmodels.api as sm
    from statsmodels.tsa.seasonal import seasonal_decompose
    from PlanilhaDados import planilhasevapo
    
    meses = ['', 'Jan', 'Fev','Mar', 'Abr', 'Mai', 'Jun', 
             'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    anos = []
    for num in range (1984, 2025):
        ano = num
        anos.append(ano)
    
    #Agrupamento     
    alldatareadgroupano = alldataread.groupby(['Ano','nm_class_2']).describe() #média por ano
    aqtablesumano = alldataread.reset_index(drop=True).pivot_table(columns='Ano', 
                                                                   index=['nm_class_2'], values='_sum')
    aqtablecountano = alldataread.reset_index(drop=True).pivot_table(
        columns='Ano',
        index=['nm_class_2'],
        values='_count')
    mediaaqtableano =  (aqtablesumano / aqtablecountano)
    mediaaqtableano.to_csv(pathout + 'media_ano_classe.csv')
    
    alldatareadgroupmes = alldataread.groupby(['Mes','nm_class_2']).describe() #média por mês
    aqtablesummes = alldataread.reset_index(drop=True).pivot_table(
        columns='Mes',
        index=['nm_class_2'],
        values='_sum')
    aqtablecountmes = alldataread.reset_index(drop=True).pivot_table(
        columns='Mes',
        index=['nm_class_2'],
        values='_count')
    mediaaqtablemes =  (aqtablesummes / aqtablecountmes)
    mediaaqtablemes.to_csv(pathout + 'media_mes_classe.csv')
    
    #Gráficos 
    mediaaqtablemes_filtrado = mediaaqtablemes.iloc[4,:]/1000
    meses = pd.DataFrame(meses).rename(columns = {0: 'Mês'})
    mediaaqtablemesgraphconcat = pd.concat([mediaaqtablemes_filtrado,meses], axis = 1)
    mediaaqtablemesgraph = mediaaqtablemesgraphconcat.set_index('Mês').dropna()
    
    #Teste de Normalidade
    test=stats.normaltest(mediaaqtablemesgraph['Floresta ombrofila densa'].dropna())
    testlog = stats.normaltest(np.log(mediaaqtablemesgraph['Floresta ombrofila densa'].dropna()))
    testBox = stats.normaltest(stats.boxcox(mediaaqtablemesgraph['Floresta ombrofila densa'].dropna())[0])
    
    fig, ax = plt.subplots()
    ax = plt.plot(mediaaqtablemesgraph, color ='mediumvioletred')
    plt.title('Floresta Ombrofila Densa - Sazonalidade')
    plt.xlabel('Meses')
    plt.ylabel('Evapotranspiração (mm)')
    fig.savefig(pathout+'Comportamento_Sazonal.png')
    
    fig, ax = plt.subplots()
    ax = mediaaqtableano_filtrado = mediaaqtableano.iloc[4,:]/1000
    fig1ano = plt.plot(mediaaqtableano_filtrado, color = 'mediumvioletred')
    plt.title('Floresta Ombrofila Densa - Comportamento')
    plt.xlabel('Ano')
    plt.ylabel('Evapotranspiração (mm)')
    fig.savefig(pathout+'Comportamento_Anual.png')
    
    fig, ax = plt.subplots()
    ax = plt.boxplot(mediaaqtablemesgraph)
    plt.title('Boxplot Média Mensal')
    plt.suptitle('Floresta Ombrofila Densa')  # Remove o título automático gerado pelo pandas
    plt.xlabel('')
    plt.ylabel('Evapotranspiração (mm)')
    plt.show()
    fig.savefig(pathout+'Boxplot_mensal.png')
    
    fig, ax = plt.subplots()
    ax = plt.boxplot(mediaaqtableano_filtrado)
    plt.title('Boxplot Média Anual')
    plt.suptitle('Floresta Ombrofila Densa')  # Remove o título automático gerado pelo pandas
    plt.xlabel('')
    plt.ylabel('Evapotranspiração (mm)')
    plt.show()
    fig.savefig(pathout+'Boxplot_anual.png')
    
    fig, ax = plt.subplots(3)
    ax[0].hist(np.log(mediaaqtableano_filtrado), 
               facecolor='mediumvioletred', 
               edgecolor = 'black')
    ax[0].set_title('Log')
    ax[0].set_ylabel('Frequência')
    ax[1].hist(stats.boxcox(mediaaqtableano_filtrado),
               facecolor='mediumvioletred', 
               edgecolor = 'black')
    ax[1].set_title('Boxcox')
    ax[1].set_ylabel('Frequência')
    ax[2].hist(mediaaqtableano_filtrado.dropna(), 
               facecolor='mediumvioletred', 
               edgecolor = 'black')
    ax[2].set_title('Dado original')
    ax[2].set_xlim(0,4)
    ax[2].set_ylabel('Frequência')
    fig.tight_layout() 
    fig.savefig(pathout +'histogram_Data_Normalization_.png')
        
      
    mediaaqtablemes_mm = mediaaqtablemes/1000
    mediaaqtableano_mm = mediaaqtableano/1000
    #Anocoluna = mediaaqtableano_mm.columns
    q = enumerate(mediaaqtablemes_mm.index)
    qlist = list(q)
    listaclassemes = []
    listanummes = []
    for item in qlist:
    q = item[0]
    listanummes.append(q)
    for item in qlist:
    q = item[1]
    listaclassemes.append(q)
    
    j = enumerate(mediaaqtableano_mm.index)
    jlist = list(j)
    listanumano = []
    for item in jlist:
    i = item[0]
    listanumano.append(i)
    print(jlist)
    #Por mês:
    print(jlist [5][0])      
    fig, ax = plt.subplots()
    for num in listanummes:
        valor = mediaaqtablemes_mm.iloc[num]
        ax.plot(valor)
        plt.tight_layout()
        ax.set_title('Comportamento ao Longo dos Anos')
        ax.set_ylabel('Evapotranspiração (mm)')
        ax.set_xlabel('Ano')
    fig.savefig(pathout + 'fig_classe_mes.png')
    
    fig2, ax = plt.subplots()
    for num in listanummes:
        valor = mediaaqtablemes_mm.iloc[num]
        ax.plot(valor)
        plt.legend(loc='upper right', bbox_to_anchor=(1, 1.05))
        plt.tight_layout()
        ax.set_title('Comportamento ao Longo dos Anos')
        ax.legend(mediaaqtablemes_mm.index)
        ax.set_ylabel('Evapotranspiração (mm)')
        ax.set_xlabel('Ano')
    fig2.savefig(pathout + 'fig_classe_mes_legenda.png')
    
    for num in listanummes:
    figboxplot, ax = plt.subplots()
    valor = mediaaqtablemes_mm.iloc[num]
    ax = plt.boxplot(valor)
    plt.title('Boxplot Média Mensal')
    plt.suptitle(num)  # Remove o título automático gerado pelo pandas
    plt.xlabel('')
    plt.ylabel('Evapotranspiração (mm)')
    plt.ylim(0,6)
    plt.show()
    figboxplot.savefig(pathout + 'boxplot_'+ str(num) +'_classe_mes_legenda.png')
    
    #Por ano:
    fig, ax = plt.subplots()
    for num in listanumano:
        valor = mediaaqtableano_mm.iloc[num]
        ax.plot(valor)
        plt.tight_layout()
        ax.set_title('Comportamento ao Longo dos Anos')
        ax.set_ylabel('Evapotranspiração (mm)')
        ax.set_xlabel('Ano')
    fig.savefig(pathout + 'fig_classe_ano.png')
    
    fig2, ax = plt.subplots()
    for num in listanumano:
        valor = mediaaqtableano_mm.iloc[num]
        ax.plot(valor)
        plt.legend(loc='upper right', bbox_to_anchor=(1, 1.05))
        plt.tight_layout()
        ax.set_title('Comportamento ao Longo dos Anos')
        ax.legend(mediaaqtableano_mm.index)
        ax.set_ylabel('Evapotranspiração (mm)')
        ax.set_xlabel('Ano')
    fig2.savefig(pathout + 'fig_classe_ano_legenda.png')
    

    
    return 