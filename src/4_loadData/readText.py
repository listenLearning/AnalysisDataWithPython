#!/usr/bin/env python
__coding__ = "utf-8"
__author__ = " Ng WaiMing "

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import csv
import json
from lxml.html import parse
from urllib.request import urlopen
from pandas.io.parsers import TextParser
from lxml import objectify
import io


class my_dialect(csv.Dialect):
    pd.set_option('display.width', 10000)
    lineterminator = '\n'
    delimiter = ';'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL


if __name__ == "__main__":
    # # 类型推断(type inference)是这些函数中最重要的功能之一,也就是说,不需要指定列的类型到底是数值,整数,布尔值,还是字符串.
    # # 日期和其他自定义类型的处理需要多花点功夫才行
    # # ex1.csv以逗号分割,所以可以使用read_csv将其读入一个dataFrame
    frame = pd.read_csv('../../data/examples/ex1.csv')
    # print(frame)
    # # 也可以使用read_table,只不过需要指定分隔符而已
    # print(pd.read_table('../../data/examples/ex1.csv',sep=','))

    # # 并不是所有文件都有标题行,读入这种文件的办法有两个,
    # # 1.可以让pandas为其分配默认的列名
    # print(pd.read_csv('../../data/examples/ex2.csv', header=None))
    # # 2.自定义列名
    # print(pd.read_csv('../../data/examples/ex2.csv', names=['a', 'b', 'c', 'd', 'message']))
    # # 如果希望某一列作为df的索引,可以明确表示要将该列放到索引的位置上,也可以通过index_col参数指定
    names = ['a', 'b', 'c', 'd', 'message']
    # print(pd.read_csv('../../data/examples/ex2.csv',names=names,index_col='message'))
    # # 如果需要将多个列做成一个层次化索引,只需要传入由列编号或列名称组成的列表即可
    parsed = pd.read_csv('../../data/examples/csv_mindex.csv', index_col=['key1', 'key2'])
    # print(parsed)
    # print(pd.read_csv('../../data/examples/csv_mindex.csv'))

    # # 对于某些不是用固定的分隔符去分隔字段的(比如空白符或其他模式),对于这种情况,可以编写一个正则表达式来作为read_table的分隔符
    result = pd.read_csv('../../data/examples/ex3.txt', sep='\s+')
    # print(result)

    # # 使用skiprows跳过文件的第一行,第三行和第四行
    # print(pd.read_csv('../../data/examples/ex4.csv',skiprows=[0,2,3]))

    # # 缺失值处理时文件解析任务中的一个重要组成部分.缺失数据经常是要么没有(空白字符串),要么用某个标记值表示.默认情况下,pandas会用一组经常出现的标记值进行识别,如NA,-1.#IND以及NULL等
    result = pd.read_csv('../../data/examples/ex5.csv')
    # print(result)
    # print(result.isnull())
    result = pd.read_csv('../../data/examples/ex5.csv', na_values=['NULL'])
    # print(result)
    # # 可以用一个字典为各列指定不同的NA标记值
    sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
    # print(pd.read_csv('../../data/examples/ex5.csv', na_values=sentinels))

    # # 逐块读取文本文件
    # # 在处理很大的文件时,或找出打文件中的参数集以便于后续处理时,可能只想读取文件的一小部分或逐块对文件进行迭代
    result = pd.read_csv('../../data/examples/ex6.csv')
    # print(result)
    # # 如果指向读取几行(避免读取整个文件),通过nrows进行指定即可:
    # print(pd.read_csv('../../data/examples/ex6.csv',nrows=5))
    # # 要逐块读取文件,需要设置chunksize(行数)
    # # read_scv返回的textParser对象可以根据chunksize对文件进行逐块迭代
    chunker = pd.read_csv('../../data/examples/ex6.csv', chunksize=1000)
    # print(chunker)
    tot = Series([])
    for piece in chunker:
        tot = tot.add(piece['key'].value_counts(), fill_value=0)
    tot = tot.sort_values(ascending=False)
    # print(tot[:10])

    # # 将数据写出到文本格式
    # # 数据也可以被输出为分隔符格式的文本
    data = pd.read_csv('../../data/examples/ex5.csv')
    # # 利用DataFrame的to_csv方法,可以将数据写到一个以逗号分隔的文件中
    # data.to_csv('../../data/writeData/ex5.csv')
    # # 还可以使用其他分隔符,使用sep参数指定分隔符
    # data.to_csv('../../data/writeData/ex5.csv', sep='|')
    # # 缺失值在输出结果中会被表示为空字符串,如果希望将其表示为别的标记值,可以使用na_rep参数指定
    # data.to_csv('../../data/writeData/ex5.csv',na_rep='NULL')
    # # 如果没有设置其他选项,则会写出行和列的标签,如果希望禁用,可以使用index和header参数指定
    # data.to_csv('../../data/writeData/ex5.csv', index=False,header=False)
    # # 此外,还可以至写出一部分的列,并以指定的顺序排列
    # data.to_csv('../../data/writeData/ex5.csv', index=False, cols=['a', 'b', 'c'])
    # # Series也有一个to_csv方法
    dates = pd.date_range('1/1/2000', periods=7)
    ts = Series(np.arange(7), index=dates)
    # print(ts)
    # ts.to_csv('../../data/writeData/tseries.csv')
    # # 虽然只需要一点整理工作(无header行,第一列作为索引)就能用read_csv将CSV文件读取为Series,但还有一个更为方便的from_csv
    # print(Series.from_csv('../../data/writeData/tseries.csv', parse_dates=True))

    # # 收处理分隔符格式
    # # 大部分存储在磁盘上的表格行数据都能用pandas.read_table进行加载.然而,又是还是需要做一些手工处理.由于接收到含有畸形行的文件而使read_table出毛病的情况并不少见
    # # 对于任何单字符分隔符文件,可以直接使用python内置的csv模块.将任意已打开的文件或文件型的对象传给csv.reader
    f = open('../../data/examples/ex7.csv')
    reader = csv.reader(f)
    # # 对这个reader进行迭代将会为每一行产生一个元组(并移除了所有的引号)
    # for line in reader:
    #     print(line)
    # # 为了使数据格式合乎要求,需要做一些整理工作
    lines = list(csv.reader(open('../../data/examples/ex7.csv')))
    header, values = lines[0], lines[1:]
    data_dict = {h: v for h, v in zip(header, zip(*values))}
    # print(data_dict)
    # # CSV文件的形式有很多.只需要定义csv.Dialect的子类即可定义出新格式(如专门的分隔符,字符串引用约定,行结束符等)
    reader = csv.reader(f, dialect=my_dialect)
    # print(reader)
    # # 各个CSV语支的参数也可以关键字的形式提供给csv.reader,而无需定义子类
    reader = csv.reader(f, delimiter='|')
    # print(reader)
    # # 注意:对于哪些使用复杂分隔符或多字符分割符的文件,csv模块就无能为力了.这种情况下,就只能使用字符串的split方法或正则表达式方法re.split进行行拆分和其他整理工作了
    # # 要手工输出分隔符文件,可以使用csv.writer.它接受一个已打开且可写的文件对象以及跟csv.reader相同的哪些语支和格式化选项
    # with open('../../data/writeData/mydata.csv', 'w') as f:
    #     writer = csv.writer(f, dialect=my_dialect)
    #     writer.writerow(('one', 'two', 'three'))
    #     writer.writerow(('1', '2', '3'))
    #     writer.writerow(('4', '5', '6'))
    #     writer.writerow(('7', '8', '9'))

    # # JSON数据
    # # 除了空值null和一些其他席位的差别(如列表末尾不允许存在多余的逗号)之外,JSON非常接近于有效的Python代码,基本类型有对象(字典),数组(列表),字符串,数值,布尔值以及null.对象中所有的键都必须是字符串.通过json.loads即可将JSON字符串转换成python对象
    obj = """
    {"name":"Wes",
    "places_lived":["United States","Spain","Germany"],
    "pet":null,
    "siblings":[{"name":"Scott","age":25,"pet":"Zuko"},
    {"name":"Katie","age":33,"pet":"Cisco"}]
    }
    """
    result = json.loads(obj)
    # print(result)
    # # 相反,json.dumps则将python对象转换成JSON格式
    # print(json.dumps(result))
    # # 将(一个或一组)JSON对象转换为DF或其它便于分析的数据结构最简单的方式是:向DF构造器传入一组JSON对象,并选取字段的子集
    siblings = DataFrame(result['siblings'], columns=['name', 'age'])
    # print(siblings)

    # # XML和HTML:web信息收集:src/4_loadData/XML和HTML(web信息收集).ipynb

    # # 利用lxml.objectify解析XML
    # # XML是另一种常见的支持分层,嵌套数据以及元数据的结构化数据格式
    path = '../../data/dataSets/mta_perf/Performance_MNR.xml'
    parsed = objectify.parse(open(path))
    root = parsed.getroot()
    # # root.INDICATOR返回一个用于产生各个<INDICATOR>XML元素的生成器.对于每条记录,可以用标记名和数据值填充一个字典(排除几个标记)
    data = []
    skip_dields = ['PARENT_SEQ', 'INDICATOR_SEQ', 'DESIRED_CHANGE', 'DECIMAL_PLACES']
    for elt in root.INDICATOR:
        el_data = {}
        for child in elt.getchildren():
            if child.tag in skip_dields:
                continue
            el_data[child.tag] = child.pyval
        data.append(el_data)
    # # 最后将这组字典转换为一个DF
    pref = DataFrame(data)
    # print(pref)

    # # 更加复杂的XML???
    tag = '<a href = "http://www.google.com">Google</a>'
    root = objectify.parse(io.StringIO(tag)).getroot()
    # print(root.get('href'))
    # print(root.text)

    # # 二进制数据格式
    # # 实现数据的二进制格式存储最简单的办法之一就是使用python内置的pickle序列化,为了使用方便,pandas对象都有一个用于将数据以pickle形式保存到磁盘上的to_pickle方法
    frame = pd.read_csv('../../data/examples/ex1.csv')
    # print(frame)
    # frame.to_pickle('../../data/writeData/frame_pickle')
    # print(pd.read_pickle('../../data/writeData/frame_pickle'))

    # # 使用HDF5格式
    # # HDF5中HDF指的是层次型数据格式.每个HDF5文件都含有一个文件系统的节点结构,它使用户能够存储多个数据集并支持元数据.与其它简单格式相比,HDF5支持多种压缩器的即时压缩,还能更高效地存储重复模式数据.对于那些非常大的无法直接放入内存的数据集,HDF5是不错的选择,因为它可以高效的分块读写
    # # pythn中的HDF5库有两个接口(PyTables和h5py),它们各自采用了不同的问题解决方式,h5py提供了一种直接而高级的HDF5API访问接口,而PyTables则抽象了HDF5的许多细节以提供多种灵活的数据容器,表索引,插叙弄能以及对核外计算技术的某些支持
    # # pandas有一个最小化的类似于字典的HDFStore类,它通过PyTables存储pandas对象
    store = pd.HDFStore('../../data/writeData/mydata.h5')
    store['obj1'] = frame
    store['obj1_col'] = frame['a']
    # print(store)
    # # HDF5文件中的对象可以通过字典一样的方式进行获取
    print(store['obj1'])

    # # 读取Microsoft Excel文件
    # # pandas的ExcelFile类支持读取存储在Excel中的表格型数据.由于ExcelFile用到了xlrd和openpyxl包,所以需要先安装它们,通过传入一个xls或xlsx文件的路径即可创建一个excelfile实例
    # xls_file = pd.ExcelFile('data.xls')
    # # 存放在某个工作表中的数据可以通过parse读取到DataFrame中
    # table = xls_file.parse('Sheet1')
