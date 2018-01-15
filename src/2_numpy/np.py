#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from numpy import *
import matplotlib.pyplot as plt

set_printoptions(linewidth=10000)
# 1. 数组与标量之间的运算
arr = array([[1., 2., 3.], [4., 5., 6.]])
# print(arr)
# # 1.1 数组的矢量化:大小相等的数组之间的任何算数运算都会将运算应用到元素级别
# print(arr + arr)
# print(arr * arr)
# print(arr - arr)
# print(arr / arr)
#
# # 1.2 数组与标量的算数运算也会将标量传播(广播)到各个元素
# # 不同大小的数组之间的运算叫做广播
# print(arr ** 0.5)
#
# # 基本的索引和切片
# # 数组切片和列表切片最重要的区别在于,数组切片是原始数组的视图.这意味着数据不会被复制,视图熵的任何修改都会直接反映到源数组上
arr = arange(0, 100, 10)
# print(arr)
# print(arr[5])
# print(arr[5:8])
# arr1 = arr[5:8].copy()
# arr[5:8] = 120
# print(arr)
#
# # 1.3 高维数组上的索引
arr3d = empty((3, 4, 5))
# print(arr3d, '\n')
# # print(arr3d[2])
# # print(arr3d[2][2][1], '<==>', arr3d[2, 2, 1])
# # # 1.3.1 高维数组熵的切片
# print(arr3d[2:, 2:, 1][0, 0])
# 1.4 Boolean型索引
random.seed(0)
names = array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = random.randn(7, 4)
# print(data, '\n')
# print(data[names == 'Bob', 2:], '\n')
# print(data[-(names == 'Bob')], '\n\n', '<==>', '\n\n', data[names != 'Bob'], '\n')
# data[data < 0] = 0
# print(data)
#
# # 花式索引,即传入一组索引下标的数组
arr = zeros((8, 4))
for i in range(shape(arr)[0]):
    arr[i] = i
# print(arr, '\n')
# print(arr[[4, 3, 0, 6]])
# # 当一次传入多个索引时,写法稍有不同
arr = arange(32).reshape((8, 4))
# print(arr, '\n')
# print(arr[[4, 3, 0, 6]][:, [3, 1, 0, 2]])
#
# # 数组的转置和轴对换
arr = arange(15).reshape((3, 5))
# print(arr, '\n')
# print(arr.T, '\n')
# print(dot(arr.T, arr))
arr = arange(16).reshape((2, 2, 4))
# print(arr, '\n')
# print(arr.transpose((1, 0, 2)),'\n')
# print(arr.transpose())
# print(arr.swapaxes(1, 2))
arr = random.randn(7) * 5
# print(arr)
# # modf返回浮点数的整数部分数组以及浮点部分数组
# print(modf(arr))

# 利用数据进行数据处理
points = arange(-5, 5, 0.01)
xs, ys = meshgrid(points, points)
# print(xs, '\n\n', ys)
z = sqrt(xs ** 2 + ys ** 2)
# print(z)
# plt.imshow(z, cmap=plt.cm.gray)
# plt.colorbar()
# plt.title('Image plot of $\sqrt{x^2+y^2}$ for grid of value')
# plt.show()

# # 将条件逻辑表述为数组运算
xarr = array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = array([True, False, True, True, False])
result = where(cond, xarr, yarr)
# print(result)

arr = random.randn(4, 4)
# print(arr, '\n')
result = where(arr > 0, 2, -2)
# print(result)
cond1 = array([True, False, True, True, False])
cond2 = array([True, False, True, True, False])
result = where(cond1 & cond2, 0, where(cond1, 1, where(cond2, 2, 3)))
# print(result)
# print('<==>')
result = 1 * (cond1 - cond2) + 2 * (cond1 & -cond2) + 3 * -(cond1 | cond2)
# print(result)

# # 随机漫步
nsteps = 1000
draw = random.randint(0, 2, size=nsteps)
steps = where(draw > 0, 1, -1)
walk = steps.cumsum()
# print(walk.min())
# print(walk.max())
# print((abs(walk) >= 10).argmax())
# # 一次模仿多个随机漫步
nwalks = 5000
nsteps = 1000
draw = random.randint(0, 2, size=(nwalks, nsteps))
steps = where(draw > 0, 1, -1)
walk = steps.cumsum(1)
print(walk, '\n')
print(walk.max(), '\n')
print(walk.min(), '\n')
hits30 = (abs(walk) >= 30).any(1)
print(hits30, hits30.sum())
crossing_times = (abs(walk[hits30]) >= 30).argmax(1)
print(crossing_times, crossing_times.min(),crossing_times.mean())
