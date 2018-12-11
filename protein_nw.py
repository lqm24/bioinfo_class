#!/usr/bin/python
# -*- coding: utf-8 -*-

# example p1: AGWGAHEA p2: PAWHEAEAG


def Max(a, b, c):  # 返回最大值
    s = [a, b, c]
    s.sort()
    return s[2]


def Score(p_s, g_s, top, topLeft, left):  # 根据全局比对罚分规则确定该位置的得分
    topScore = top + g_s
    leftScore = left + g_s
    topLeftScore = topLeft + p_s
    return Max(topScore, leftScore, topLeftScore)


def Score_local(p_s, g_s, top, topLeft, left):  # 根据局部比对罚分规则确定该位置的得分
    topScore = top + g_s
    leftScore = left + g_s
    topLeftScore = topLeft + p_s
    if Max(topScore, leftScore, topLeftScore) >= 0:
        return Max(topScore, leftScore, topLeftScore)
    else:
        return 0


P1 = 'AGWGPHEA'
P2 = 'PAWGEAHAG'
P1 = P1.upper()
P2 = P2.upper()
gap_score = -8
Length1 = len(P1)  # type: int
Length2 = len(P2)  # type: int
Matrix = [[0]*(Length2 + 1) for i in range(Length1 + 1)]    # 声明对应大小的得分矩阵
pam250 = [[5, -1, 0, -2, -1, -3],  # 输入pam250矩阵
          [-1, 6, -3, 0, -1, -3],
          [0, -3, 8, -2, -2, -3],
          [-2, 0, -2, 10, -2, -3],
          [-1, -1, -2, -2, 10, -4],
          [-3, -3, -3, -3, -4, 15]
          ]
A, E, G, H, P, W = range(6)  # 方便将输入的字符直接对应矩阵下标

print("global alignment rezult :")

# 初始化得分矩阵
for i in range(Length2):
    Matrix[0][i + 1]= Matrix[0][i] + gap_score
for i in range(Length1):
    Matrix[(i + 1)][0] = Matrix[i][0] + gap_score

# 循环计算得分矩阵,通过Score函数进行具体得分计算
for i in range(Length1):
    for j in range(Length2):
        Matrix[i + 1][j + 1] = Score(pam250[eval(P1[i])][eval(P2[j])], gap_score, Matrix[i][j + 1], Matrix[i][j], Matrix[i + 1][j])

# 打印出全局得分矩阵
for i in range(Length1 + 1):
    print(Matrix[i])

# 回溯,找出最优解


def traceback(seq1, seq2, pam, gap, M, x, y, s1, s2, t1, t2):  # 定义全局比对回溯的函数
    if x == 0 and y == 0:
        s1.append("" + t1)
        s2.append("" + t2)
        return
    if M[x][y] - M[x - 1][y] == gap:
        traceback(seq1, seq2, pam, gap, M, x-1, y, s1, s2, seq1[x] + t1, "-" + t2)
    if M[x][y] - M[x][y - 1] == gap:
        traceback(seq1, seq2, pam, gap, M, x, y-1, s1, s2, "-" + t1, seq2[y] + t2)
    if M[x][y] - M[x - 1][y - 1] == pam[eval(seq1[x])][eval(seq2[y])]:
        traceback(seq1, seq2, pam, gap, M, x-1, y-1, s1, s2, seq1[x] + t1, seq2[y] + t2)


s1 = []
s2 = []
t1 = ""
t2 = ""
P1 = ' ' + P1
P2 = ' ' + P2
traceback(P1, P2, pam250, gap_score, Matrix, Length1, Length2, s1, s2, t1, t2)

print(s1)
print(s2)
print(len(s1))

print("Local alignment rezult:")
P1 = P1.strip()
P2 = P2.strip()
Matrix2 = [[0]*(Length2 + 1) for i in range(Length1 + 1)]

# 循环计算得分矩阵,通过Score函数进行具体得分计算
for i in range(Length1):
    for j in range(Length2):
        Matrix2[i + 1][j + 1] = Score_local(pam250[eval(P1[i])][eval(P2[j])], gap_score, Matrix2[i][j + 1], Matrix2[i][j], Matrix2[i + 1][j])

# 打印出局部比对得分矩阵
for i in range(Length1 + 1):
    print(Matrix2[i])

# 找到得分矩阵中最大值
temp = Matrix2[0]
for i in range(len(Matrix2) - 1):
    temp = temp + Matrix2[i + 1]
max_score = max(temp)

# 保存局部得分最大值对应的下标
x_index = []
y_index = []
print "max score is :%d\n" % max_score
for i in range(Length1 + 1):
    for j in range(Length2 + 1):
        if Matrix2[i][j] == max_score:
            x_index.append(i)
            y_index.append(j)


# 回溯,找出最优解

def traceback_local(seq1, seq2, pam, gap, S, x, y, s1, s2, t1, t2):  # 定义局部比对的回溯函数
    if S[x][y] == 0:
        s1.append("" + t1)
        s2.append("" + t2)
        return
    if S[x][y] - S[x - 1][y] == gap:
        traceback_local(seq1, seq2, pam, gap, S, x-1, y, s1, s2, seq1[x]+t1, "-"+t2)
    if S[x][y] - S[x][y - 1] == gap:
        traceback_local(seq1, seq2, pam, gap, S, x, y-1, s1, s2, "-" + t1, seq2[y] + t2)
    if S[x][y] - S[x - 1][y - 1] == pam[eval(seq1[x])][eval(seq2[y])]:
        traceback_local(seq1, seq2, pam, gap, S, x-1, y-1, s1, s2, seq1[x] + t1, seq2[y] + t2)


s1_local = []
s2_local = []
t1_local = ""
t2_local = ""
P1 = ' ' + P1
P2 = ' ' + P2
for i in range(len(x_index)):
    traceback_local(P1, P2, pam250, gap_score, Matrix2, x_index[i], y_index[i], s1_local, s2_local, t1_local, t2_local)
print(s1_local)
print(s2_local)
print(len(s1_local))