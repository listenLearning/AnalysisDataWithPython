#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

import pandas as pd
import numpy as np

pd.set_option('display.width', 10000)
username = ['user_id', 'gender', 'age', 'occupation', 'zip']
user = pd.read_table('../../data/dataSets/movielens/users.dat', sep='::', header=None, names=username, engine='python')
# print(user)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('../../data/dataSets/movielens/ratings.dat', sep='::', header=None, names=rnames,
                        engine='python')
# print(ratings[:5])
mname = ['movie_id', 'title', 'genres']
movies = pd.read_table('../../data/dataSets/movielens/movies.dat', sep='::', header=None, names=mname, engine='python')
# print(movies[:5])
# print(ratings.info())
data = pd.merge(pd.merge(user, ratings), movies)
# print(data.ix[0])
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
# print(mean_ratings)
# groupby相当于是一个与计算操作,返回的是一个groupby对象,只有当action操作去触发的时候,才会执行计算
# 找到所有电影的评分条数
ratings_by_title = data.groupby('title').size()
# print(ratings_by_title[:10])
# 根据计算好的评分条数,过滤评分数据不够250条的电影
active_title = ratings_by_title.index[ratings_by_title >= 250]
# print(active_title)
# ix:根据index提取出相应的值
mean_ratings = mean_ratings.ix[active_title]
# print(mean_ratings.info())
# sort_values 针对某一列进行排序
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
# print(top_female_ratings)
# 找出男女观众间分歧最大的电影
mean_ratings['diff'] = mean_ratings.M - mean_ratings.F
# print(mean_ratings[:15])
sort_by_diff = mean_ratings.sort_values(by='diff', ascending=False)
# print(sort_by_diff[:15])

# 根据电影名称分组的得分数据的标准差
rating_std_by_title = data.groupby('title')['rating'].std()
# print(ratings_by_title[:10])
rating_std_by_title = rating_std_by_title.ix[active_title]
# 根据值对Series进行降序排列
rating_std_by_title = rating_std_by_title.sort_values(ascending=False)[:10]
print(rating_std_by_title)