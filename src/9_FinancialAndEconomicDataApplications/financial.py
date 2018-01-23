#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from datetime import datetime, time
from pandas_datareader import data as web

if __name__ == "__main__":
    pd.set_option('display.width', 10000)
    np.random.seed(0)
    path1 = '../../data/examples/stock_px.csv'
    path2 = '../../data/examples/volume.csv'
    prices = pd.read_csv(path1, parse_dates=True, index_col=0)
    volume = pd.read_csv(path2, parse_dates=True, index_col=0)
    prices = prices.loc['2011-09-05':'2011-09-14', ['AAPL', 'JNJ', 'SPX', 'XOM']]
    volume = volume.loc['2011-09-05':'2011-09-12', ['AAPL', 'JNJ', 'XOM']]
    # # # # 计算成交量加权平均价格,由于pandas可以在算数中自动对其数据,并在sum这样的函数中排除缺失数据
    # print(prices * volume)
    vwap = (prices * volume).sum() / volume.sum()
    # print(vwap)
    # print(vwap.dropna())
    # # # # 如果希望手工进行对齐,可以使用DF的align方法,它返回的使一个元组,含有两个对象的重索引版本
    # print(prices.align(volume, join='inner'))
    # # # # 另一个不可或缺的功能是,通过一组索引可能不同的series构建一个df
    s1 = Series(range(3), index=['a', 'b', 'c'])
    s2 = Series(range(4), index=['d', 'b', 'c', 'e'])
    s3 = Series(range(3), index=['f', 'a', 'c'])
    data = DataFrame({'one': s1, 'two': s2, 'three': s3})
    # print(data)
    # # # # 显式定义结果的索引(丢弃其余的数据)
    data = DataFrame({'one': s1, 'two': s2, 'three': s3}, index=list('abcdef'))
    # print(data)

    # # # 频率不同的时间序列的运算
    # # # # resample用于将数据转换到固定频率,而reindex则用于使数据符合一个新索引.它们都支持插值(向前填充)逻辑
    ts1 = Series(np.random.randn(3), index=pd.date_range('2012-6-13', periods=3, freq='W-WED'))
    # print(ts1)
    # # # # 将其重采样到工作日频率,则那些没有数据的日子就会出现一个空洞
    # print(ts1.resample('B'))
    # # # # 处理较低频率的数据时可以调用ffill()方法用前面的值填充这些空白,因为最中结果中各个时间点都有一个最新的有效值
    ts2 = ts1.resample('B').ffill()
    # print(ts2)
    # # # # 如果要将ts1中"最当前"的值(即前向填充)加到ts2上.一个办法是将两者重采样为规整频率后再相加,但是如果想要维持ts2中的日期索引,则reindex回事一种更好的解决方案
    # print(ts1.reindex(ts2.index).ffill())
    # print(ts2+ts1.reindex(ts2.index).ffill())

    # # # 使用Period
    # # # # period(表示时间区间)提供了另一种处理不同频率时间序列的办法,尤其是那些有着特殊规范的一年或季度为频率的金融或经济序列
    gdp = Series([1.78, 1.94, 2.08, 2.01, 2.15, 2.31, 2.46],
                 index=pd.period_range('1984Q2', periods=7, freq='Q-SEP'))
    infl = Series([0.025, 0.045, 0.037, 0.04],
                  index=pd.period_range('1982', periods=4, freq='A-DEC'))
    # print(gdp,'\n')
    # print(infl)
    # # # # 跟timestamp的时间序列不同,由period索引的两个不同频率的时间序列之间的运算必须进行显式转换
    infl_q = infl.asfreq('Q-SEP', how='E')
    # print(infl_q)
    # # # # 这个时间序列就可以被重新索引了(使用前向填充以匹配GDP)
    # print(infl_q.reindex(gdp.index).ffill())

    # # # 时间和"最当前"数据选取
    # # # # 生成一个交易日内的日期范围和时间序列
    rng = pd.date_range('2012-06-01 09:30', '2012-06-01 15:59', freq='T')
    # # # # 生成5天的时间点(9:30~15:59之间的值)
    rng = rng.append([rng + pd.offsets.BDay(i) for i in range(1, 4)])
    ts = Series(np.arange(len(rng), dtype=float), index=rng)
    # print(ts)
    # # # # 利用python的datetime.time对象进行索引即可抽取这些时间点上的值
    # print(ts[time(10, 0)])
    # # # # 实际上,该操作用到了实例方法at_time(各时间序列以及类似的DF对象都有)
    # print(ts.at_time(time(10,0)))
    # # # # 还有一个between_time方法,它用于选取两个Time对象之间的值
    # print(ts.between_time(time(10, 0), time(10, 1)))
    # # # # 如果正好没有任何数据落在某个具体的时间上(比如上午10点).
    # # # # 将该事件序列的大部分内容随机设置为NA
    indexer = np.sort(np.random.permutation(len(ts))[700:])
    irr_ts = ts.copy()
    irr_ts[indexer] = np.nan
    # print(irr_ts['2012-06-01 09:50':'2012-06-01 10:00'])
    # # # # 如果将一组timestamp传入asof方法,就能得到这些时间点处(或其之前最近)的有效值(非NA)
    selection = pd.date_range('2012-06-01 10:00', periods=4, freq='B')
    # print(irr_ts.asof(selection))

    # # # 拼接多个数据源
    # # # # 在金融或经济领域,由几个经常出现的情况:1.在一个特定的时间点上,从一个数据源切换到另一个数据源,2.用另一个时间序列对当前时间序列中的缺失值"打补丁",4.将数据中的符号(国家,资产代码等)替换为实际数据
    # # # # 对于第一种情况,在特定时刻从一个时间序列切换到另一个,起始就是用pandas.concat将两个timseries或df对象合并到一起
    data1 = DataFrame(np.ones((6, 3), dtype=float), columns=['a', 'b', 'c'],
                      index=pd.date_range('6/12/2012', periods=6))
    data2 = DataFrame(np.ones((6, 3), dtype=float) * 2, columns=['a', 'b', 'c'],
                      index=pd.date_range('6/13/2012', periods=6))
    spliced = pd.concat([data1.loc[:'2012-06-14'], data2.loc['2012-06-15':]])
    # print(spliced)
    # # # # 假设data1缺失了data2中存在的某个时间序列:
    data2 = DataFrame(np.ones((6, 4), dtype=float) * 2, columns=['a', 'b', 'c', 'd'],
                      index=pd.date_range('6/13/2012', periods=6))
    spliced = pd.concat([data1.loc[:'2012-06-14'], data2.loc['2012-06-15':]])
    # print(spliced)
    # # # # conbine_first可以引入合并点之前的数据,这样也就扩展了'd'项的历史
    # # # # 由于data2没有关于2012-06-12的数据,所以也就没有值被填充到那一天
    spliced_filled = spliced.combine_first(data2)
    # print(spliced_filled)
    # # # # Df也有一个类似的方法update,特可以实现就地更新.如果只是想填充空洞,必须传入overwrite=False
    spliced.update(data2, overwrite=True)
    # print(spliced)
    # # # # 利用DF的索引机制直接对列进行设置会更简单一些
    cp_spliced = spliced.copy()
    cp_spliced[['a','c']] = data1[['a','c']]
    # print(cp_spliced)

    # # # 收益指数和累计收益
    # # # # 在金融领域中,收益通常指的使某资产介个的百分比变化
    price = web.get_data_yahoo('AAPL','2011-01-01')['Adj Close']
    print(price)