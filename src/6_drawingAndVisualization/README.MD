### pyplot.subplots的选项
|参数|说明|
|:---|:---|
|nrows|subplot的行数|
|ncols|subplot的列数|
|sharex|所有subplot应该使用相同的x轴刻度(调节xlim将会影响所有subplot)|
|sharey|所有subplot应该使用相同的y轴刻度(调节ylim将会影响所有的subplot)|
|subplot_kw|用于创建各subplot的关键字字典|
|**fig_kw|创建figure时的其他关键字,如果plt.subplots(2,2,figsize=(8,6))|