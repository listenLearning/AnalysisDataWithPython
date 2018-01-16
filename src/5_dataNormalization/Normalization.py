#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import DataFrame, Series
import pandas as pd
import numpy as np

if __name__ == "__main__":
    pd.set_option('display.width', 100000)
    # # 合并数据集
    # # # 数据库风格的DF合并
    # # # # 数据集的合并(merge)或链接(join)运算时通过一个或多个键将行连接起来的,这些运算时关系型数据库的核心.pandas的merge函数时对数据应用这些算法的主要切入点
    df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                     'data1': range(7)})
    df2 = DataFrame({'key': ['a', 'b', 'd'],
                     'data2': range(3)})
    # print(df1, '\n')
    # print(df2, '\n')
    # # # # 这是一种多对一的合并,DF1中的数据有多个被标记为a和b行,而df2中key列的每个值则进对应一行.对这些对象调用merge即可得到
    # print(pd.merge(df1,df2))
    # # # # 如果没有指定特定列进行连接,merge就会将重叠列的列名当作键,可以通过参数on指定
    # print(pd.merge(df1,df2,on='key'))
    # # # # 如果两个对象的列名不同,也可以分别进行指定
    df3 = DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                     'data1': range(7)})
    df4 = DataFrame({'rkey': ['a', 'b', 'd'],
                     'data2': range(3)})
    # print(pd.merge(df3,df4,left_on='lkey',right_on='rkey'))
    # # # # 默认情况下,merge做的是inner连接,其他方式还有left,right以及outer.外连接求取的是键的并集,组合了左连接和右连接的效果
    # print(pd.merge(df1,df2,how='outer'))
    # # # # 多对多的合并操作非常简单,无需额外操作,如下所示:
    df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                     'data1': range(6)})
    df2 = DataFrame({'key': ['a', 'b', 'a', 'b', 'd'],
                     'data2': range(5)})
    # print(df1,'\n')
    # print(df2,'\n')
    # print(pd.merge(df1,df2,on='key',how='left'))
    # # # # 多对多连接产生的是行的笛卡儿积.由于左边的DF有三个'b'行,右边的有2个,所以最终结果中就有6个b行.连接方式只影响出现在结果中的键
    # print(pd.merge(df1,df2,how='inner'))
    # # # # 要根据多个键进行合并,传入一个由列名组成的列表即可
    left = DataFrame({'key1': ['foo', 'foo', 'bar'],
                      'key2': ['one', 'two', 'one'],
                      'lval': [1, 2, 3]})
    right = DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                       'key2': ['one', 'one', 'one', 'two'],
                       'rval': [4, 5, 6, 7]})
    # # # # 结果中出现哪些键组合取决于所选的合并方式,可以这样理解:多个键形成一系列元组,并将其当作单个连接键
    # # # # 注意:在进行列-列连接时,df对象中的索引会被丢弃
    # print(pd.merge(left, right, on=['key1', 'key2'], how='outer'))
    # # # # 对于合并运算需要考虑的最后一个问题是对重复列名的处理.merge中的suffixex参数,用于指定附加到左右两个DF对象的重叠列名上的字符串
    # print(pd.merge(left, right, on='key1'), '\n')
    # print(pd.merge(left, right, on='key1', suffixes=('_left', '_right')))

    # # # 索引上的合并
    # # # # 有时候,DF中的连接键位于其索引中.在这种情况下,可以使用left_index=True或right_index=True以说明索引应该被用作连接键
    left1 = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
    right1 = DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
    # print(left1, '\n')
    # print(right1, '\n')
    # print(pd.merge(left1, right1, left_on='key', right_index=True))
    # print(pd.merge(left1, right1, left_on='key', right_index=True,how='outer'))
    # # # #  对于层次化索引,必须以列表的形式指明用作合并键的多个列
    lefth = DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                       'key2': [2000, 2001, 2002, 2001, 2002],
                       'data': np.arange(5.)})
    righth = DataFrame(np.arange(12).reshape((6, 2)), columns=['event1', 'event2'],
                       index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'],
                              [2000, 2000, 2000, 2000, 2001, 2002]])
    # print(lefth, '\n')
    # print(righth, '\n')
    # print(pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True))
    # print(pd.merge(lefth,righth,left_on=['key1','key2'],right_index=True,how='outer'))
    # # # # 合并双方的索引
    left2 = DataFrame([[1., 2.], [3., 4.], [5., 6.]], index=['a', 'c', 'e'], columns=['Ohio', 'Nevada'])
    right2 = DataFrame([[7., 8.], [9., 10.], [11., 12.], [13., 14]],
                       index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])
    # print(right2, '\n')
    # print(left2, '\n')
    # print(pd.merge(left2,right2,how='outer',left_index=True,right_index=True))
    # # # # Df还有一个join实例方法,它能更为方便地实现按索引合并.他还可以用于合并多个带有相同或相似索引的DF对象,而不管它们之间有没有重叠的列.
    # print(left2.join(right2,how='outer'))
    # # # # DF的join方法默认是在连接键上做的左连接,它还支持参数DF的索引跟调用者DF的某个列之间的连接
    # print(left1.join(right1,on='key'))
    # # # # 对于简单的索引合并,还可以向join传入一组DF
    another = DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17]], index=['a', 'c', 'e', 'f'],
                        columns=['New York', 'Oregon'])
    # print(left2.join([right2,another]))
    # print(left2.join([right2,another],how='outer'))

    # # # 轴向连接
    # # # # 另一种数据合并运算也被称作连接,绑定或堆叠.Numpy由一个用于合并原始numpy数组的concatenation函数
    arr = np.arange(12).reshape((3, 4))
    # print(arr)
    # np.concatenate([arr,arr],axis=1)
    s1 = Series([0, 1], index=['a', 'b'])
    s2 = Series([2, 3, 4], index=['c', 'd', 'e'])
    s3 = Series([5, 6], index=['f', 'g'])
    # # # # 对以上对象调用concat函数可以将值和索引粘和在一起
    # print(pd.concat([s1,s2,s3]))
    # # # # 默认情况下,concat实在axis=0上工作得,最终产生一个新的Series.如果传入axis=1,则结果就会变成一个DataFrame
    # print(pd.concat([s1,s2,s3],axis=1))
    # # # # 在上面的情况下,另一条轴上没有重叠,从索引的有序并集(外连接)上就可以看出来.传入join='inner'即可得到它们的交集
    s4 = pd.concat([s1 * 5, s3])
    # print(pd.concat([s1, s4], axis=1), '\n')
    # print(pd.concat([s1, s4], axis=1, join='inner'))
    # # # # 可以通过join_axes指定要在其他轴上使用的索引
    # print(pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']]))
    # # # # 参与连接的片段在结果中区分不开,假设要在连接轴上创建一个层次化索引,使用keys参数即可达到目的
    result = pd.concat([s1, s2, s3], keys=['one', 'two', 'three'])
    # print(result)
    # print(result.unstack())
    # # # # 沿着axis=1对Series进行合并,则keys就会成为DataFrame的列头
    # print(pd.concat([s1,s2,s3],axis=1,keys=['one','two','three']))
    # # # # 同样的逻辑对DF对象也是一样
    df1 = DataFrame(np.arange(6).reshape((3, 2)), index=['a', 'c', 'c'], columns=['one', 'two'])
    df2 = DataFrame(5 + np.arange(4).reshape((2, 2)), index=['a', 'c'], columns=['three', 'four'])
    # print(df1,'\n')
    # print(df2,'\n')
    # print(pd.concat([df1, df2],axis=1, keys=['level1', 'level2']))
    # # # # 如果传入的不是列表而是一个字典,则字典的键就会被当作keys选项的值
    # print(pd.concat({'level1': df1, 'level2': df2}))
    # # # # 用于管理层此话索引创建方式的参数
    # print(pd.concat([df1,df2],keys=['level1','level2'],names=['upper','lower']))
    # # # # 对于跟当前分析工作无关的DF行索引,可以通过参数ignore_index=True过滤掉
    df1 = DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
    df2 = DataFrame(np.random.rand(2, 3), columns=['b', 'd', 'a'])
    # print(df1, '\n')
    # print(df2, '\n')
    # print(pd.concat([df1, df2], ignore_index=True))

    # # # 合并重叠数据
    # # # # 还有一种数据组合问题不能用简单的合并或连接运算来处理,比如说,索引全部或部分重叠的两个数据集.
    a = Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan], index=['f', 'e', 'd', 'c', 'b', 'a'])
    b = Series(np.arange(len(a), dtype=np.float64), index=['f', 'e', 'd', 'c', 'b', 'a'])
    b[-1] = np.nan
    # print(a,'\n')
    # print(b,'\n')
    # print(np.where(pd.isnull(a),b,a))
    # # # # Series又一个combine_first方法,实现的也是类似np.where一样的功能,而且会进行数据对齐
    # print(b[:-2].combine_first(a[2:]))
    # # # # 对于DF,combine_first自然也会在列上做同样的事情,可以将其看作:用参数对象中的数据为调用者对象的缺失数据"打补丁"
    df1 = DataFrame({'a': [1., np.nan, 5., np.nan], 'b': [np.nan, 2., np.nan, 6.], 'c': range(2, 18, 4)})
    df2 = DataFrame({'a': [5., 4., np.nan, 3., 7.], 'b': [np.nan, 3., 4., 6., 8.]})
    # print(df1.combine_first(df2))

    # # 重塑和轴向旋转
    # # # # 有许多用于重新排列表格型数据的基础运算,这些函数也称作重塑(reshape)或轴向旋转(pivot)运算

    # # # 重塑层次化索引
    data = DataFrame(np.arange(6).reshape((2, 3)), index=pd.Index(['Ohio', 'Colorado'], name='state'),
                     columns=pd.Index(['one', 'two', 'Three'], name='number'))
    # print(data, '\n')
    # # # # 使用stack将列转为行,可以得到一个Series
    result = data.stack()
    # print(result)
    # # # # 对于一个层次化索引的Series,可以使用unstack将其重排为一个DF
    # print(result.unstack())
    # # # # 默认情况下,unstack操作的是最内存(stack也是如此).传入分层级别的编号或名称即可对其他级别进行unstack操作:
    # print(result.unstack(0),'\n')
    # print(result.unstack('number'))
    # # # # 如果不是所有的级别值都能在各分组中找到的话,unstack操作可能会引入缺失数据
    s1 = Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
    s2 = Series([4, 5, 6], index=['c', 'd', 'e'])
    data2 = pd.concat([s1, s2], keys=['one', 'two'])
    # print(data2)
    # print(data2.unstack())
    # # # # stack默认会滤除缺失数据,因此该运算是可逆的
    # print(data2.unstack().stack(), '\n')
    # print(data2.unstack().stack(dropna=False))
    # # # # 对DF进行unstack操作时,作为旋转轴的级别将会成为结果中的最低级别
    df = DataFrame({'left': result, 'right': result + 5}, columns=pd.Index(['left', 'right'], name='side'))
    # print(df)
    # print(df.unstack('state'),'\n')
    # print(df.unstack('state').stack('side'))

    # # # 将"长格式"旋转为"宽格式"
    # # # # 时间序列数据通常是以所谓的"长格式"(long)或"堆叠格式"(stacked)存储在数据库和CSV中的
    # # # # 关系型数据库中的数据经常都是这样存储的,因为固定架构(即列名和数据类型)有一个好处:随着表中数据的添加或删除,item列中的值的种类能够增加或减少.当然这也是优缺点的:长格式的数据操作起来可能不那么轻松,DF的pivot方法完全可以实现df和长格式数据的转换
    path = '../../data/examples/macrodata.csv'
    data = pd.read_csv(path)
    # print(data.head(), '\n')
    periods = pd.PeriodIndex(year=data.year, quarter=data.quarter, name='date')
    columns = pd.Index(['realgdp', 'infl', 'unemp'], name='item')
    data = data.reindex(columns=columns)
    # print(data.head(), '\n')
    data.index = periods.to_timestamp('D', 'end')
    ldata = data.stack().reset_index().rename(columns={0: 'value'})
    # print(ldata.head())
    pivoted = ldata.pivot('date', 'item', 'value')
    # print(pivoted.head())
    # # # # 前两个参数值分别用作行和列索引的列名,最后一个参数值则是用于填充DF的数据列的列名,假设有两个需要参与重塑的数据列
    ldata["value2"] = np.random.randn(len(ldata))
    # print(ldata[:10])
    # # # # 如果忽略最后一个参数,得到的DF就会带有层次化的列
    pivoted = ldata.pivot('date', 'item')
    # print(pivoted.head())
    # print(pivoted['value'].head())
    # # # # pivot只是一个快捷方式而已:用set_index创建层次化索引,再用unstack重塑
    unstacked = ldata.set_index(['date', 'item']).unstack('item')
    # print(unstacked[:7])

    # # 数据转换
    # # # 移除重复数据
    # # # # DF中经常会出现重复行,可以通过DF的duplicated方法返回一个布尔型Series,表示各行是否有重复行,
    data = DataFrame({'k1': ['one'] * 3 + ['two'] * 4, 'k2': [1, 1, 2, 3, 3, 4, 4]})
    # print(data)
    # print(data.duplicated())
    # # # # 还可以通过drop_duplicated方法移除重复行的df
    # print(data.drop_duplicates())
    # # # # 以上两个方法默认会判断全部列,也可以指定部分列进行重复项判断
    data['v1'] = range(7)
    # print(data.drop_duplicates('k1'))
    # # # # duplicated和drop_duplicates默认保留的时第一个出现的值组合.传入keep='last'则保留最后一个
    # print(data.drop_duplicates(['k1', 'k2'], keep='last'))

    # # # 利用函数或映射进行数据转换
    # # # # 在对数据集进行转换时,如果需要根据数组,Series或DataFrame列中的值来实现该转换工作
    data = DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami', 'corned beef', 'Bacon', 'pastrami',
                               'honey ham', 'nova lox'], 'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
    # print(data)
    meat_to_animal = {
        'bacon': 'pig',
        'pulled pork': 'pig',
        'pastrami': 'cow',
        'corned beef': 'cow',
        'honey ham': 'pig',
        'nova lox': 'salmon'
    }
    # # # # Series的map方法可以接受一个函数或含有映射关系的字典型对象
    data['animal'] = data['food'].map(str.lower).map(meat_to_animal)
    # print(data)
    # # # # 也可以传入一个能够完成全部这些工作的函数
    # # # # 使用map是一种实现元素级转换以及其它数据清理工作的便捷方式
    # print(data['food'].map(lambda x:meat_to_animal[x.lower()]))

    # # # 替换值
    # # # # 利用fillna方法填充缺失数据可以看作值替换的一种特殊情况.虽然map可以用于修改对象的数据子集,然而replace提供了一种实现该功能的更简单,更灵活的方式
    data = Series([1., -999., 2., -999., -1000., 3.])
    # print(data)
    # print(data.replace(-999., np.nan))
    # # # # 一次替换多个值
    # print(data.replace([-999.,-1000.], np.nan))
    # # # # 对不同的值进行不同的替换,则传入一个由替换关系组成的列表即可
    # print(data.replace([-999.,-1000.],[np.nan,0]))
    # # # # 传入的参数也可以是字典
    # print(data.replace({-999.: np.nan, -1000.: 0}))

    # # # 重命名轴索引
    # # # # 跟Series中的值一样,轴标签也可以通过函数或映射进行转换,从而得到一个新对象,轴还可以被就地修改,而无需新建一个数据结构
    data = DataFrame(np.arange(12).reshape((3, 4)),
                     index=['Ohio', 'Colorado', 'New York'],
                     columns=['one', 'two', 'three', 'four'])
    # # # # 同Series一样,轴标签也有一个map方法
    # print(data.index.map(str.upper))
    data.index = data.index.map(str.upper)
    # print(data)
    # # # # 如果想要创建数据及的转换版(而不是修改原始数据),比较使用的方法是rename
    # print(data.rename(index=str.title, columns=str.upper))
    # # # # rename可以结合字典型对象实现对部分轴标签的更新
    # print(data.rename(index={'OHIO': 'INDIANA'}, columns={'three': 'peekboo'}))
    # # # # rename帮我们实现了:复制DF并对其索引和列标签进行赋值.如果希望就地修改某个数据集,传入inplace=True即可
    _ = data.rename(index={'OHIO': 'INDIANA'}, inplace=True)
    # print(data)

    # # # 离散化和面元划分
    # # # # 为了便于分析,连续数据常常被离散化或拆分为'面元'(bin)
    age = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    # # # # 将这些age划分为"18-25,26-35,35-60,60+"几个面元,要实现该功能,需要用pandas的cut函数
    bins = [18, 25, 35, 60, 100]
    cats = pd.cut(age, bins)
    # print(cats)
    # # # # pandas返回的是一个特殊的Categories对象,可以将其看作一组表示面元名称的字符串.实际上,它还有一个表示不同分类名称的levels数组以及一个年龄数据进行行标号的labels属性
    # print(cats.codes)
    # print(cats.categories)
    # print(pd.value_counts(cats))
    # # # # 跟区间的数学符号一样,圆括号表示开端,而方括号则表示闭段,那边是闭端可以通过right=False进行修改
    # print(pd.cut(age, [18, 26, 36, 61, 100], right=False))
    # # # # 也可以设置面元名称,将labels选项设置为一个列表或数组即可
    group_names = ['Youth', 'YougAdult', 'MiddleAged', 'Senior']
    # print(pd.cut(age, bins, labels=group_names))
    # # # # 如果向cut传入的是面元的数量而不是确切的面元边界,则它会根据数据的最小值和最大值计算等长面元
    data = np.random.rand(20)
    # print(pd.cut(data, 4, precision=2))
    # # # # qcut是一个非常类似于cut的函数,它可以根据样本分位数对数据进行面元划分.根据数据分布情况,cut可能无法使各个面元中含有相同数量的数据点,而qcut由于使用的是样本分位数,因此可以得到大小基本相等的面元
    data = np.random.randn(1000)
    cats = pd.qcut(data, 4)  # 按四分位数进行切割
    # print(cats)
    # print(pd.value_counts(cats))
    # # # # 自定义分位数
    # print(pd.qcut(data, [0, 0.1, 0.5, 0.9, 1]))

    # # # 检测和过滤异常值
    # # # # 异常值的过滤或变换运算在很大程度上其实就是数组运算
    np.random.seed(0)
    data = DataFrame(np.random.randn(1000, 4))
    # print(data.describe())
    # # # # 找出某列绝对值大小超过3的值
    col = data[3]
    # print(col[np.abs(col)>3])
    # # # # 获取全部含有"超过3或-3的值"的行,可以利用布尔型DF以及any方法
    # print(data[(np.abs(data)>3).any(1)])
    # # # # 将值限制在区间-3到3以内
    data[np.abs(data)>3] = np.sign(data)*3
    print(data.describe())
