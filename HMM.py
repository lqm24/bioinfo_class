#!/usr/bin/python
# -*- coding: utf-8 -*-

omega_x = ['Sunny', 'Cloudy', 'Rainy']
omega_o = ['Dry', 'Dryish', 'Damp', 'Soggy']
pi = [0.63, 0.17, 0.20]
a = [[0.500, 0.250, 0.250],
     [0.375, 0.250, 0.375],
     [0.125, 0.675, 0.200]]
b = [[0.60, 0.20, 0.15, 0.05],
     [0.25, 0.25, 0.25, 0.25],
     [0.05, 0.10, 0.35, 0.50]]
# 评估问题
sigma = ['Dry', 'Damp', 'Soggy', 'Dryish']
Pcondition = []
for i in range(len(omega_x)):
    Pcondition.append(pi[i]*b[i][0])
Pweather = []
for i in range(1, len(sigma)):
    for j in range(len(omega_x)):
        temp = []
        for k in range(len(Pcondition)):
            temp.append(Pcondition[k] * a[k][j])
            print "%f*%f" % (Pcondition[k], a[k][j])
        Pweather.append(sum(temp))
    Pcondition = []
    for p in range(len(Pweather)):
        Pcondition.append(Pweather[p]*b[p][omega_o.index(sigma[i])])
    Pweather = []
pvalue = sum(Pcondition)
print "P value is %f" % pvalue

# 解码
flag = []
Pcondition2 = []
for i in range(len(omega_x)):
    Pcondition2.append(pi[i]*b[i][0])
Pweather2 = []
for i in range(1, len(sigma)):
    flag_t = []
    for j in range(len(omega_x)):
        temp = []
        for k in range(len(Pcondition2)):
            temp.append(Pcondition2[k] * a[k][j])
        print max(temp)
        print (Pcondition2[temp.index(max(temp))], a[temp.index(max(temp))][j])
        flag_t.append(omega_x[Pcondition2.index(Pcondition2[temp.index(max(temp))])])
        Pweather2.append(max(temp))
    flag.append(flag_t)
    Pcondition2 = []
    for p in range(len(Pweather2)):
        Pcondition2.append(Pweather2[p]*b[p][omega_o.index(sigma[i])])
    print Pcondition2
    Pweather2 = []
pvalue2 = max(Pcondition2)
print "P value is %f" % pvalue2
last_day = omega_x[Pcondition2.index(max(Pcondition2))]


def traceback(l_d, flag, x, w_l):
    if x == -1:
        return
    else:
        w_l.append(flag[x][omega_x.index(l_d)])
        traceback(flag[x][omega_x.index(l_d)], flag, x-1, w_l)


weatherlist = [last_day]
traceback(last_day, flag, len(flag)-1, weatherlist)
weatherlist.reverse()
print weatherlist

