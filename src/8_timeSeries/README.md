# 时间序列
时间序列的具体场景:
- 时间戳,特定的时刻
- 固定时期,如2007年1月或2010年全年
- 时间间隔,由起始和结束时间戳表示.时期可以被看作间隔的特例
- 实验或过程时间,每个时间点都是相对于特定起始时间的一个度量.例如,从放入烤箱时起,每秒钟饼干的直径

### datetime模块中的数据类型
|类型|说明|
|:---|:---|
|date|以公历形式存储日历日期|
|time|将时间存储为时,分,秒,毫秒|
|datetime|存储日期和时间|
|timedelta|表示两个datetime值之间的查(日,秒,毫秒)|

### datetime格式定义(兼容ISO C89)
|代码|说明|
|:---|:---|
|%Y|4位数的年|
|%y|2位数的年|
|%m|2位数的月[01,12]|
|%d|2位数的日[01,31]|
|%H|时(24小时制)[00,23]|
|%I|时(12小时制)[01,12]|
|%M|2位数的分[00,59]|
|%S|秒[00,61](秒60和61用于闰秒)|
|%w|用整数表示的星期几[0,(星期天),6]|
|%U|每年的第几周[0,53].星期天被认为是每周的第一天,每年的第一个星期天之前的那几天被认为是"第0周"|
|%W|每年的第几周[00,53].星期一被认为是每周的第一天,每年第一个星期一之前的那几天被认为是"第0周"|
|%z|以+HHMM或-HHMM表示的UTC时区偏移量,如果时区为naive,则返回空字符串|
|%F|%Y-%m-%d简写形式,例如2012-4-18|
|%D|%m/%d/%Y简写形式,例如04/18/12|

### 特定于当前环境的日期格式
|代码|说明|
|:---|:---|
|%a|星期几的简写|
|%A|星期几的全称|
|%b|月份的简写|
|%B|月份的全称|
|%c|完整的日期和时间,例如"Tue 01 may 2012 04:20:57 PM"|
|%p|不同环境中的AM或PM|
|%x|适合于当前环境的日期格式,例如,在美国,'May 1, 2012'会产生'05/01/2012'|
|%X|适合于当前环境的时间格式,例如'04:24:12 PM'|

### 时间序列的基础频率
|别名|偏移量类型|说明|
|:---|:---|:---|
|D|Day|每日历日|
|B|BusinessDay|每工作日|
|H|Hour|每小时|
|T或min|Minute|每分|
|S|Second|每秒|
|L或ms|Milli|每毫秒(即千分之一秒)|
|U|Micro|每微秒(即每百万分之一秒)|
|M|MonthEnd|每月最后一个日历日|
|BM|BusinessMonthEnd|每月最后一个工作日|
|MS|MonthBegin|每月第一个日历日|
|BMS|BusinessMonthBegin|每月第一个工作日|
|W-MON,W-TUE...|Week|从指定的星期几(MON,TUE,WED,THU,FRI,SAT,SUN开始算起,每周)|
|WOM-1MON,WOM-2MON...|WeekOfMonth|产生每月第一,第二,第三或第四周的星期几.例如WOM-3FRI表示每月第三个星期五|
|Q-JAN,Q-FEB...|QuarterEnd|对于以指定月份(JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC)结束的年度,每季度最后一月的最后一个日历日|
|BQ-JAN,BQ-FEB|BusinessQuarterEnd|对于以指定月份结束的年度,每季度最后一阅的最后一个工作日|
|QS-JAN,QS-FEB...|QuarterBegin|对于以指定月份结束的年度,每季度最后一月的第一个日历日|
|BQS-JAN,BQS-FEB...|BusinessQuarterBegin|对于以指定月份结束的年度,每季度最后一个月的第一个工作日|
|A-JAN,A-FEB...|YearEnd|每年指定月份(JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC)的最后一个日历日|
|BA-JAN,BA-FEB...|BusinessYearEnd|每年指定月份的最后一个工作日|
|AS-JAN,AS-FEB...|YearBegin|每年指定月份的第一个日历日|
|BAS-JAN,BAS-FEB...|BusinessYearBegin|每年指定月份的第一个工作日|

### resample方法的参数
|参数|说明|
|:---|:---|
|freq|表示重采样频率的字符串或DateOffset,例如'M','5min'或Second(15)|
|how='mean'|用于产生聚合值的函数名或数组函数,例如"mean",'ohlc',np.max等.默认为mean,其他常用的值有:'first','last','median','ohlc','max','min'|
|axis=0|重采样的轴,默认为axis=0|
|fill_method=None|升采样时如何插值,比如'ffill'或'bfill',默认不插值|
|colsed='right'|在降采样中,各时间段的哪一段时闭合(即包含)的,'right'或'left'.默认为'right'|
|lable='right'|在降采样中,如何设置聚合值的标签,'right'或'left'(面元的右边界或左边界).例如,9:30到9:35之间的这5分钟会被标记为9:30或9:35.默认为'right'|
|loffset=None|面元标签的事件校正值.比如'-1s'/Second(-1)用于将聚合标签调早疫苗|
|limit=None|在前向或后向填充时,允许填充的最大时期数|
|kind=None|聚合到时期('period')或时间戳('timestamp'),默认聚合到时间序列的索引类型|
|convention=None|当重采样时期时,将低频率转换到高频率所采用的约定("start"或"end").默认为"end"|