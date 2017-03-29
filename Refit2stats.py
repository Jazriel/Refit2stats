# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:40:42 2017

@author: Javier Martínez Riberas
"""
import pandas as pd

def extract_metrics_from_csv(
        filename = 'metrics.csv',
        quantiles = (0.25, 0.75)):
	"""
	Simple script that extracts the data from the csv and dumps it into a pandas DataFrame.
	"""
    
    project =  pd.read_csv(filename, na_values='NaN')
    
	metrics = ('V(G)', 'NP', 'WMC', 'RFC', 'DIT', 'NOC', 'Ca', 'Ce', 'I', 'A', 'D', 'LCOM')
	
    stats = dict() 
    for index in metrics:
        stats[index] = []
        for p in quantiles:
            stats[index].append(project[index]                           
                                         .quantile(p, interpolation='nearest'))
    
    
    for type_ in set(project['Type']):
        stats['NCLOC_' + type_] = []
        for quantile in quantiles:
            stats['NCLOC_' + type_].append(project.loc[project['Type'] == type_]['NCLOC'].quantile(quantile, interpolation='nearest'))
    
    nps = dict()
    last_class = ''
    for row in project.itertuples():
        if(row.Type == 'class'):
            nps[row.Location] = []
            last_class = row.Location
        elif(row.Type == 'method'):
            nps[last_class].append(row.NP)
        else:
            pass
    
    nps_aux = dict()
    
    for class_ in nps:
        semi = 0
        for v in nps[class_]:
            semi += v
        if len(nps[class_]) == 0:
            nps_aux[class_] = 0
        else:
            nps_aux[class_] = semi/len(nps[class_])
    
    nps = pd.Series(nps_aux)
    
    stats['NPS'] = []
    stats['NPS'].append(nps.quantile(0.25, interpolation='nearest'))
    stats['NPS'].append(nps.quantile(0.75, interpolation='nearest'))
    
    return pd.DataFrame(stats, index=[str(x)[-2:] for x in quantiles])


if __name__=='__main__':
    extract_metrics_from_csv()