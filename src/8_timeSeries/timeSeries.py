#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import calendar
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd
import pytz

if __name__ == "__main__":
    np.random.seed(0)
    pd.set_option('display.width', 10000)
    # # # 日期和时间数据类型及工具
    # # # # python标准库包含用于日期和时间数据的数据类型,而且还有日历方面的功能.之后会主要用到datetime,time和calendar模块.datetime.datetime是用的最多的数据类型
    now = datetime.now()
    # print(now,'\n')
    # print(now.year,now.month,now.day)
    # # # # datetime以毫秒形式存储日期和时间.datetime-datetime表示两个datetime对象之间的时间差
    delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
    # print(delta)
    # # # # 可以给datetime对象加上(或减去)一个或多个timedelta,这样会产生一个新对象
    start = datetime(2011, 1, 7)
    # print(start + timedelta(12))
    # print(start - 2 * timedelta(12))

    # # # 字符串和datetime的相互转换
    # # # # 利用str或strftime方法(传入一个格式化字符串),datetime对象和pandas的timestamp对象可以被格式化为字符串
    stamp = datetime(2011, 1, 3)
    # print(str(stamp),'\n')
    # print(stamp.strftime('%Y-%m-%d'))
    # # # # datetime.strptime也可以用这些格式化编码将字符串转换为日期
    value = '2011-01-03'
    # print(datetime.strptime(value, '%Y-%m-%d'), '\n')
    datestrs = ['7/6/2011', '8/6/2011']
    # print([datetime.strptime(x, '%m/%d/%Y') for x in datestrs])
    # # # # datetime.strptime是通过已知格式进行日期解析的最佳方式.但是每次都要编写格式定义是很麻烦的是情感,尤其是对一些常见的日期格式.在这种情况下,可以用dateutil这个第三方包中的parser.parse方法
    # print(parse('2011-01-03'))
    # # # # dateutil可以解析几乎所有人类能够理解的日期表示形式(中文除外)
    # print('PARSE:', parse('Jan 31, 1997 10:45 PM'))
    # # # # 在国际通用的格式中,日通常出现在月的前面,传入dayfirst=True即可解决这个问题
    times = parse('6/12/2011', dayfirst=True)
    # print(type(times))
    # # # # pandas通常是用于处理组成日期的,不管这些日期是DataFrame的轴索引还是列.to_datetime方法可以解析多种不同的日期表示形式.对标准日期格式(如ISO8601)的解析非常快
    # print(datestrs)
    # print(pd.to_datetime(datestrs))
    # # # # 处理缺失值
    # # # # NaT是pandas中时间戳数据的NA值
    idx = pd.to_datetime(datestrs + [None])
    # print(idx)
    # print(pd.isnull(idx))

    # # # 时间序列基础
    # # # # pandas最基本的时间序列类型就是以时间戳(通常以Pyhton字符串或datatime对象表示为索引的Series)
    dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7), datetime(2011, 1, 8),
             datetime(2011, 1, 10), datetime(2011, 1, 12)]
    ts = Series(np.random.randn(6), index=dates)
    # print(ts)
    # # # # 这些datetime对象实际上是被放在一个DatetimeIndex中的.变量ts就成为一个ImteSeries了
    # print(type(ts))
    # print(ts.index)
    # # # # 跟其它Series一样,不同索引的时间序列之间的算数匀速那会自动按日期对齐
    # print(ts + ts[::2])
    # # # # DatetimeIndex 中的各个标量值是pandas的Timestamp对象
    stamp = ts.index[0]
    # print(stamp)
    # # # # 只要有需要,timestamp可以随时自动转换为datetime对象.此外,它还可以存储频率信息,且直到如何执行时区转换以及其它操作.

    # # # 索引,选取,子集构造
    # # # # 由于TimeSeries是Series的一个子类,所以在索引以及数据选取方面它们的行为是一样的
    stamp = ts.index[2]
    # print(ts[stamp])
    # # # # 还有一种更为方便的用法:传入一个可以被解释为日期的字符串
    # print(ts['1/10/2011'])
    # print(ts['20110110'])
    # # # # 对于较长的时间序列,只需传入"年"或"年月"即可轻松选取数据的切片
    longer_ts = Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    # print(longer_ts.head())
    # print(longer_ts['2001'])
    # print(longer_ts['2001-05'])
    # # # # 通过日期进行切片的方式只对规则Series有效
    # print(ts[datetime(2011, 1, 7):])
    # # # # 由于大部分时间序列数据都是按照时间先后排序的,因此你也可以用不存在于该时间序列中的时间戳对其进行切片(即范围查询)
    # print(ts,'\n')
    # print(ts['1/6/2011':'1/11/2011'])
    # # # # 这里可以传入字符串日期,datetime或timestamp.注意,这样切片所产生的源时间序列的视图,跟numpy数组的切片运算时一样的.此外还有一个等价的实例方法也可以截取两个日期之间timeseries
    # print(ts.truncate(after='1/9/2011'))
    # # # # 以上的操作对DF也有效,例如,对DF的行进行索引:
    dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')
    long_df = DataFrame(np.random.randn(100, 4), index=dates, columns=['Colorado', 'Texas', 'New York', 'Ohio'])
    # print(long_df.head(10))
    # print(long_df.loc['5-2001'])

    # # # 带有重复索引的时间序列
    # # # # 在某些应用场景中,可能会存在多个观测数据落在同一个时间点上的情况.下面就是一些例子
    dates = pd.DatetimeIndex(['1/1/2000', '1/2/2000', '1/2/2000', '1/2/2000', '1/3/2000'])
    dup_ts = Series(np.arange(5), index=dates)
    # print(dup_ts)
    # # # # 通过检查索引的is_unique属性,就可以直到它是不是唯一的
    # print(dup_ts.index.is_unique)
    # # # # 对这个时间序列进行索引,要么产生标量值,要么产生切片,具体要看所选的时间点是否重复
    # print(dup_ts['1/3/2000'])
    # print(dup_ts['1/2/2000'])
    # # # # 想要对具有非唯一时间戳的数据进行聚合.一个办法是使用groupby,并传入level=0(索引的唯一一层)
    grouped = dup_ts.groupby(level=0)
    # print(grouped.mean())
    # print(grouped.count())

    # # # 日期的范围,频率以及移动
    # # # # pandas中的时间序列一般被认为是不规则的,也就是说,它们没有固定的频率.对于大部分应用程序而言,这是无所谓的,但是,它常常需要以某种相对固定的频率进行分析,比如每日,每月,每N分钟等(这样自然会在时间序列中引入缺失值).
    # # # # pandas由一整套标准时间序列频率以及用于重采样,频率推断,生成固定频率日期范围的工具
    # # # # 将时间序列转换为一个具有固定频率(每日)的时间序列,只需要调用resample即可:
    # print(ts)
    # print(ts.resample('D'))

    # # # 生成日期范围
    # # # # pandas.date_range可用于生成指定长度的DatetimeIndex
    index = pd.date_range('4/1/2012', '6/1/2012')
    # print(index)
    # # # # 默认情况下,date_range会产生按添加算的时间点.如果传入起始或结束日期,那就还得传入一个表示一段时间的数字
    # print(pd.date_range(start='4/1/2012', periods=20), '\n')
    # print(pd.date_range(end='6/1/2012', periods=20))
    # # # # 起始日期和结束日期定义了日期索引的严格边界,如果想要生成一个由每月最后一个工作日组成的日期索引,可以传入'BM'频率,这样就只会包含时间间隔内(或刚好在边界上的)符合频率要求的日期
    # print(pd.date_range('1/1/2000','12/1/2000',freq='BM'))
    # # # # date_range默认会保留起始和结束时间戳的时间信息(如果有的话)
    # print(pd.date_range('5/2/2012 12:56:31', periods=5))
    # # # # 虽然起始和结束日期带有时间信息,但是如果希望产生一组被规范化到午夜的时间戳,normalize选项即可实现该功能:
    # print(pd.date_range('5/2/2012 12:56:31', periods=5, normalize=True))

    # # # 频率和日期偏移量
    # # # # pandas中的频率是由一个基础频率和一个乘数组成的.基础频率通常以一个字符串别名表示,比如'M'表示每月,'H'表示每小时.对于每个基础频率,都有一个被称为日期偏移量(date offset)的对象与之对应
    # # # # 例:
    hour = Hour()
    # print(hour)
    # # # # 传入一个整数即可定义偏移量的倍数:
    four_hours = Hour(4)
    # print(four_hours)
    # # # # 一般来说,无需显式创建这样的对象,只需使用诸如'H'或'4H'这样的字符串别名即可,在基础频率前面放上一个整数即可创建倍数
    # print(pd.date_range('1/1/2000', '1/3/2000 23:59:00', freq='4h'))
    # # # # 大部分偏移量对象都可以通过假发进行连接:
    # print(Hour(2)+Minute(30))
    # # # # 同理,也可以传入频率字符串(如'2h30min'),这种字符串可以被高效地解析为等效表达式
    # print(pd.date_range('1/1/2000',periods=10,freq='1h30min'))
    # # # # 有些频率所描述的时间点并不是均匀分隔的.例如,'M'(日历月末)和'BM'(每月最后一个工作日)就取决于每月的天数,对于后者,还要考虑月末是不是周末.由于没有更好的术语,暂时将其称为锚点偏移量

    # # # WOM日期
    # # # # WOM(week of Month)是一种非常使用的频率,它以WOM开头,它可以帮助用户获得诸如"每月第三个星期五"之类的日期
    rng = pd.date_range('1/1/2012', '9/1/2012', freq='WOM-3FRI')
    # print(list(rng))

    # # # 移动(超前和滞后)数据
    # # # # 移动指的是沿着时间轴将数据前移或后移.Series和DataFrame都有一个shift方法用于执行单纯的迁移或后移操作,保持索引不变
    ts = Series(np.random.randn(4), index=pd.date_range('1/1/2000', periods=4, freq='M'))
    # print(ts,'\n')
    # print(ts.shift(2))
    # print(ts.shift(-2))
    # # # # shift通常用于计算一个时间序列或多个时间徐磊中的百分比变化,可以这样表达:ts/ts.shift(1)-1
    # # # # 由于单纯的位移操作不会修改索引,所以部分数据会被丢弃.因此,如果频率已知,则可以将其传给shift以便实现对时间戳进行位移而不是对数据进行简单位移
    # print(ts.shift(2, freq='M'))
    # # # # 还可以使用其它频率,这样就能非常灵活地对数据进行超前和滞后处理了
    # print(ts.shift(3, freq='D'), '\n')
    # print(ts.shift(-2, freq='3D'))
    # print(ts.shift(1,freq='90T'))

    # # # 通过偏移量对日期进行位移
    # # # # pandas的日期偏移量还可以用在datetime或timestamp对象上
    now = datetime(2011, 11, 17)
    # print(now + 3 * Day())
    # # # # 如果是锚点偏移量,第一次增量会将原日期向前滚动到符合频率规则的下一个日期:
    # print(now+MonthEnd())
    # print(now+MonthEnd(3))
    # # # # 通过锚点偏移量的rollforward和rollback方法,可显式地将日期向前或向后'滚动'
    offset = MonthEnd()
    # print(offset.rollback(now))
    # # # # 日期偏移量还有一个巧妙的用法,即结合groupby使用这两个滚动方法:
    ts = Series(np.random.randn(20),
                index=pd.date_range('1/15/2000', periods=20, freq='4d'))
    # print(ts)
    # print(ts.groupby(offset.rollforward).mean())
    # # # # 更简单,更快速地实现该功能的办法是使用resample
    # print(ts.resample('M').mean())

    # # # 时区处理
    # # # # 获取时区名
    # print(pytz.common_timezones[-5:])
    # # # # 获取时区对象
    tz = pytz.timezone('US/Eastern')
    # print(tz)
    # # # # pandas中的方法既可以几首时区名也可以接受这种对象

    # # # 本地化和转换
    # # # # 默认情况下,pandas中的时间序列是单纯的时区
    rng = pd.date_range('3/9/2012 9:30', periods=6, freq='D')
    ts = Series(np.random.randn(len(rng)), index=rng)
    # print(ts)
    # print(ts.index.tz)
    # # # # 在生成日期范围的时候还可以加上一个时区集
    # print(pd.date_range('3/9/2012 9:30', periods=10, freq='D', tz='UTC'))
    # # # # 从单纯到本地化的转换时通过tz_localize方法处理的
    ts_utc = ts.tz_localize('UTC')
    # print(ts_utc)
    # print(ts_utc.index)
    # # # # 一旦时间序列被本地化到某个特定时区,就可以用tz_convert将其转换到别的时区了
    # print(ts_utc.tz_convert('US/Eastern'))
    # # # # 对于以上这种时间序列,可以将其变化到EST,然后转换为UTC或柏林时间
    ts_eastern = ts.tz_localize('US/Eastern')
    # print(ts_eastern.tz_convert('UTC'))
    # print(ts_eastern.tz_convert('Europe/Berlin'))
    # # # # tz_Localize和tz_convert也是DatetimeIndex的实例方法
    # print(ts.index.tz_localize('Asia/Shanghai'))

    # # # 操作时区意识型TimeStamp对象
    # # # # 跟时间序列和日期范围差不多,TimeStamp对象也能被从单纯型本地化为时区意识型(time zone-aware),并从一个时区转换到另一个时区
    stamp = pd.Timestamp('2011-03-12 04:00')
    stamp_utc = stamp.tz_localize('utc')
    # print(stamp_utc.tz_convert('US/Eastern'))
    # # # # 在创建timestamp时,还可以传入一个时区信息
    stamp_moscow = pd.Timestamp('2011-03-12 04:00', tz='Europe/Moscow')
    # print(stamp_moscow)
    # # # # 时区意识型timestamp对象在内部保存了一个utc时间戳值(自UNIX纪元(1970年1月1日)算起的纳秒数).这个UTC值在时区转换过程中是不会发生变化的:
    # print(stamp_utc.value)
    # print(stamp_utc.tz_convert('US/Eastern').value)
    # # # # 当使用pandas的DataOffst对象执行时间算术运算时,运算过程会自动关注是否存在夏令时转变期
    # # # # 夏令时转变前30分钟
    stamp = pd.Timestamp('2012-03-12 01:30', tz='US/Eastern')
    # print(stamp)
    # print(stamp + Hour())
    # # # # 夏令时转变前90分钟
    stamp = pd.Timestamp('2012-03-12 00:30', tz='US/Eastern')
    # print(stamp)
    # print(stamp + 2 * Hour())

    # # # 不同时区之间的运算
    # # # # 如果两个时间序列的时区不同,在将它们合并到一起时,最终结果就会使UTC.由于时间戳其实是以UTC存储的,所以这是一个很简单的运算,并不需要发生任何转换
    rng = pd.date_range('3/7/2012 9:30', periods=10, freq='B')
    ts = Series(np.random.randn(len(rng)), index=rng)
    # print(ts,'\n')
    ts1 = ts[:7].tz_localize('Europe/London')
    ts2 = ts1[2:].tz_convert('Europe/Moscow')
    result = ts1 + ts2
    # print(result.index)

    # # # 时期及其算数运算
    # # # # 时期(period)表示的时时间区间,biru数日,数月,数季,数年等.period类所表示的就是这种数据类型,其构造函数需要用到一个字符串或整数
    p = pd.Period(2007, freq='A-DEC')
    # # # # 这个Period对象表示的是从2007年1月1日到2007年12月31日之间的整段时间.只需对Period对象加上或减去一个整数即可达到根据其频率进行位移的效果
    # print(p + 5)
    # # # # 如果两个period对象拥有相同的频率,则它们的查就是它们之间的单位数量
    # print(pd.Period('2014', freq='A-DEC') - p)
    # # # # period_range函数可用于创建规则的时期范围
    rng = pd.period_range('1/1/2000', '6/30/2000', freq='M')
    # print(rng)
    # # # # PeriodIndex类保存了一组Period,它可以在任何pandas数据结构中被用作轴索引
    # print(Series(np.random.randn(6),index=rng))
    # # # # PeriodIndex类的构造函数还允许直接使用一组字符串
    values = ['2001Q3', '2002Q2', '2003Q1']
    index = pd.PeriodIndex(values, freq='Q-DEC')
    # print(index)

    # # # 时期的频率转换
    # # # # Period和PeriodIndex对象都可以通过其asfreq方法被转换成别的频率.
    p = pd.Period('2007', freq='A-DEC')
    # print(p.asfreq('M',how='start'))
    # print(p.asfreq('M',how='end'))
    p = pd.Period('2007', freq='A-JUN')
    # print(p.asfreq('M', 'start'))
    # print(p.asfreq('M', 'end'))
    # # # # 在将高频率转换为低频率时,超时期是由子时期所属的位置决定的
    p = pd.Period('2007-08', 'M')
    # print(p.asfreq('A-JUN'))
    # # # # PeriodIndex或TimeSeries的频率转换方式也是如此
    rng = pd.period_range('2006', '2009', freq='A-DEC')
    ts = Series(np.random.randn(len(rng)), index=rng)
    # print(ts.head())
    # print(ts.asfreq('M',how='S'),'\n')
    # print(ts.asfreq('B',how='E'))

    # # # # 按季度计算的时期频率
    p = pd.Period('2012Q4', freq='Q-JAN')
    # print(p)
    # print(p.asfreq('D', how='S'))
    # print(p.asfreq('D', how='E'))
    p4pm = (p.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
    # print(p4pm)
    # print(p4pm.to_timestamp())
    # # # # period_range还可用于生成季度型范围.季度型范围的算数运算也跟上面是一样的
    rng = pd.period_range('2011Q3', '2012Q4', freq='Q-JAN')
    ts = Series(np.arange(len(rng)), index=rng)
    # print(ts)
    new_rng = (rng.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
    ts.index = new_rng.to_timestamp()
    # print(ts)

    # # # 将TimeStamp转换为Period(及其反向过程)
    # # # # 通过使用to_period方法,可以将由时间戳索引的Series和DataFrame对象转换为以时期索引
    rng = pd.date_range("1/1/2000", periods=3, freq='M')
    ts = Series(np.random.randn(3), index=rng)
    pts = ts.to_period()
    # print(pts)
    # # # # 由于时期指的是非重叠时间区间,因此对于给定的频率,一个时间戳智能属于一个时期.新PeriodIndex的频率默认是从时间戳推断而来的,也可以制定任何别的频率.结果中允许存在重复时期
    rng = pd.date_range('1/29/2000', periods=6, freq='D')
    ts2 = Series(np.random.randn(6), index=rng)
    # print(ts2)
    # print(ts2.to_period('M'))
    # # # # 要转换为时间戳,使用to_timestamp即可
    # print(pts.to_timestamp(how='E'))

    # # # 通过数组创建PeriodIndex
    # # # # 固定频率的数据集通常会将时间信息分开存放在多个列中
    data = pd.read_csv('../../data/examples/macrodata.csv')
    # print(data.year.head(), '\n')
    # print(data.quarter.head(), '\n')
    # # # # 将以上两个数组以及一个频率传入PeriodIndex,就可以将它们合并成DataFrame的一个索引
    index = pd.PeriodIndex(year=data.year, quarter=data.quarter, freq='Q-DEC')
    # print(index)
    data.index = index
    # print(data.infl.head())

    # # # 重采样及频率转换
    # # # # 重采样指的是将时间序列从一个频率转换到另一个频率的处理过程.将高频率数据聚合到低频率称为降采样,而将低频率数据转换到高频率则称为升采样.并不是所有的重采样都能被划分到这两个大类中.例如,将W-WED(每周三)转换为W-FRI既不是降采样也不是升采样
    # # # # pandas对象都带有一个resample方法,他是各种频率转换工作的主力函数
    rng = pd.date_range('1/1/2000', periods=100, freq='D')
    ts = Series(np.random.randn(len(rng)), index=rng)
    # print(ts,'\n')
    # print(ts.resample('M').mean())
    # print(ts.resample('M',kind='period').mean())
    # # # # resample是一个灵活高效的方法,可用于处理非常大的时间序列

    # # # 降采样
    # # # # 将数据聚合到规整的低频率是一件非常普通的时间序列处理任务,待聚合的数据不必拥有固定的频率,期望的频率会自动定义聚合的面元边界,这些面元用于将事件序列拆分为多个片段
    # # # # 各时间段都是半开放的.一个数据点智能属于一个时间段,所有时间段的并集必须能组成整个时间帧.在用resample对数据进行降采样时,需要考虑两样东西:1.各区间哪边时闭合的.2.如何标记各个聚合面元,用区间的开头还是末尾
    rng = pd.date_range('1/1/2000', periods=12, freq='T')
    ts = Series(np.arange(12), index=rng)
    # print(ts)
    # # # # 通过求和的方式将以上数据聚合到"5分钟"块中
    # print(ts.resample('5min').mean())
    # # # # 传入的频率将会以"5分钟"的增量定义面元边界.默认情况下,面元的右边界时包含的,因此00:00到00:05的区间中是包含00:05的.传入closed='left'会让区间以左边界闭合
    # print(ts.resample('5min',closed='right').mean())
    # # # # 传入lable='left'即可用面元的左边界对其进行标记
    # print(ts.resample('5min',closed='left',label='left').mean())
    # # # # 对结果索引做一些位移,比如从右边界减去一秒以便更容易明白时间戳到底表示的是哪个区间.只需要用过loffset设置一个字符串或日期偏移量即可实现
    # print(ts.resample('5min', loffset='-1s', label='left', closed='left').sum())

    # # # OHLC重采样
    # # # # 金融领域中有一种无所不在的时间序列聚合方式,即计算各面元的四个值,第一个值(open,开盘),最后一个值(close,收盘)，最大值(high,最高)以及最小值(low,最低).传入how='ohlc'即可得到一个含有这四种聚合值的DF,整个过程很高效,只需一次扫描即可计算出结果
    # print(ts.resample('5min').ohlc())

    # # # 通过groupby进行重采样
    # # # 另一种采样的办法是使用pandas的groupby功能
    rng = pd.date_range('1/1/2000', periods=100, freq='D')
    ts = Series(np.arange(100), index=rng)
    # print(ts.groupby(lambda x: x.month).mean())
    # print(ts.groupby(lambda x: x.weekday).mean())

    # # # 升采样和插值
    # # # # 在将数据从低频率转换到高频率时,就不需要聚合了
    frame = DataFrame(np.random.randn(2, 4),
                      index=pd.date_range('1/1/2000', periods=2, freq='W-WED'),
                      columns=['Colorado', 'Texas', 'New York', 'Ohio'])
    # print(frame)
    # # # # 将其重采样到日频率,默认会引入缺失值
    df_daily = frame.resample('D')
    # print(df_daily, '\n')
    # print(frame.resample('D').ffill())

    # # # 同样,这里也可以值填充指定的时期数(目的是限制前面的观测值的持续使用距离)
    # print(frame.resample('D', limit=2).ffill())
    # # # # 注意,新的日期索引完全没有必要跟旧的相交
    print(frame.resample('W-THU').ffill())
