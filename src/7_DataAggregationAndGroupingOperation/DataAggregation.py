#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import DataFrame, Series
import pandas as pd
import numpy as np


def peak_to_peak(arr):
    return arr.max() - arr.min()


if __name__ == "__main__":
    np.random.seed(0)
    pd.set_option('display.width', 100000)
    df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                    'key2': ['one', 'two', 'one', 'two', 'one'],
                    'data1': np.random.randn(5),
                    'data2': np.random.randn(5)})
    # print(df, '\n')
    # # # # 按key1进行分组,并计算data1列的平均值
    grouped = df['data1'].groupby(df['key1'])
    # # # # 变量grouped是一个GroupBy对象.它实际上还没有进行任何计算,只是含有一些有关分组建df['key1']的中间数据而已.即,grouped已经有了接下来对各组执行运算所需的一切信息
    # # # # 数据(Series)根据分组键进行了聚合,产生了一个新的Series,其索引为key1列中的唯一值.之所以结果索引的名字为key1,是因为原始DF的列df['key1']就叫这个名字
    # print(grouped.mean())
    # # # # 一次传入多个数组,通过两个键对数据进行了分组,得到的Series具有一个层次化索引(由唯一的键对组成)
    means = df['data1'].groupby([df['key1'], df['key2']]).mean()
    # print(means)
    # # # # 分组键可以是任何长度适当的数组
    states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
    years = np.array([2005, 2005, 2006, 2005, 2006])
    # print(df['data1'].groupby([states,years]).mean())
    # # # # 将列名(可以是字符串,数字或其它python对象)用作分组键
    # print(df.groupby('key1').mean())
    # print(df.groupby(['key1','key2']).mean())
    # # # # groupby的size返回一个含有分组大小的series
    size = df.groupby(['key1', 'key2']).size()
    # print(size)

    # # # 对分组进行迭代
    # # # # Groupby对象支持迭代,可以产生一组二元元组(由分组名和数据块组成).
    # for name,group in df.groupby('key1'):
    #     print(name)
    #     print(group)
    # # # # 对于多重键的情况,元组的第一个元素将会是由键值组成的元组
    # for (k1,k2),group in df.groupby(['key1','key2']):
    #     print(k1,k2)
    #     print(group)
    # # # # 将数据片段做成一个字典
    pieces = dict(list(df.groupby('key1')))
    # print(pieces['b'])
    # # # # groupby默认实在axis=0上进行分组的,通过设置也可以在其他任何轴上进行分组
    # print(df.dtypes)
    grouped = df.groupby(df.dtypes, axis=1)
    dic = dict(list(grouped))
    # print(dic)

    # # # 选取一个或一组列
    # # # # 对于由DF产生的groupby对象,如果用一个(单个字符串)或一组(字符串数组)列名对其进行索引.就能实现选取部分列进行聚合的目的
    # print(df['data1'].groupby(df['key1']))
    # print(df[['data2']].groupby(df['key1']))
    # # # # 尤其对于大数据集,很可能只需要对部分列进行聚合.例如,在前面那个数据集中,如果只需要计算data2列的平均值并以DF形式得到结果:
    # print(df.groupby(['key1','key2'])[['data2']].mean())
    # # # # 这种索引操作返回的对象是一个已分组的DF(如果传入的是列表或数组)或已分组的Series(如果传入的是标量形式的单个列名):
    s_grouped = df.groupby(['key1', 'key2'])['data2']
    # print(s_grouped.mean())

    # # # 通过字典或Series进行分组
    # # # # 除数组以外,分组信息还可以其它形式存在.
    people = DataFrame(np.random.randn(5, 5),
                       columns=['a', 'b', 'c', 'd', 'e'],
                       index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
    people.loc[2:3, ['b', 'c']] = np.nan
    # print(people)
    # # # # 假设一直列的分组关系,并希望根据分组计算列的总计:
    mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
               'd': 'blue', 'e': 'red', 'f': 'orange'}
    # # # # 将上面这组字典传给groupby即可:
    by_column = people.groupby(mapping, axis=1)
    # print(by_column.sum())
    # # # # Series也有同样的功能,它可以被看作一个固定大小的映射,对于上面那个例子,如果用Series作为分组键,则pandas会检查Series以确保其索引跟分组轴对齐的:
    map_series = Series(mapping)
    # print(people.groupby(map_series, axis=1).count())
    # # # 通过函数进行分组
    # # # # 相较于字典或Series,python函数在定义分组映射关系时可以更有创意且更为抽象.任何被当作分组键的函数都会在各个索引值上被调用一次,其返回值就会被用作分组名称.
    # print(people.groupby(len).sum())
    # # # # 将函数跟数组,列表,字典,Seris混合使用也不是问题,因为任何东西最终都会被转换为数组
    key_list = ['one', 'one', 'one', 'two', 'two']
    # print(people.groupby([len,key_list]).min())

    # # # 根据索引级别分组
    # # # # 层次化索引数据集最方便的地方就在于它能够根据索引级别进行聚合.要实现该目的,通过level关键字传入级别编号或名称即可
    columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'], [1, 3, 5, 1, 3]], names=['cty', 'tenor'])
    hier_df = DataFrame(np.random.randn(4, 5), columns=columns)
    # print(hier_df)
    # print(hier_df.groupby(level='cty',axis=1).count())

    # # # 数据聚合
    # # # # 许多常见的聚合运算都有就地计算数据集统计信息的优化实现
    grouped = df.groupby('key1')
    # # # # groupby会高效地对series进行切片,然后对各片调用piece.quantile(0.9),最后将这些结果组装成最终结果
    # print(grouped['data1'].quantile(0.9))
    # # # # 要使用自定义聚合函数,只需将其传入aggregate或agg方法即可
    # print(grouped.agg(peak_to_peak))
    # # # # 有些方法(如describe)也是可以用在这里的,即使严格来讲,它们并非聚合运算:
    # print(grouped.describe())
    # # # 案例:
    tips = pd.read_csv('../../data/examples/tips.csv')
    tips['tip_pct'] = tips['tip'] / tips['total_bill']
    # print(tips.head())

    # # # 面向列得多函数应用
    # # # # 对Series或DF列得聚合运算其实就是使用aggregate(使用自定义函数)或嗲用诸如mean,std之类的方法.然而,如何针对不同的列使用不同的聚合函数,或一次应用多个函数?
    grouped = tips.groupby(['sex', 'smoker'])
    grouped_oct = grouped['tip_pct']
    # print(grouped_oct.agg('mean'))
    # # # # 如果传入一组函数或函数名,得到的DF的列就会以相应的函数命名
    # print(grouped_oct.agg(['mean','std',peak_to_peak]))
    # # # # 并非一定要接受groupby自动给出的那些列名,特别是lambda函数,他们的名称是'<lambda>',这样的辨识度就很低了.如果传入的是一个由(name,function)猿族组成的列表,则各元组的第一个元素就会被用作DF列名
    # print(grouped_oct.agg([('foo','mean'),('bar',np.std)]))
    # # # # 对于DF,还可以定义一组应用于全部列的函数,或不同的列应用不同的函数.
    functions = ['count', 'mean', 'max']
    result = grouped['tip_pct', 'total_bill'].agg(functions)
    # print(result)
    # # # # 结果DF拥有层次化的列,相当于分别对各列进行聚合,然后用concat将结果组装到一起(列名用作keys参数)
    # print(result['tip_pct'])
    # # # # 这里也可以传入带有自定义名称的远足列表
    ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
    # print(grouped['tip_pct','total_bill'].agg(ftuples))
    # # # # 要对不同的列应用不同的函数.具体的办法是向agg传入一个从列明映射到函数的字典:
    # print(grouped.agg({'tip':np.max,'size':'sum'}))
    # print(grouped.agg({'tip_pct':['min','max','mean','std'],'size':'sum'}))

    # # # 以"无索引"的形式返回聚合数据
    # # # # 由于并不总是需要聚合数据都由唯一的分组键组成索引(可能还是层次化的),可以向groupby传入as_index=False以禁用该功能
    # print(tips.groupby(['sex','smoker'],as_index=False).mean())

    # # # 分组级运算和转换
    # # # # 聚合不过是分组运算的其中一种而已,它是数据转换的一个特例.即,它接受能够将一维数组简化为标量值的函数.
    # # # # transform和apply方法能够执行更多其它的分组运算
    # # # # 例1:假设想要为一个DF添加一个用于存放各索引分组平均值的列,其中一个办法是先聚合再合并
    # print(df)
    k1_means = df.groupby('key1').mean().add_prefix('mean_')
    # print(k1_means)
    print(pd.merge(df,k1_means,left_on='key1',right_index=True))
