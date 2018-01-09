#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

import pandas as pd
import numpy as np

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
mean_ratings = data.pivot_table('rating',index='title',columns='gender',aggfunc='mean')
print(mean_ratings)