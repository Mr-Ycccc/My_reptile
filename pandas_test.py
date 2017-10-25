# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:30:21 2017

@author: ChangYan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


print('一、创建对象：')
print('----------------------------通过传递一个list对象来创建一个Series，pandas会默认创建整型索引------------------')
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

print('----------------------------通过传递一个numpy array，时间索引以及列标签来创建一个DataFrame-----------------')
dates = pd.date_range('20170821', periods=6)
print(dates)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print(df)

print('---------------------------通过传递一个能够被转换成类似序列结构的字典对象来创建一个DataFrame---------------')
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20170821'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]),
                    'F': 'foo'
                    })
print(df2)
print('-------------------------------查看不同列的数据类型--------------------------------------------')
print(df2.dtypes)

print('\n二、查看数据：')
print('-------------------------------查看frame中头部和尾部的行--------------------------------------')
print(df.head())
print(df.tail())

print('------------------------------- 显示索引、列和数据--------------------------------')
print(df.index)
print(df.columns)
print(df.values)

print('----------------------------describe()函数对于数据的快速统计汇总-----------------------------------')
print(df.describe())

    print('--------------------------------  对数据的转置-------------------------------------------')
print(df.T)

print('--------------------------------   按轴进行排序-------------------------------------------')
print(df.sort_index(axis=1, ascending=False))

print('--------------------------------   按值进行排序-------------------------------------------')
#print(df.sort(columns='C'))
print('三、选择：\n\t\t ⊙.获取')
print('-------------------------选择一个单独的列，这将会返回一个Series，等同于df.A--------------')
print(df['A'])

print('------------------------- 通过[]进行选择，这将会对行进行切片--------------')
print(df[0:3])
print(df['20170821':'20170823'])
print('\n\t\t⊙.通过标签选择')
print('-------------------------使用标签来获取一个交叉的区域--------------')
print(df.loc[dates[0]])

print('-------------------------通过标签来在多个轴上进行选择--------------')
print(df.loc[:, ['A', 'B']])

print('------------------------- 标签切片--------------')
