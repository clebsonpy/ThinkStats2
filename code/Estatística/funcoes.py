import calendar as cal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def dados(dir, label):
    
    dados = pd.read_csv(dir, index_col=0, parse_dates=True)
    boolean = dados[label].isnull()
    date = boolean.loc[boolean == False].index

    return dados[label].loc[date[0]:date[-1]]

def date(dados, start, end):
    date_start = pd.to_datetime(start, dayfirst=True)
    date_end = pd.to_datetime(end, dayfirst=True)
    
    return dados.loc[date_start:date_end]

def month_start_year_hydrologic(dados):
    mean_month = [dados.loc[dados.index.month == i].mean() for i in range(1, 13)]
    month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
    month_start_year_hydrologic_abr = cal.month_abbr[month_start_year_hydrologic].upper()
    month_num = month_start_year_hydrologic
    month_abr = month_start_year_hydrologic_abr
    
    return month_num, month_abr

def annual(dados, month_start_year_hydrologic):
    data_by_year_hydrologic = dados.groupby(pd.Grouper(freq='AS-%s' % month_start_year_hydrologic[1]))
    max_vazao = data_by_year_hydrologic.max().values
    idx_vazao = data_by_year_hydrologic.idxmax().values

    peak = pd.Series(max_vazao, index=idx_vazao, name='VMA')

    return peak

def plot_pmf(dados, bins):
    counts, binss = np.histogram(dados, bins=bins, density=True)
    #binss = binss[:-1] + (binss[1] - binss[0])/2
    plt.bar(binss, counts)