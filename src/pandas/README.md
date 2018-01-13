## 可以输入给DataFrame构造器的数据
|类型|说明|
|:---|:---|
|二维ndarray|数据矩阵,还可以传入行标和列标|
|由数组、列表和元组组成的字典|每个序列会变成DataFrame的一列.所有序列的长度必须相同|
|Numpy的结构化/记录数组|类似于"由数组组成的字典"|
|由Series组成的字典|每个Series会成为一列.如果没有显式指定索引,则各Series的索引会被合并成结果的行索引|
|由字典组成的字典|各内层字典会成为一列.键会被合并成结果的行索引,跟"由Series组成的字典"的情况一样|
|字典或Series的列表|各项将会成为DataFrame的一行.字典键或Series索引的并集将会成为DataFrame的列标|
|由列表或元组组成的列表|类似于"二维ndarray"|
|另一个DataFrame|该DataFrame的索引将会被沿用,除非显式指定了其它索引|
|Numpy的MaskedArray|类似于"二维ndarray"的情况,只是掩码值在结果DataFrame会变成NA/缺失值|

## pandas中主要的index对象
|类型|说明|
|:---|:---|
|Index|最泛化的Index对象,将轴标签表示为一个由python对象组成的numpy数组|
|Int64Index|针对整数的特殊Index|
|MultiIndex|"层次化"索引对象,表示单个轴上的多层索引.可以看作由元组组成的数组|
|DatetimeIndex|存储纳秒级时间戳(用Numpy的datetime64类型表示)|
|PeriodIndex|针对Period数据(时间戳)的特殊Index|

## Index的方法和属性
|类型|说明|
|:---|:---|
|append|连接另一个Index对象,产生一个新的Index|
|diff|计算差集,并得到一个Index|
|intersection|计算交集|
|union|计算并集|
|isin|计算一个指示各值是否都包含在参数集合中的布尔型数组|
|delete|删除索引i处的元素,并得到新的Index|
|drop|删除传入的值,并得到新的Index|
|insert|将元素插入到索引i处,并得到新的Index|
|is_monotonic|当各元素均大于等于前一个元素时,返回True|
|is_unique|当Index没有重复值时,返回True|
|unique|计算Index中唯一值的数组|

## reindex的(插值)method选项
|类型|说明|
|:---|:---|
|ffill或pad|前向填充(或搬运)值|
|bfill或backfill|后向填充(或搬运)值|

## reindex函数的参数
|类型|说明|
|:---|:---|
|index|用作索引的新序列.既可以是Index实例,也可以是其它序列型的Python数据结构.Index会被完全使用,就像没有任何复制一样|
|method|插值(填充)方式,具体参数参见"reindex的(插值)method选项"|
|fill_value|在重新索引的过程中,需要引入缺失值时使用的替代值|
|limit|前向或后向填充时的最大填充量|
|level|在MultiIndex的指定级别上匹配简单索引,否则选择其子集|
|copy|默认为True,无论如何都复制,如果为False,则新旧相等就不复制|

## DataFrame的索引选项
|类型|说明|
|:---|:---|
|obj[val]|选取DataFrame的单个列或一组列.在一些特殊情况下会比较便利:布尔型数组(过滤行),切片(行切片),布尔型DataFrame(根据条件设置值)|
|obj.ix[val]|选取DataFrame的单个行或一组行|
|obj.ix[:,val]|选取单个列或列子集|
|obj.ix[val1,val2]|同时选取行和列|
|reindex方法|将一个或多个轴匹配到新索引|
|xs方法|根据标签选取单行或单列,并返回一个Series|
|icol,irow方法|根据整数位置选取单列或单行,并返回一个Series|
|get_value,set_value方法|根据行标签和列标签选取单个值|

## 灵活的算术方法
|类型|说明|
|:---|:---|
|add|用于加法(+)的方法|
|sub|用于减法(-)的方法|
|div|用于除法(/)的方法|
|mul|用于乘法(*)的方法|