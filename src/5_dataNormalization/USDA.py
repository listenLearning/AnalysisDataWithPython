#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = "Ng WaiMing"

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import re
import json
from matplotlib import pyplot as plt

if __name__ == "__main__":
    pd.set_option('display.width', 100000)
    path = '../../data/dataSets/usda_food/database.json'
    # print(open(path).readlines())
    db = json.load(open(path))
    # print(len(db))
    # print(db[0].keys())
    # print(db[0]['nutrients'][0])
    nutrients = DataFrame(db[0]['nutrients'])
    # print(nutrients[:7])
    info_keys = ['description', 'group', 'id', 'manufacturer']
    info = DataFrame(db, columns=info_keys)
    # print(info.head())
    # print(pd.value_counts(info.group).head(10))
    nutrients = []
    for rec in db:
        fnuts = DataFrame(rec['nutrients'])
        fnuts['id'] = rec['id']
        nutrients.append(fnuts)
    nutrients = pd.concat(nutrients, ignore_index=True)
    # print(nutrients.info())
    # print(nutrients.duplicated().sum())
    nutrients = nutrients.drop_duplicates()
    col_mapping = {'description': 'food', "group": 'fgroup'}
    info = info.rename(columns=col_mapping, copy=False)
    # print(info.info())
    col_mapping = {'description': 'nutrient', "group": 'nutgroup'}
    nutrients = nutrients.rename(columns=col_mapping, copy=False)
    # print(nutrients.info())
    ndata = pd.merge(nutrients, info, on='id', how='outer')
    # print(ndata.info())
    result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
    result['Zinc, Zn'].sort_values().plot(kind='barh')
    # plt.show()
    by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
    get_maximum = lambda x: x.xs(x.value.idxmax())
    get_minimum = lambda x: x.xs(x.value.idxmin())
    max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
    max_foods.food = max_foods.food.str[:50]
    print(max_foods.ix['Amino Acids']['food'])
