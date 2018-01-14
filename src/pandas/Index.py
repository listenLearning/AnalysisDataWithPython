#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from pandas_datareader import data as web
from numpy import nan as NA


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
    # print(frame, '\n')
    # print(frame.sort_values(by=['b', 'a']))

    # # 排名(ranking)跟排序关系密切,且它会增设一个排名值(从1开始,一直到数组中有效数据的数量),它与numpy.argsort产生的简介排序索引差不多,
    # # 只不过它可以根据某种规则破坏平级关系
    # # 默认情况下,pandas的rank方法是通过"为各组分配一个平均排名"的方式破坏平级关系的
    obj = Series([7, -5, 7, 4, 2, 0, 4])
    # print(obj.rank())
    # # 也可以根据值在原数据中出现的顺序给出排名
    # print(obj.rank(method='first'))
    # # 按降序进行排名
    # print(obj.rank(ascending=False, method='max'))
    # # DF可以在列或行上计算排名
    frame = DataFrame({'b': [4.3, 7, -3, 2], 'a': [0, 1, 0, 1], 'c': [-2, 5, 8, -2.5]})
    # print(frame, '\n')
    # print(frame.rank(axis=1))

    # # 带有重复值的轴索引
    # # 虽然许多pandas函数(如reindex)都要求标签唯一,但这并不是强制性的.
    obj = Series(range(5), index=['a', 'a', 'b', 'b', 'c'])
    # print(obj, '\n')
    # # 索引的is_unique属性可以验证它的值是否是唯一的
    # print(obj.index.is_unique)
    # # 对于带有重复值的索引,数据选取的行为将会有些不同.如果某个索引对应多个值,则返回一个Series,而对应单个值的,则返回一个标量值
    # print(obj['a'], '\n','c:', obj['c'])
    # # 对DF进行索引时也是如此
    df = DataFrame(np.random.randn(4, 3), index=['a', 'a', 'b', 'b'])
    # print(df)
    # print(df.ix['a'])

    # # 会综合计算描述统计
    # # pandas对象拥有一组常用的数学和统计方法.它们大部分都属于约简和汇总统计,用于从Series中提取单个值或从DF的行和列中提取一个Series.
    # # 跟对应的Numpy数组方法相比,它们都是基于没有确实数据的假设而构建的
    df = DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]], index=['a', 'b', 'c', 'd'],
                   columns=['one', 'two'])
    # print(df)
    # # 调用DF的sum方法将会返回一个含有列小计的Series
    # print(df.sum())
    # # 传入axis=1将会按行进行求和运算
    # print(df.sum(axis=1))
    # # na值会自动被排除,除非整个切片(指行和列)都是NA,通过skipna选项可以禁用该功能
    # print(df.mean(axis=1, skipna=False))
    # # 有些方法(如idxmin和idxmax)返回的是间接统计(比如达到最小值或最大值的索引)
    # print(df.idxmax())
    # # 另一些方法则是累计型的
    # print(df.cumsum())
    # # 还有一种方法,既不是约简也不是累计,describe就是一个例子,它用于一次性产生多个汇总统计
    # print(df.describe())
    # # 对于非数值型数据,describe会产生另一种汇总统计
    obj = Series(['a', 'a', 'b', 'c'] * 4)
    # print(obj.describe())

    # # 相关系数与协方差:src/pandas/相关系数与协方差.ipynb

    # # 唯一值,值计数以及成员资格
    # # 还有一类方法可以从一维Series的值中抽取信息
    obj = Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
    # # unique,获取Series中的唯一值数组
    # # 返回的唯一值是未排序的,如果需要的话,可以对结果再次进行排序
    uniques = obj.unique()
    # print(uniques)
    # # value_counts(): 用于计算一个Series中各值出现的频率
    # print(obj.value_counts())
    # # 为了便于查看,结果Series是按值频率降序排列的,value_counts还是一个顶级pandas方法,可用于任何数组或序列
    # print(pd.value_counts(obj.values, sort=False))
    # # isin: 用于判断矢量化集合的成员资格,可用于选取Series中或DataFrame列中数据的子集
    mask = obj.isin(['b', 'c'])
    # print(mask,'\n')
    # print(obj[mask])
    # # 如果希望得到DataFrame中多个相关列的一张柱状图.将pandas,value_counts传给该DF的apply函数,即可:
    data = DataFrame({'Qu1': [1, 3, 4, 3, 4],
                      'Qu2': [2, 3, 1, 2, 3],
                      'Qu3': [1, 5, 2, 4, 4]})
    # print(data, '\n')
    result = data.apply(pd.value_counts).fillna(0)
    # print(result)

    # # 处理缺失数据
    # # pandas的设计目标之一就是让缺失数据的处理任务尽量轻松,pandas对象上的所有描述统计都排除了缺失数据
    # # pandas使用浮点值Nan(Not a Number)表示浮点和非浮点数组中的趋势数据.他只是一个便于检测出来的标记而已
    string_data = Series(['aardvark', 'artichoke', np.nan, 'avocado'])
    # print(string_data,'\n')
    # print(string_data.isnull())
    string_data[0] = None
    # print(string_data.isnull())

    # # 滤除缺失数据
    # # 过滤掉缺失数据的办法有很多,但dropna可能会更实用一些,对于一个Series,dropna返回一个仅含飞控数据和索引值的Series
    data = Series([1, NA, 3.5, NA, 7])
    # print(data.dropna())
    # # 也可以通过布尔型索引达到这个目的
    # print(data[data.notnull()])
    # # 对于DF对象,dropna默认丢弃任何含有缺失值的行
    data = DataFrame([[1., 6.5, 3.], [1., NA, NA], [NA, NA, NA], [NA, 6.5, 3.]])
    # print(data,'\n')
    # print(data.dropna())
    # # 传入how='all'将只丢弃权威NA的哪些行,丢弃列只需传入axis=1
    # print(data.dropna(how='all'))
    # # 另一个滤除DF行的问题涉及事件序列数据,假设项留下一部分观测数据,可以用thresh参数实现
    df = DataFrame(np.random.randn(7, 3))
    df.ix[:4, 1] = NA
    df.ix[:2, 2] = NA
    # print(df)
    # print(df.dropna(thresh=3))

    # # 填充缺失数据
    # # 对于大多数情况而言,填充缺失数据,fillna方法是最主要的函数.通过一个常数调用fillna就会将缺失值替换为那个常数值
    # print(df.fillna(0))
    # # 若是通过一个字典调用fillna,就可以实现对不同的列填充不同的值
    # print(df.fillna({1: 0.5, 2: -1}))
    # # fillna默认会返回新对象,但也可以对现有对象进行就地修改
    _ = df.fillna(0, inplace=True)
    # print(df)
    # # 对reindex有效的那些插值方法也可以用于fillna
    df = DataFrame(np.random.randn(6, 3))
    df.ix[:2, 1] = NA
    df.ix[4:, 2] = NA
    # print(df)
    # print(df.fillna(method='ffill'))
    # print(df.fillna(method='ffill', limit=2))
    # # 使用平均值填充缺失数据
    data = Series([1., NA, 3.5, NA, 7])
    # print(data.fillna(data.mean()))

    # # 层次化索引
    # # 层次化索引是pandas的一项重要功能,它是你能在一个轴上拥有多个(两个以上)索引级别.抽象点说,它使你能以低维度形式处理高维度数据
    # # 创建一个Series,并用一个由列标或数组组成的列表作为索引
    data = Series(np.random.randn(10),
                  index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'], [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
    # # 这就是带有MutiIndex索引的Series的格式化输出形式,索引之间的"间隔"bi傲视"直接使用上面的标签"
    # print(data)
    # print(data.index)
    # # 对于一个层次化索引的对象,选取数据子集的操作很简单
    # print(data['b'], '\n')
    # print(data['b':'c'], '\n')
    # print(data.ix[['b','d']],'\n')
    # # 在"内层"中进行选取
    # print(data[:, 2])
    # # 层次化索引在数据重塑和基于分组的操作(如透视表生成)中扮演着重要的角色.比如,这段数据可以通过unstack方法被重新安排到一个DF中
    # print(data.unstack())
    # # unstack的逆运算是stack
    # print(data.unstack().stack())
    # # 对于DF,每条轴都可以有分层索引
    frame = DataFrame(np.arange(12.).reshape((4, 3)), index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                      columns=[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
    # print(frame)
    # # 各层都可以有名字(可以时字符串,也可以是别的Python对象).如果指定了名称,它们就会显示在控制台中输出(不要将索引名称跟轴标签混为一谈!!)
    frame.index.names = ['key1', 'key2']
    frame.columns.names = ['state', 'color']
    # print(frame)
    # # 有了部分的列索引,因此可以轻松选取列分组
    # print(frame['Ohio'])
    # # 单独创建MultiIndex然后复用
    pd.MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']], names=['state', 'color'])

    # # 重排分级顺序
    # # 有时需要重新调整某条轴上各级别的顺序,或根据指定级别上的值对数据进行排序.swaplevel接受两个级别编号或名称,并返回一个互换了级别的新对象(单数据不会发生变化)
    # print(frame.swaplevel('key1','key2'))
    # # 而sortlevel则根据单个戒备中的值对数据进行排序(稳定的).交换级别时,常常也会用到sortlevel,这样最终结果就是有序的了
    # print(frame.sortlevel(1), '\n')
    # print(frame.swaplevel(0, 1).sortlevel(0))
    # # 在层次化索引的对象上,如果索引是按字典方式从外到内排序(即调用sortlevel(0)或sort_index()的结果),数据选取操作的性能要好很多

    # # 根据级别汇总统计
    # # 许多对DF和Series的描述和汇总统计都有一个level选项,它用于指定在某条轴上求和的级别.
    # print(frame.sum(level='key2'))
    # print(frame.sum(level='color', axis=1))

    # # 使用DF的列
    # # 将DF的一个或多个列当作行索引来用,或者可能希望将行索引变成DF的列
    frame = DataFrame({'a': range(7), 'b': range(7, 0, -1), 'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'],
                       'd': [0, 1, 2, 0, 1, 2, 3]})
    # print(frame)
    # # DF的set_index函数会将其一个或多个列转换为行索引,并创建一个新的DF
    # # 默认情况下,变成行索引的列将从DF中移除
    frame2 = frame.set_index(['c', 'd'])
    # print(frame2)
    # # 将变成行索引的列保存下来
    # print(frame.set_index(['c', 'd'], drop=False))
    # # reset_index的功能跟set_index刚好相反,层次化索引的级别会被转移到列里面
    # print(frame2.reset_index())
