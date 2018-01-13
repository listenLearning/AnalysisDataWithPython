#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np


def f(x):
    return Series([x.min(), x.max()], index=['min', 'max'])


if __name__ == "__main__":
    pd.set_option('display.width', 10000)
    np.random.seed(0)
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
    # print(data.ix['Colorado', ['two', 'three']], '\n')
    # print(data.ix[['Colorado', 'Utah'], [3, 0, 1]], '\n')
    # print(data.ix[2], '\n')
    # print(data.ix[:'Utah', 'two'], '\n')
    # print(data.ix[data.three > 5, :3])

    # # 算数运算和数据对齐
    # # pandas最重要的一个功能是,它可以对不同索引的对象进行算数运算.在将对象相加时,如果存在不同的索引对,则结果的索引就是该索引对的并集
    # # 自动的数据对齐操作在不重叠的索引处引入了Nan值.缺失值会在算术运算过程中传播
    s1 = Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
    s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
    # print(s1, '\n')
    # print(s2, '\n')
    # print(s1 + s2)

    # # 对于DataFrame,对齐操作会同时发生在行和列上
    df1 = DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'), index=['Ohio', 'Texas', 'Colorado'])
    df2 = DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
    # print(df1, '\n')
    # print(df2, '\n')
    # # 把两个DF相加后会返回一个新的DF,其索引和列为原来那两个DF的并集
    # print(df1+df2)

    # # 在算术方法中填充值
    # # 在对不同索引的对象进行算术运算时,你可能希望当一个对象中某个轴标签在另一个对象中找不到时填充一个特殊值(比如0)
    df1 = DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
    df2 = DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))
    # print(df1, '\n')
    # print(df2, '\n')
    # print(df1 + df2)
    # # 使用df1的add方法,传入df2以及一个fill_value参数
    # print(df1.add(df2, fill_value=0))

    # # 与此类似,在对Series或DataFrame重新索引时,也可以指定一个填充值
    # print(df1.reindex(columns=df2.columns, fill_value=0))

    # # DataFrame和Series之间的运算
    # # 和Numpy数组一样,DataFrame和Series之间算数运算也是有明确规定的.
    arr = np.arange(12.).reshape((3, 4))
    # print(arr, '\n')
    # print(arr[0], '\n')
    # print(arr - arr[0], '\n')
    frame = DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
    series = frame.ix[0]
    # print(frame, '\n')
    # print(series, '\n')
    # # 默认情况下,DF和Series之间的算数运算会将Series的索引匹配到DF的列,然后沿着行一直向下广播
    # print(frame - series)
    # # 如果某个索引值在DataFrame的列或Series的索引中找不到,则参与运算的两个对象就会被重新索引以形成并集
    series2 = Series(range(3), index=['b', 'c', 'd'])
    # print(frame+series2)

    # # 匹配行且在列上广播,就必须使用算术运算方法,传入的轴号就是希望匹配的轴
    series3 = frame['d']
    # print(frame.sub(series3, axis=0))

    # # 函数应用和映射
    # # numpyde ufuncs(元素级数组方法)也可以用于操作pandas对象
    frame = DataFrame(np.random.randn(4, 3), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
    # print(frame)
    # print(np.abs(frame))

    # # 另一种常见的操作是,将函数应用到由各列或行所形成的一维数组上.DataFrame的apply方法即可实现此功能
    f = lambda x: x.max() - x.min()

    # print(frame.apply(f), '\n')
    # print(frame.apply(f, axis=1))

    # # 许多最为常见的数组统计功能都被实现成DF的方法,因此无需使用apply方法
    # # 除标量值外,传递给apply的函数还可以返回有多个值组成的Series
    # print(frame.apply(f))

    # # 此外,元素级的Python函数也是可以用的.假如想得到frame中各个浮点值的格式化字符串,使用applymap即可
    # # 之所以叫applymap,是因为有一个用于应用元素级函数的map方法
    format = lambda x: '%.2f' % x
    # print(frame.applymap(format))
    # print(frame['e'].map(format))

    # # 排序和排名
    # # 根据条件对数据集排序(sorting)也是一种重要的内置运算.要对行或列索引进行排序(按字典排序),可以使用sort_index方法,它将返回一个已排序的新对象
    obj = Series(range(4), index=['d', 'a', 'b', 'c'])
    # print(obj.sort_index())

    # # 对于DF而言,则可以根据任意一个轴上的索引进行排序
    frame = DataFrame(np.arange(9).reshape((3, 3)), index=['3', '1', '0'], columns=['d', 'a', 'b'])
    # print(frame, '\n')
    # print(frame.sort_index(), '\n')
    # print(frame.sort_index(axis=1))
    # # 数据默认是按升序排序的,但也可以降序排列
    # print(frame.sort_index(axis=1, ascending=False))
    # # 若要按值对Series进行排序,可使用sort_values方法
    obj = Series([4, 7, -3, 2])
    # print(obj.sort_values())
    # # 在排序时,任何缺失值默认都会被放到Series末尾
    obj = Series([4, np.nan, 7, np.nan, -3, 2])
    # print(obj,'\n')
    # print(obj.sort_values(ascending=False))
    # # 在DF上,根据一个或多个列中的值进行排序.将一个或多个列的名字传递给by选项即可
    frame = DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
    print(frame, '\n')
    print(frame.sort_values(by=['b', 'a']))
