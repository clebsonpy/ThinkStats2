import calendar as cal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import thinkplot
import thinkstats2
import scipy.stats as ss

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

def dados_media(dados, freq='M'):
    dados = dados.groupby(pd.Grouper(freq=freq)).mean()
    return dados

def dados_acumulado(dados, freq='M'):
    dados = dados.groupby(pd.Grouper(freq=freq)).sum()
    if freq == 'A':
        return dados.loc[dados.values > 1000]
    return dados

def plot_percentil(dados_chuva, dados_vazao):
    dados_month = pd.DataFrame([dados_chuva, dados_vazao])
    dados_month = dados_month.T
    
    dados_month = dados_month.dropna(subset=[dados_chuva.name, dados_vazao.name])
    bins = np.arange(0, 400, 40)
    indices = np.digitize(dados_month[dados_chuva.name], bins)
    groups = dados_month.groupby(indices)
    
    mean_chuva = [group[dados_chuva.name].mean() for i, group in groups]
    cdfs = [thinkstats2.Cdf(group[dados_vazao.name]) for i, group in groups]
    
    for percent in [75, 50, 25]:
        vazao_percentiles = [cdf.Percentile(percent) for cdf in cdfs]
        label = '%d°' % percent
        thinkplot.Plot(mean_chuva, vazao_percentiles, label=label)

def expon_distribution(dados):
    
    mu,sigma=ss.expon.fit(dados)
    lin = np.linspace(0, dados.max(), num=100)
    
    expon_cdf = ss.expon.cdf(lin, mu, sigma)
    plt.plot(lin, expon_cdf, color='black')
    
def normal_pdf(dados):
    
    mean = dados.mean()
    std_dev = dados.std()
    lin = ss.norm.rvs(size=10000, loc=mean, scale=std_dev) 
    x = np.sort(lin)
    normal = ss.norm.pdf(x, mean, std_dev)
    plt.plot(x, normal, color='black')

    
def normal_cdf(dados, label):
    
    mean = dados.mean()
    std_dev = dados.std()
    lin = ss.norm.rvs(size=10000, loc=mean, scale=std_dev) 
    x = np.sort(lin)
    normal = ss.norm.cdf(x, mean, std_dev)
    plt.plot(x, normal, color='black', label=label)
    
def lognormal_pdf(dados):
    
    s, loc, scale = ss.lognorm.fit(dados)
    print(s)
    lin = ss.lognorm.rvs(s=s, size=1000, loc=loc, scale=scale) 
    x = np.sort(lin)
    normal = ss.norm.pdf(x, loc=loc, scale=scale)
    plt.plot(x, normal, color='black')

    
def lognormal_cdf(dados, label):
    
    s, loc, scale = ss.lognorm.fit(dados)
    lin = ss.lognorm.rvs(s=s, size=1000, loc=loc, scale=scale)
    x = np.sort(lin)
    normal = ss.norm.cdf(x, loc=loc, scale=scale)
    plt.plot(x, normal, color='black', label=label)

    
def pareto_cdf(dados, label):

    b, loc, scale = ss.pareto.fit(dados)
    lin = ss.pareto.rvs(b=b, size=1000, loc=loc, scale=scale)
    x = np.sort(lin)
    pareto_cdf = ss.pareto.cdf(x, b=b, loc=loc, scale=scale)
    plt.plot(x, pareto_cdf, color='black', label=label)
    
def pareto_pdf(dados):
    
    b, loc, scale = ss.pareto.fit(dados)
    lin = ss.pareto.rvs(b=b, size=1000, loc=loc, scale=scale)
    x = np.sort(lin)
    pareto_pdf = ss.pareto.pdf(x, b=b, loc=loc, scale=scale)
    plt.plot(x, pareto_pdf, color='black')
    