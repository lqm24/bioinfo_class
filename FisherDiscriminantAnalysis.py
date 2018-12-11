#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import numpy as np
import matplotlib.pyplot as mpl
from scipy.linalg import solve
f1 = io.open('/home/lqm/python/data/Fisher/Fisher-positive.txt', 'r', encoding='utf-8')   # 读入两类数据
f2 = io.open('/home/lqm/python/data/Fisher/Fisher-negative.txt', 'r', encoding='utf-16')
positive = f1.readlines()
negative = f2.readlines()
positive_list = []
negative_list = []
p = len(positive)
q = len(negative)
for neg in negative:
    negative_list.append(neg.strip('\n\r').split('\t'))
for pos in positive:
    positive_list.append(pos.strip('\n\r').split('\t'))
n = len(positive_list[0])
data_set = [positive_list, negative_list]
sumOfColumn = [[], []]
meanSumOfColumn = [[], []]
for i in range(n):
    temp = []
    for j in range(p):
        temp.append(float(positive_list[j][i]))
    sumOfColumn[0].append(sum(temp))     # 计算Ｘi(1) 1~p 求和
    meanSumOfColumn[0].append(sumOfColumn[0][i]/p)  # 计算 1/p Xi(1)求和的值
for i in range(n):
    temp = []
    for j in range(q):
        temp.append(float(negative_list[j][i]))
    sumOfColumn[1].append(sum(temp))     # 计算Ｘi(2) 1~q 求和
    meanSumOfColumn[1].append(sumOfColumn[1][i]/q)  # 计算 1/q Xi(2)求和的值

sumOfSquares_p = [[0]*n for i in range(n)]
sumOfSquares_n = [[0]*n for i in range(n)]
for i in range(n):
    for j in range(n):
        temp = []
        for k in range(p):
            temp.append(float(positive_list[k][i]) * float(positive_list[k][j]))  # 计算Ｘi(1)*Xj(1) 1~p 求和
        sumOfSquares_p[i][j] = sum(temp)
for i in range(n):
    for j in range(n):
        temp = []
        for k in range(p):
            temp.append(float(negative_list[k][i]) * float(negative_list[k][j]))  # 计算Ｘi(2)*Xj(2) 1~q 求和
        sumOfSquares_n[i][j] = sum(temp)
sumOfSquares = [sumOfSquares_p, sumOfSquares_n]
d = []
for i in range(n):
    d.append(meanSumOfColumn[0][i] - meanSumOfColumn[1][i])  # 计算ｄ
S = [[0]*n for i in range(n)]
for i in range(n):                                           # 计算Ｓ协方差
    for j in range(n):
        S[i][j] = sumOfSquares[0][i][j] - 1.0/p * sumOfColumn[0][i] * sumOfColumn[0][j] + sumOfSquares[1][i][j] - 1.0/q\
                  * sumOfColumn[1][i] * sumOfColumn[1][j]

a = np.array(S)
b = np.array(d)
C = solve(a, b)
print C

meanY = []
for i in range(2):
    sumTemp = []
    for j in range(n):
        sumTemp.append(C[j]*meanSumOfColumn[i][j])
    meanY.append(sum(sumTemp))

C_value = (p*meanY[0] + q*meanY[1])/(p + q)

print C_value

T_value = [[],[]]
for i in range(2):
    for j in range(10):
        t = []
        for k in range(10):
            t.append(float(C[k]) * float(data_set[i][j][k]))
        if sum(t)>C_value:
            T_value[i].append(True)
        else:
            T_value[i].append(False)
print T_value
