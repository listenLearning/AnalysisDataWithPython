#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import statsmodels.api as sm
from matplotlib import pyplot as plt

def peak_to_peak(arr):
    return arr.max() - arr.min()


def demean(arr):
    return arr - arr.mean()


def top(df, n=5, column='tip_pct'):
    return df.sort_values(by=column)[-n:]


def get_stats(group):
    return ({'min': group.min(), 'max': group.max(), 'count': group.count(), 'mean': group.mean()})


def draw(deck, n=5):
    return deck.take(np.random.permutation(len(deck))[:n])


def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params


def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    # 根据key对totals进行降序排列
    return totals.sort_values(ascending=False)[:n]


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
    # print(pd.merge(df,k1_means,left_on='key1',right_index=True))
    # # # # 在groupby上使用transform
    key = ['one', 'two', 'one', 'two', 'one']
    # print(people.groupby(key).mean(),'\n')
    # # # # transform会将一个函数应用到各个分组,然后将结果放置到合适的位置上.如果各分组产生的是一个标量值,则该值就会被广播出去.
    # print(people.groupby(key).transform(np.mean))
    # # # # 从各组中减去平均值,为此,先创建一个距平化函数,然后将其传给transform
    demeaned = people.groupby(key).transform(demean)
    # print(demeaned)
    # # # # 查看各组平均值是否为0
    # print(demeaned.groupby(key).mean())

    # # # Apply:一般性的"拆分-应用-合并"
    # # # # 跟aggregate一样,transform也是一个有着严格条件的特殊函数,传入的函数只能产生两种结果,瑶妹产生一个可以广播的标量值(如np.mean),要么产生一个相同大小的结果数组.
    # # # # 最一般化的groupby方法是apply.apply会将待处理的对象拆分成多个片段,然后对各片段调用传入的函数,最后尝试将各片段组合到一起
    # # # # 例:根据分组选出最高的5各tip_pct值.首先,编写一个选取指定列具有最大值的行的函数
    # print(top(tips,n=6))
    # # # # 对smoker分组并用该函数调用apply
    # # # # top函数在DF的各个片段上调用,然后结果由pandas.concat组装到一起,并以分组名称进行了标记.于是,最终结果就有了一个层次化索引,其内层索引值来自原DF
    # print(tips.groupby('smoker').apply(top))
    # # # # 如果传给apply的函数能够接受其它参数或关键字,则可以将这些内容放在函数名后面一并传入
    # print(tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill'))
    result = tips.groupby('smoker')['tip_pct'].describe()
    # print(result,'\n')
    # print(result.unstack('smoker'))
    # # # # 在groupby中,调用诸如describe之类的方法时,实际上只是应用了下面两条代码的快捷方式而已
    f = lambda x: x.describe()
    grouped.apply(f)

    # # # 禁止分组键
    # # # # 分组键会跟原始对象的索引共同构成结果对象中的层次化索引,将group_keys=False传入groupby即可禁止该效果
    # print(tips.groupby('smoker',group_keys=False).apply(top))

    # # # 分位数和桶分析
    # # # # pandas有一些能够根据指定面元或样本分位数将数据拆分成多块的工具(比如cuthe qcut).将这些函数跟groupby结合起来,就能非常轻松地实现对数据集的桶(bucket)或分位数(quantile)分析了
    frame = DataFrame({'data1': np.random.randn(1000),
                       'data2': np.random.randn(1000)})
    factor = pd.cut(frame.data1, 4)
    # print(factor[:10], '\n')
    # # # #  由cut返回的factor对象可直接用于groupby,因此,可以像下面这样对data2做一些统计计算
    grouped = frame.data2.groupby(factor)
    # print(grouped.apply(get_stats).unstack(), '\n')
    # # # # 这些都是长度相等的桶,要根据样本分位数得到大小相等的桶,使用qcut即可.传入labels=False即可只获取分位数的编号
    grouping = pd.qcut(frame.data1, 10, labels=False)
    grouped = frame.data2.groupby(grouping)
    # print(grouped.apply(get_stats).unstack())

    # # # 示例:用于特定分组的值填充缺失值
    # # # # 对于缺失数据的清理工作,有时会用dropna将其过滤,而有时则可能希望用一个固定值或由数据集本身所衍生出来的值去填充NA值.这时就得使用fillna这个工具了
    s = Series(np.random.randn(6))
    s[::2] = np.nan
    # print(s)
    # print(s.fillna(s.mean()))
    # # # # 如果需要对不同的分组填充不同的值,只需将数据分组,并使用apply和一个能够对各数据块调用fillna的函数即可
    state = ['Ohio', 'New York', 'Vermont', 'Florida', 'Oregon', 'Nevada', 'California', 'Indaho']
    group_by = ['East'] * 4 + ['West'] * 4
    data = Series(np.random.randn(8), index=state)
    data[['Vermont', 'Nevada', 'Indaho']] = np.nan
    # print(data)
    # # # # 用分组平均值去填充NA值
    fill_mean = lambda g: g.fillna(g.mean())
    # print(data.groupby(group_by).apply(fill_mean))
    # # # # 此外,可以在代码中预定义各组的填充值,由于分组具有一个name属性,所以我们可以拿来用一下
    fill_values = {'East': 0.5, 'West': -1}
    fill_func = lambda g: g.fillna(fill_values[g.name])
    # print(data.groupby(group_by).apply(fill_func))

    # # # 示例:随机采样和排列
    # # # # 假设想要从一个大数据集中随机抽取样本以进行蒙特卡罗模拟或其他分析工作."抽取"的方式有很多,其中一些的效率会比其他的高很多.一个办法是,选取np.random.permutation(N)的前K个元素,其中N为完整数据的大小,K为期望的样本大小.
    # 红桃(Hearts),黑桃(Spades),梅花(Clubs),方片(Diamonds)
    suits = ['H', 'S', 'C', 'D']
    card_val = (list(range(1, 11)) + [10] * 3) * 4
    base_names = ['A'] + list(range(2, 11)) + ['J', 'K', 'Q']
    cards = []
    for suit in suits:
        cards.extend(str(num) + suit for num in base_names)
    deck = Series(card_val, index=cards)
    # print(deck)
    # print(draw(deck))
    # # # # 假设想要从每种花色中随机抽取两张牌.由于花色是牌名的最后一个字符,所以可以据此进行分组,并使用apply
    get_suit = lambda card: card[-1]  # 只要最后一个字母就可以了
    # print(deck.groupby(get_suit).apply(draw, n=2))
    # # # # 另一种办法
    # print(deck.groupby(get_suit, group_keys=False).apply(draw, n=2))

    # # # 分组加权平均数和相关系数
    # # # # 根据groupby的"拆分-应用-合并"范式,df的列于列之间或两个series之间的运算(比如分组加权平均)成为一种标准作业
    df = DataFrame({'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                    'data': np.random.randn(8),
                    'weights': np.random.rand(8)})
    # print(df)
    # # # # 利用category计算分组加权平均数
    grouped = df.groupby('category')
    get_wavg = lambda g: np.average(g['data'], weights=g['weights'])
    # print(grouped.apply(get_wavg))

    # # # 来自Yahoo!Finance的数据集
    close_px = pd.read_csv('../../data/examples/stock_px.csv', parse_dates=True, index_col=0)
    # print(close_px.head(1))
    # # # # 计算一个由日收益率(通过百分数变化计算)于SPX之间的年度相关系数组成的DF
    rets = close_px.pct_change().dropna()
    spx_corr = lambda x: x.corrwith(x['SPX'])
    by_year = rets.groupby(lambda x: x.year)
    # print(by_year.apply(spx_corr).head())
    # # # # 计算列与列之间的相关系数
    # print(by_year.apply(lambda g:g['AAPL'].corr(g['MSFT'])))

    # # # 示例:面向分组的线性回归
    # # # # 利用grouby执行更为复杂的分组统计分析,只要函数返回的是pandas对象或标量值即可.
    # # # # 例如:定义一个函数对各数据块执行普通最小二乘法回归
    # # # # 按年计算AAPL对SPX收益率的线性回归
    # print(by_year.apply(regress,'AAPL',['SPX']).head())

    # # # 透视表和交叉表
    # # # # 透视表是各种电子表格程序和其他数据分析软件中一种常见的数据汇总工具.他根据一个或多个键对数据进行聚合,并根据行和列上的分组键将数据分配到各个矩形区域中.在pandas中,可以通过groupby功能以及(能够利用层次化索引的)重塑运算制作透视表.DF有一个pivot_table方法,此外还有一个顶级的pandas.pivot_table函数.除能为groupby提供便利之外,pivot_table还可以添加分项小计(也叫margins)
    # # # # 根据sex和smoker计算分组平均数,并将sex和smoker放到行上
    # print(tips.pivot_table(index=['sex', 'smoker']))
    # # # # 聚合tip_pct和size,而且根据day进行分组
    # print(tips.pivot_table(['tip_pct','size'],index=['sex','day'],columns='smoker'))
    # # # # 对透视表做进一步处理,传入margins=True添加分项小计.这将会添加标签为all的行和列,其值对应于单个等级中所有数据的分组统计.
    # print(tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'], columns='smoker', margins=True))
    # # # # 要使用其他的聚合函数,将其传给aggfunc即可.例如,使用count或len即可得到有关分组大小的交叉表
    # print(tips.pivot_table('tip_pct', index=['sex', 'smoker'], columns='day', aggfunc=len, margins=True))
    # # # # 针对空值,可以设置fill_value
    # print(tips.pivot_table('size', index=['time', 'sex', 'smoker'], columns='day', aggfunc='sum', fill_value=0))

    # # # 交叉表:crosstab
    # # # # 交叉表是一种用于计算分组频率的特殊透视表
    data = pd.read_csv('../../data/examples/Wikipedia.csv')
    # # # # 根据性别和用手习惯对这段数据进行汇总统计,虽然用pivot_table可以实现该功能,但是用pandas.crosstab函数会更方便
    # print(pd.crosstab(data.Gender,data.Handedness,margins=True))
    # # # # crosstab的前两个参数可以是数组,Series或数组列表
    # print(pd.crosstab([tips.time,tips.day],tips.smoker,margins=True))

    # # # 示例:2010联邦选举委员会数据库
    fec = pd.read_csv('../../data/dataSets/fec/P00000001-ALL.csv', low_memory=False)
    # print(fec.info(),'\n')
    # print(fec.loc[123456])
    # # # # 通过unique获取全部的候选人名单
    unique_cands = fec.cand_nm.unique()
    # print(unique_cands)
    # # # # 利用字典说明党派关系
    parties = {'Bachmann, Michelle': 'Republican',
               'Cain, Herman': 'Republican',
               'Gingrich, Newt': 'Republican',
               'Huntsman, Jon': 'Republican',
               'Johnson, Gary Earl': 'Republican',
               'McCotter, Thaddeus G': 'Republican',
               'Obama, Barack': 'Democrat',
               'Paul, Ron': 'Republican',
               'Pawlenty, Timothy': 'Republican',
               'Perry, Rick': 'Republican',
               "Roemer, Charles E. 'Buddy' III": 'Republican',
               'Romney, Mitt': 'Republican',
               'Santorum, Rick': 'Republican'}
    # # # # 通过以上映射以及Series对象的map方法,可以根据候选人姓名得到一组党派信息
    # print(fec.cand_nm[123456:123461])
    fec['party'] = fec.cand_nm.map(parties)
    # print(fec['party'].value_counts())
    # # # # 注意,1.该数据既包括赞助也包括退款(负的出资额)
    # print((fec.contb_receipt_amt>0).value_counts())
    # # # # 为简化分析,限定该数据集只能由正的出资额
    fec = fec[fec.contb_receipt_amt > 0]
    # # # # 创建一个只包含主要候选人的子集
    fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

    # # # 根据职业和雇主计赞助信息
    # # # # 根据职业机算出资总额
    # print(fec.contbr_occupation.value_counts()[:10])
    occ_mapping = {
        'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
        'INFORMATION REQUESTED': 'NOT PROVIDED',
        'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
        'C.E.O.': 'CEO'
    }
    # # # # 如果没有提供相关映射,则返回x
    f = lambda x: occ_mapping.get(x, x)
    fec.contbr_occupation = fec.contbr_occupation.map(f)
    emp_mapping = {
        'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
        'INFORMATION REQUESTED': 'NOT PROVIDED',
        'SELF': 'SELF-EMPLOYED',
        'SELF EMPLOYED': 'SELF-EMPLOYED',
    }
    f = lambda x: emp_mapping.get(x, x)
    fec.contbr_employer = fec.contbr_employer.map(f)
    # # # # 通过pivot_table根据党派和职业对数据进行聚合,然后过滤掉总出资额不足200万美元的数据
    by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='party', aggfunc='sum')
    over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
    # print(over_2mm.head())
    # over_2mm.plot(kind='barh')
    # plt.show()
    # # # # 根据职业和估值进行聚合
    grouped = fec_mrbo.groupby('cand_nm')
    # print(grouped.apply(get_top_amounts, 'contbr_occupation', n=7))
    # print(grouped.apply(get_top_amounts, 'contbr_employer', n=10))

    # # # 对出资额分组
    # # # # 利用cut函数根据出资额的大小将数据离散化到多个面元中
    bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
    labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)
    # print(labels)
    # # # # 根据侯选人姓名以及面元标签对数据进行分组
    grouped = fec_mrbo.groupby(['cand_nm', labels])
    # print(grouped.size().unstack(0))
    bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
    # print(bucket_sums)
    normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
    # print(normed_sums)
    # normed_sums[:-2].plot(kind='barh',stacked=True)
    # plt.show()

    # # # 根据州统计赞助信息
    # # # # 根据候选人和州对数据进行聚合
    grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
    totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
    totals = totals[totals.sum(1) > 100000]
    # print(totals.head(10))
    # # # # 对各行除以总赞助额,就会得到各候选人在各州的总赞助额比例
    percent = totals.div(totals.sum(1), axis=0)
    # print(percent.head(10))
