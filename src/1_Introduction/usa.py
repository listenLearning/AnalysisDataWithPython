#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

import json
from collections import defaultdict
import operator
from collections import Counter
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from matplotlib import pyplot as plt


def get_counts(sequence):
    '''
    对时区数进行计数
    :param sequence:
    :return:
    '''
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def get_counts2(sequence):
    '''
    对时区进行计数
    :param sequence:
    :return:
    '''
    # 所有的值都被初始化成0
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


def top_counts(counts, n=10):
    '''
    获取前n位的时区及其计数值
    :param counts:
    :param n:
    :return:
    '''
    value_key_pairs = [(count, tz) for tz, count in counts.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


if __name__ == "__main__":
    path = '../../data/dataSets/bitly_usagov/example.txt'
    # 使用列表推导式将读取的文件逐行遍历并使用json加载之后放置到列表中
    records = [json.loads(line) for line in open(path).readlines()]
    # print(records[0]['tz'])
    time_zones = [rec['tz'] for rec in records if 'tz' in rec]
    # print(time_zones[:10])
    counts = get_counts(time_zones)
    top_counts = top_counts(counts)
    # 获取前n位的时区及其计数值
    sort_dict = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
    # print(sort_dict[:10])
    # print(counts)
    counts = get_counts2(time_zones)
    # print(counts[1])
    # 使用Counter函数,自动聚合同一个key出现的次数,调用most_common返回topN
    counts = Counter(time_zones)
    top_n = counts.most_common(10)
    # print(top_n)
    frame = DataFrame(records)
    # print(frame['tz'],frame['tz'].value_counts())
    # print(frame.info(),frame.describe())
    # fillna可以替换Nan
    clean_tz = frame['tz'].fillna('Missing')
    clean_tz[clean_tz == ''] = 'Unkonwn'
    tz_counts = clean_tz.value_counts()
    # print(tz_counts)
    tz_counts[:5].plot(kind='barh', rot=0)
    # plt.show()

    # 获取数据中最常出现的时区
    result = Series([i.split()[0] for i in frame.a.dropna()])
    # print(result.value_counts()[:10])
    c_frame = frame[frame.a.notnull()]
    operator_system = np.where(c_frame['a'].str.contains('Windows'), 'Windows', 'Not Windows')
    # print(operator_system[:10])
    by_tz_os = c_frame.groupby(['tz', operator_system])
    agg_counts = by_tz_os.size().unstack().fillna(0)
    # print(agg_counts[:10])
    index = agg_counts.sum(1).argsort()
    # print(index[:10])

    count_subset = agg_counts.take(index)[-10:]
    # print(count_subset)
    count_subset.plot(kind='barh', stacked=True)
    # plt.show()
    normed_subset = count_subset.div(count_subset.sum(1), axis=0)
    normed_subset.plot(kind='barh', stacked=True)
    plt.show()
