# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:40:42 2017

@author: Jack
"""
import pandas as pd

metrics = ('V(G)', 'NP', 'WMC', 'RFC', 'DIT', 'NOC', 'Ca', 'Ce', 'I', 'A', 'D', 'LCOM')

quantiles = (0.25, 0.75)

jsonfiter_data = pd.read_csv('jsonfiter.csv', na_values='NaN')
jschevalidator_data = pd.read_csv('jsonschemaval.csv', na_values='NaN')

projects = {
        'jsonfiter': jsonfiter_data,
        'jsonschema': jschevalidator_data
        }

stats = dict()

for project in projects:
    stats[project] = dict() 
    for index in metrics:
        for p in quantiles:
            stats[project][index + str(p)[-2:]] = projects[project][index].quantile(p)
    
