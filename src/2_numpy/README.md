## 数组创建函数
|函数|说明|
|:--|:--|
|array|将输入数据(列标,元组,数组或其它序列类型)转换为ndarray.要么推断出dtype,要么显式指定dtype.默认直接复制输入数据|
|asarray|将输入转换为ndarray,如果输入本身就是一个ndarray就不进行复制|
|arange|类似于内置的range,但返回的时一个ndarray而不是列标|
|ones,ones_like|根据指定的形状和dtype创建一个全1的数组.ones_like以另一个数组为参数,并根据其形状和dtype创建一个全1的数组|
|zeros,zeros_like|类似于ones和ones_like,只不过产生的是全0数组而已|
|empty,empty_like|创建新数组,只分配内存空间但不填充任何值|
|eye,identity|创建一个正方的$N\times{N}$单位矩阵(对角线为1,其余为0)|

# # Numpy的数据类型
|函数|类型代码|说明|
|:--|:--|:--|
|int8,uint8|i1,u1|有符号和无符号的8位(1个字节)整型|
|int16,uint16|i2,u2|有符号和无符号的16位(2个字节)整型|
|int32,uint32|i4,u4|有符号和无符号的32位(4个字节)整型|
|int64,uint64|i8,u8|有符号和无符号的64位(8个字节)整型|
|float16|f2|半精度浮点数|
|float32|f4或f|标准的单精度浮点数.与C的float兼容|
|float64|f8或d|标准的双精度浮点数.与C的Double和Python的float对象兼容|
|float128|f16或g|扩展精度浮点数|
|complex64,complex128,complex,256|c8,c16,c32|分别用两个32位、64位或128位浮点数表示的复数|
|bool|?|存储True和False值的布尔类型|
|object|O|Python对象类型|
|string_|S|固定长度额字符串类型(每个字符1个字节).例如,要创建一个长度位10的字符串,应使用S10|
|unicode_|U|固定长度的unicode类型(字节数由平台决定).跟字符串的定义方式一样(如U10)|

## 一元func
|函数|说明|
|:--|:--|
|abs,fabs|计算整数,浮点数或复数的绝对值.对于非复数值,可以使用更快的fabs|
|sqrt|计算各元素的平方根.相当于arr**0.5|
|square|计算各元素的平法.相当于arr**2|
|exp|计算各元素的指数$e^x$|
|log,log10,log2,log1p|分别位自然对数(底数位e),底数位为10的log,底数为2的log,log(1+x)|
|sign|计算各元素的正负号:1(正数),0(零),-1(负数)|
|ceil|计算各元素的ceiling值,即大于等于该值的最小整数|
|floor|计算各元素的floor值,即小于等于改制的最大整数|
|rint|将各元素值四舍五入到最接近的整数,保留dtype|
|modf|将数组的小数和整数部分以两个独立数组的形式返回|
|isnan|返回一个表示"哪些值是Nan(这不是一个数字)"的布尔型数组|
|isfinte,isinf|分别返回一个表示"哪些元素是有穷的(非inf，非Nan)"或"哪些元素是无穷的"的布尔型数组|
|cos,cosh,sin,sinh,tan,tanh|普通型和双曲型三角函数|
|arccos,arccosh,arcsin,arcsinh,arctan,arctanh|反三角函数|
|logical_not|计算各元素not x的真值,相当于-arr|

## 二元func
|函数|说明|
|:--|:--|
|add|将数组中对应的元素相加|
|subtract|从第一个数组中减去第二个数组中的元素|
|multiply|数组元素相乘|
|divide,floor_divide|除法或向下圆整除法(丢弃余数)|
|power|对第一个数组中的元素A,根据第二个数组中的相应元素B,计算$A^B$|
|maximum,fmax|元素级的最大值计算.fmax将忽略Nan|
|minimum,fmin|元素级的最小值计算.fmin将忽略nan|
|mod|元素级的求模计算(除法的余数)|
|copysign|将第二个数组中的值的符号复制给第一个数组中的值|
|greater,greater_equal,less,less_equal,equal,not_equal|执行元素级的比较运算,最终产生布尔型数组.相当于中缀运算符>,>=,<,<=,==,!=|
|logical_and,logical_or,logical_xor|执行元素级的真值逻辑运算.相当于中缀运算符&,|,^|

## 基本数组统计方法
|函数|说明|
|:--|:--|
|sum|对数组中全部或某轴向的元素求和.零长度的数组的sum为0|
|mean|算数平均数.零长度的数组mean为Nan|
|std,var|分别为标准差和方差,自由度可调(默认为n)|
|min,max|最大值和最小值|
|argmin,argmax|分贝为最大和最小元素的索引|
|cumsum|所有元素的累计和|
|cumprod|所有元素的累计积|

## 数组的集合运算
|函数|说明|
|:--|:--|
|unique(x)|计算x中的唯一元素,并返回有序结果|
|intersect1d(x,y)|计算x和y中的公共元素,并返回有序结果|
|union1d(x,y)|计算x和y的并集,并返回有序结果|
|in1d(x,y)|得到一个表示"x的元素是否包含于y"的布尔型数组|
|setdiff1d(x,y)|集合的差,即元素在x中且不在y中|
|setxor1d(x,y)|集合的对称差,即存在于一个数组中但不同是存在于两个数组中的元素|

## 常用的numpy.linalg函数
|函数|说明|
|:--|:--|
|diag|以一维数组的形式返回方阵的对角线(或非对角线)元素,或将一维数组转换为方阵(非对角线元素为0)|
|dot|矩阵乘法|
|trace|计算对角线元素的和|
|det|计算矩阵行列式|
|eig|计算方阵的本征值和本征向量|
|inv|计算方阵的逆|
|pinv|计算矩阵的Moore-Penrose伪逆|
|qr|计算QR分解|
|svd|计算奇异值分解|
|solve|解线性方程组Ax=b,其中A为一个方阵|
|lstsq|计算Ax=b的最小乘解|

## 部分numpy.random函数
|函数|说明|
|:--|:--|
|seed|确定随机数生成器的种子|
|permutation|返回一个序列的随机排列或返回一个随机排列的范围|
|shuffle|对一个序列就地随机排列|
|rand|产生均匀分布的样本值|
|randint|从给定的上下限范围内随机选取整数|
|randn|产生正态分布(平均值为0,标准差为1)的样本值,类似于MATLAB接口|
|binomial|产生二项分布的样本值|
|normal|产生正态(高斯)分布的样本值|
|beta|产生Beta分布分样本值|
|chisquare|产生卡方分布的样本值|
|gamma|产生Gamma分布的样本值|
|uniform|产生在(0,1)中均匀分布的样本值|