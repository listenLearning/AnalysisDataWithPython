#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def loaddata(fileName, name):
    return pd.read_csv(fileName, names=name)


def loadDataSet(start, stop, names, path):
    years = range(start, stop)
    pieces = []
    for year in years:
        paths = path + 'yob%d.txt' % year
        frame = loaddata(paths, names)
        frame['year'] = year
        pieces.append(frame)
    return pieces


def get_top1000(group):
    '''
    取出分组的前N个名字
    :param group:
    :return:
    '''
    return group.sort_values(by='birth', ascending=False)[:1000]


def add_prop(group):
    '''
    增加一个prop列,用于存放指定名字的婴儿数相对于总出生数的比例
    :param group:
    :return:
    '''
    birth = group.birth.astype(float)
    group['prop'] = birth / birth.sum()
    return group


def get_quantile_count(group, q=0.5):
    return int(group.sort_values(by='prop', ascending=False).prop.cumsum().searchsorted(q)) + 1


pd.reset_option('display.width', 1000000)
names = ['name', 'sex', 'birth']
pieces = loadDataSet(start=1880, stop=2011, names=names, path='../../data/dataSets/babynames/')
# concant 按行将多个DataFrame组合到一起
# ignore_index=True 不保留read_csv返回的原始行号
names = pd.concat(pieces, ignore_index=True)
# print(names)
# print(names1880[:10])
total_birth = names.pivot_table('birth', index='year', columns='sex', aggfunc=sum)
# print(total_birth.tail())

# total_birth.plot(title='Total births by sex and year')
# plt.show()
# 按year和sex进行分组,在将新列添加到各个分组
names = names.groupby(['year', 'sex']).apply(add_prop)
# print(names)
# 验证所有分组的总和是否为1,由于这是一个浮点型数据,所以应该用np.allclose来检查这个分组总计值是否足够近似于1
bl = np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)
# print(bl)
top1000 = names.groupby(['year', 'sex']).apply(get_top1000)
# print(top1000.info())

# 分析命名的趋势
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
# print(boys)
# 按birth的具体值作聚合，year和name是筛选birth的行标签和列标签，year和name相同并且birth相同就相加，如果没有就以NaN填充
total_birth = top1000.pivot_table(values='birth', index='year', columns='name', aggfunc=sum)
# print(total_birth.head())
subset = total_birth[['John', 'Harry', 'Mary', 'Marilyn', 'Bob']]

# subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')
# plt.show()


# 评估命名多样性的增长
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
# print(table)

# table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13),
#            xticks=range(1880, 2020, 10))
# plt.show()

df = boys[boys.year == 2010]
# # print(df)
# # cumsum将当前值于以前的值累加起来，返回一个新的值
# prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
# # 对prop降序排列之后,通过searchsorted找出前面多少个名字的人数加起来才够50%
# print(prop_cumsum.searchsorted(0.5))
diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
# print(type(diversity))
diversity = diversity.unstack('sex')
# print(diversity.head())

# diversity.plot(title='Number of popular names in top 50%', xticks=range(1880, 2020, 5))
# plt.show()

last_latter = names.name.map(lambda x: x[-1])
last_latter.name = 'last_letters'
table = names.pivot_table('birth', index=last_latter, columns=['sex', 'year'], aggfunc=sum)
# print(table)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
# print(subtable.head())
# print(subtable.sum())
letter_prop = subtable / subtable.sum().astype(float)
# print(latter_prop['M'])

# fig, axes = plt.subplots(2, 1, figsize=(10, 8))
# letter_prop.loc[:, 'M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
# letter_prop.loc[:, 'F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)
# plt.show()
letter = table / table.sum().astype(float)
dny_ts = letter.ix[['a', 'e', 'n', 'y'], 'F'].T
# print(dny_ts.head())

# dny_ts.plot()
# plt.show()

all_names = top1000.name.unique()
# print(all_names)
mask = np.array(['lesl' in i.lower() for i in all_names])
# print(mask)
lesley_like = all_names[mask]
# print(lesley_like)
filered = top1000[top1000.name.isin(lesley_like)]
# print(filered.groupby('name').birth.sum())
table = filered.pivot_table(values='birth', index='year', columns='sex', aggfunc=sum)
table = table.div(table.sum(1), axis=0)
# print(table.tail())
table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()
