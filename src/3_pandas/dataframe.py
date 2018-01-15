#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

if __name__ == "__main__":
    print("")
    # # DataFrame是一个表格型的数据结构,它含有一组有序的列,每列可以是不同的值类型
    # # DataFrame既有行索引也有列索引,它可以被看作由Series组成的字典(共用同一个索引)
    # # 和其他类似的数据结构相比,DataFrame中面向行和面向列的操作基本上是平衡的
    # # DataFrame中的数据是以一个或多个二维块存放的
    dict = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
    frame1 = DataFrame(dict)
    # print(frame1)
    # # 如果指定了列序列,DataFrame的列就会按照指定顺序进行排列
    frame2 = DataFrame(dict, columns=['year', 'state', 'pop'])
    # print(frame2)

    # # 如果传入的列在数据中找不到,就会产生Nan值
    frame3 = DataFrame(dict, columns=['year', 'state', 'pop', 'debt'],
                       index=['one', 'two', 'three', 'four', 'five'])
    # print(frame3)

    # # 通过类似字典标记的方式或属性的方式,可以将DataFrame的列获取为一个Series
    # # 返回的Series拥有原DataFrame相同的索引,且其name属性也已经被相应地设置好了.
    # print(frame3['state'], '\n')
    # print(frame3.year,'\n')

    # # 行也可以通过位置或名称的方式进行获取,比如用索引字段ix
    # print(frame3.ix['three'])

    # # 列也可以通过赋值的方式进行修改
    frame3['debt'] = 16.5
    # print(frame3)
    frame3['debt'] = np.arange(5.)
    # print(frame3)

    # # 将列表或数组赋值给某个列时,其长度必须跟DF的长度相匹配.如果赋值的是一个Series,就会精确匹配DF的索引,所有的空位都将被填上缺失值
    val = Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
    frame3['debt'] = val
    # print(frame3)

    # # 为不存在的列赋值会创建出一个新列,关键字del用于删除列
    frame3['eastern'] = frame3.state == 'Ohio'
    # print(frame3)
    del frame3['eastern']
    # print(frame3.columns)

    # # 嵌套字典
    # # 如果将嵌套字典传给df,他就会被解释为:外层字典的键作为列,内层键则作为行索引
    pop = {'Nevada': {2001: 2.4, 2002: 2.9},
           'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    frame4 = DataFrame(pop)
    # print(frame4.T)

    # # 内层字典的键会被合并,排序以形成最终的索引,如果显示指定了索引,则不会这样
    # print(DataFrame(pop, index=[2001, 2002, 2003]))

    # # 由Series组成的字典差不多也是一样的用法
    pdata = {'Ohio': frame4['Ohio'][:-1],
             'Nevada': frame4['Nevada'][:2]}
    # print(DataFrame(pdata))

    # # 如果设置了df的index和Columns的name属性,这些信息也会被显示出来
    frame4.columns.name = 'state'
    frame4.index.name = 'year'
    # print(frame4)

    # # 同Series,values属性也会以二维ndarray的形式返回df中的数据
    # print(frame4.values)

    # # 如果df各列的数据类型不同,则值数组的数据类型就会选用能兼容所有列的数据类型
    # print(frame3.values)