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


def in_degree(s, matrix, port):  # 计算序列的入度
    for m in matrix:
        if m[port.index(s)] != 0:
            return False
    return True


def out_degree(s, matrix, port):
    contig = []
    for i in range(len(port)):
        contig.append(overlap(s, port[i]))
    if s is None:
        return True
    elif sum(contig) == 0:
        return True
    else:
        return False


def get_greedy_next(s, port):
    contig = []
    for i in range(len(port)):
        contig.append(overlap(s, port[i]))
    print contig
    for next in port:
        if contig[port.index(next)] == max(contig):
            return next
            break


w = 'AGTATTGGCAATC'
z = 'AATCGATG'
u = 'ATGCAAACCT'
x = 'CCTTTTGG'
y = 'TTGGCAATCACT'
port = [w, z, u, x, y]  # 将待排序序列放入列队
io_degree = [[0] * len(port) for i in range(len(port))]  # 初始化出度矩阵
new_list = []
while len(port) > 0:
    new = []
    for i in range(len(port)):
        for j in range(len(port)):
            io_degree[i][j] = overlap(port[i], port[j])  # 计算出度矩阵
    for s in port:
        if in_degree(s, io_degree, port):                # 找到入度为０的片段
            new.append(s)
            port.pop(port.index(s))
            break
    while not out_degree(new[-1], io_degree, port):     # 计算其出度是否为０
        nextone = get_greedy_next(new[-1], port)
        new.append(nextone)
        port.pop(port.index(nextone))
    assembled_seq = new[0]
    for i in range(len(new) - 1):
        assembled_seq = assembled_seq + new[i + 1][overlap(new[i], new[i + 1]):]  # 将new中排好序的序列按重叠大小拼接起来
    new_list.append(assembled_seq)

print new_list


