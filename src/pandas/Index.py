#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # # 索引对象
    # # pandas的索引对象负责管理轴标签和其他元数据(比如轴名称等等).构建Series或DF时,所用到的任何数组或其他序列的标签都会被转换成一个Index
    obj = Series(range(3), index=['a', 'b', 'c'])
    index = obj.index
    # print(index)
    # print(index[1:])

    # # 不可修改性非常重要,因为这样才能使Index对象在多个数据结构之间安全共享
    Index = pd.Index(np.arange(3))
    obj2 = Series([1.5, -2.5, 0], index=Index)
    # print(obj2.index is Index)

    # # 除了长得像数组,index的功能也类似一个固定大小的集合
    pop = {'Nevada': {2001: 2.4, 2002: 2.9},
           'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    frame4 = DataFrame(pop)
    frame4.columns.name = 'state'
    frame4.index.name = 'year'
    # print('Ohio' in frame4.columns)
    # print(2000 in frame4.index)

    # # 重新索引
    # # pandas的一个重要方法时reindex,其作用是创建一个适应新索引的新对象
    obj3 = Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
    # print(obj3)
    obj4 = obj3.reindex(['a', 'b', 'c', 'd', 'e'])
    # print(obj4)
    obj5 = obj3.reindex(['a', 'b', 'c', 'd', 'e'], fill_value=0)
    # print(obj5)

    # # 对于时间序列这样的有序数据,重新索引时可能需要做一些差值处理.method选项即可达到此目的
    obj6 = Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
    # print(obj6.reindex(range(6), method='ffill'))

    # # 对于DF,reindex可以修改(行)索引,列,或者两个都修改,如果出啊内一个序列,则会重新索引行
    frame = DataFrame(np.arange(9).reshape((3, 3)), index=['a', 'c', 'd'], columns=['Ohio', 'Texas', 'California'])
    # print(frame)
    frame2 = frame.reindex(['a', 'b', 'c', 'd'])
    # print(frame2)
    # # 使用columns关键字即可重新索引列
    states = ['Texas', 'Utah', 'California']
    # print(frame.reindex(columns=states))

    # # 也可以同时对行和列进行重新索引,而插值则只能按行应用(即轴0)
    # print(frame.reindex(['a', 'b', 'c', 'd'],  method='ffill', columns=states))

    # # 利用ix的标签索引功能,重新索引任务可以变得更简洁
    # print(frame.ix[['a', 'b', 'c', 'd'], states])

    # # 丢弃指定轴上的项
    # # 丢弃某条轴上的一个或多个项很简单,只要由一个索引数组或列表即可.由于需要执行一些数整理和集合逻辑,所以drop方法返回的是一个在指定轴上删除了指定值的新对象
    obj = Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
    new_obj = obj.drop(['c', 'd'])
    # print(new_obj)

    # # 对于DF,可以删除任意轴上的索引值
    data = DataFrame(np.arange(16).reshape((4, 4)),
                     index=['Ohio', 'Colorado', 'Uath', 'New York'],
                     columns=['one', 'two', 'three', 'four'])
    # print(data.drop(['Colorado', 'Ohio']))
    # print(data.drop('two', axis=1))

    # # 索引、选取和过滤
    # # Series索引(obj[...])的工作方式类似于Numpy数组的索引,只不过Series的索引值不只是整数
    obj = Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
    # print(obj)
    # print(obj['b'], '<==>', obj[1])
    # print(obj[2:4], '<==>', obj[['b', 'c']])
    # print(obj[[1, 3]], '\n')
    # print(obj[obj < 2])

    # # 利用标签得切片运算于普通的python切片运算不同,其末端是包含的(inclusive)
    # print(obj['b':'c'])
    obj['b':'c'] = 5
    # print(obj)

    # # 对DF进行索引其实就是获取一个或多个列
    data = DataFrame(np.arange(16).reshape((4, 4)),
                     index=['Ohio', 'Colorado', 'Utah', 'New York'],
                     columns=['one', 'two', 'three', 'four'])
    # print(data['two'], '\n')
    # print(data[['two', 'three']], '\n')
    # print(data[data['three'] > 5], '\n')
    # print(data[:2], '\n')
    data[data < 5] = 0
    # print(data)

    # # 为了在DF的行上进行标签索引,可以使用索引字段ix.它使你可以通过Numpy式的标记法以及轴标签从DF中选取行和列的子集
    print(data.ix['Colorado', ['two', 'three']], '\n')
    print(data.ix[['Colorado', 'Utah'], [3, 0, 1]], '\n')
    print(data.ix[2], '\n')
    print(data.ix[:'Utah', 'two'], '\n')
    print(data.ix[data.three > 5, :3])
