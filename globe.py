#!/usr/bin/python2.7
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


P1 = 'AGWGPHEA'
P2 = 'PAWGEAHAG'
P1 = P1.upper()
P2 = P2.upper()
gap_score = -8
Length1 = len(P1)  # type: int
Length2 = len(P2)  # type: int
Matrix = [[0] * (Length2 + 1) for i in range(Length1 + 1)]  # 声明对应大小的得分矩阵
Matrix_trace = [[0] * ((Length2 + 1) * 3) for i in range((Length1 + 1) * 3)]  # 声明对应大小的回溯方向记录矩阵
pam250 = [[5, -1, 0, -2, -1, -3],  # 输入pam250矩阵
          [-1, 6, -3, 0, -1, -3],
          [0, -3, 8, -2, -2, -3],
          [-2, 0, -2, 10, -2, -3],
          [-1, -1, -2, -2, 10, -4],
          [-3, -3, -3, -3, -4, 15]
          ]
A, E, G, H, P, W = range(6)  # 方便将输入的字符直接对应矩阵下标


# 初始化得分矩阵
for i in range(Length2):
    Matrix[0][i + 1] = Matrix[0][i] + gap_score
for i in range(Length1):
    Matrix[(i + 1)][0] = Matrix[i][0] + gap_score

# 循环计算得分矩阵,通过Score函数进行具体得分计算
for i in range(Length1):
    for j in range(Length2):
        Matrix[i + 1][j + 1] = Score(pam250[eval(P1[i])][eval(P2[j])], gap_score, Matrix[i][j + 1], Matrix[i][j],
                                     Matrix[i + 1][j])

# 填充轨迹回溯矩阵的对应位置的得分
for i in range(Length1 + 1):
    for j in range(Length2 + 1):
        if (i == 0) & (j != 0):
            Matrix_trace[0][3*j+1] = P2[j-1]
        Matrix_trace[3*i+1][3*j+1] = Matrix[i][j]
    if i != 0:
        Matrix_trace[3*i+1][0] = P1[i-1]



# 回溯,找出最优解
def traceback(seq1, seq2, pam, gap, M, x, y, s1, s2, t1, t2, M_t):  # 定义全局比对回溯的函数
    if x == 0 and y == 0:
        s1.append("" + t1)
        s2.append("" + t2)
        return
    if M[x][y] - M[x - 1][y] == gap:
        M_t[3 * x][3 * y + 1] = "|"
        M_t[3 * x - 1][3 * y + 1] = "|"
        traceback(seq1, seq2, pam, gap, M, x - 1, y, s1, s2, seq1[x] + t1, "-" + t2, M_t)
    if M[x][y] - M[x][y - 1] == gap:
        M_t[3 * x + 1][3 * y] = "---"
        M_t[3 * x + 1][3 * y - 1] = "---"
        traceback(seq1, seq2, pam, gap, M, x, y - 1, s1, s2, "-" + t1, seq2[y] + t2, M_t)
    if M[x][y] - M[x - 1][y - 1] == pam[eval(seq1[x])][eval(seq2[y])]:
        M_t[3 * x][3 * y] = "\\"
        M_t[3 * x - 1][3 * y - 1] = "\\"
        traceback(seq1, seq2, pam, gap, M, x - 1, y - 1, s1, s2, seq1[x] + t1, seq2[y] + t2, M_t)


s1 = []
s2 = []
t1 = ""
t2 = ""
P1 = ' ' + P1
P2 = ' ' + P2
traceback(P1, P2, pam250, gap_score, Matrix, Length1, Length2, s1, s2, t1, t2, Matrix_trace)

# 打印出回溯路径矩阵
print("global alignment rezult :")
for i in range((Length1 + 1) * 3):
    for j in range((Length2 + 1) * 3):
        if (Matrix_trace[i][j] == 0) & (i*j != 1):
            print ("".center(3)),
        else:
            print (str(Matrix_trace[i][j]).center(3)),
    print "\n"

print(s1)
print(s2)
print(len(s1))
