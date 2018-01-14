#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = "Ng WaiMing"

from pandas import Series, DataFrame
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # # 整数索引
    # # 整数索引的pandas对象跟内置的python数据结构(如列表和元组)在索引语义上有些不同,例如下面的例子
    ser = Series(np.arange(3.))
    # print(ser[-1])
    # # 在上面的情况下,虽然pandas会'求助于'整数索引,但没有那种方法能够既不引入任何bug又安全有效地解决该问题,
    # # 在上面的例子,我们又一个含有0,1,2的索引,但是很难推断出用户想要些什么(基于标签或位置的索引)

    # # 相反,对于一个非整数索引,就没有这样的歧义
    ser2 = Series(np.arange(3.), index=list('abc'))
    # print(ser2)
    # print(ser2[-1])
    # # 为了保持良好的一致性,如果轴索引含有索引器,那么根据证书进行数据选取的操作将总是面向标签的.
    # print(ser.ix[:1])
    # # 如果需要可靠的,不考虑索引类型的,基于位置的索引,可以使用Series的iat和iloc方法和DF的irow和icol方法
    ser3 = Series(range(3), index=[-5, 1, 3])
    # print(ser3.iat[2], '<==>', ser3.iloc[2])

    # # 面板数据: src/pandas/面板数据.ipynb
