#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # # Series是一种类似于一维数组的对象,它由一组数据(各种Numpy数据类型)以及一组与之相关的数据标签(索引)组成
    # # Series的字符串表现形式为:索引在左,值在右.
    # # 如果没有为数据指定索引,Series会自动创建一个0到N-1的整数型索引,可以通过values和index属性获取其数组表现形式和索引对象
    obj = Series([4, 7, -5, 3])
    # print(obj.values)
    # print(obj.index)

    # # 创建带有一个可以对各个数据点进行标记的索引
    obj = Series([4, 7, -5, 3], index=['a', 'b', 'c', 'd'])
    # print(obj)
    # # 通过索引方式选取Series中的单个或一组值
    # print(obj[['a', 'c', 'd']])

    # # 数组运算会保留索引和值之间的链接
    # print(obj[obj > 2])
    # print(obj ** 2)
    # print(np.exp(obj))

    # # 可以将Series看成一个定长的有序字典,因为它是索引值到数据值得一个映射
    # print('b' in obj)

    # # 通过python字典来创建Series
    dict = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    obj1 = Series(dict)
    # print(obj1)

    # # 如果只传入一个字典,则结果Series中的索引就是原字典的键(有序排列)
    states = ['California', 'Ohio', 'Oregon', 'Texas']
    obj2 = Series(dict, index=states)
    # print(obj2)

    # # 检测缺失值
    # print(obj2.isnull(), '\n\n', obj2.notnull())

    # # Series在算数运算中会自动对齐相同索引的数据
    # print(obj1 + obj2)

    # # Series对象本身及其索引都有一个name属性,该属性跟pandas其他的关键功能非常密切
    obj2.name = 'population'
    obj2.index.name = 'state'
    # print(obj2)

    # # Series通过赋值的方式修改索引
    obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']
    print(obj)
