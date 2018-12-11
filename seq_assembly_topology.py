#!/usr/bin/python
# -*- coding: utf-8 -*-


def overlap(s1, s2):  # 计算s1与s2的重叠部分,s1的尾部去比较s2的头部
    if s1 == s2:
        return 0
    else:
        c1 = len(s1)
        for i in range(len(s1)):
            if s1[i:len(s1)] == s2[0:len(s1) - i]:
                break
            else:
                c1 = c1 - 1
        return c1


def input_degree(s, matrix, port):  # 计算序列的入度
    for m in matrix:
        if m[port.index(s)] != 0:
            return False
    return True


w = 'AGTATTGGCAATC'
z = 'AATCGATG'
u = 'ATGCAAACCT'
x = 'CCTTTTGG'
y = 'TTGGCAATCACT'
t = 3
port = [w, z, u, x, y]
new = []
while len(port) > 0:
    io_degree = [[0] * len(port) for i in range(len(port))]  # 初始化出度矩阵
    for i in range(len(port)):
        for j in range(len(port)):
            if overlap(port[i], port[j]) >= t:
                io_degree[i][j] = overlap(port[i], port[j])  # 计算出度矩阵
            else:
                io_degree[i][j] = 0
    for p in port:
        if input_degree(p, io_degree, port):  # 找到入度为０的序列,出队列,加入到new的队尾
            new.append(p)
            port.pop(port.index(p))
assembled_seq = new[0]
for i in range(len(new)-1):
    assembled_seq = assembled_seq + new[i+1][overlap(new[i], new[i+1]):]  # 将new中排好序的序列按重叠大小拼接起来
print "The rezult of 'Topology algorithm': %s" % assembled_seq

